"""Refresh the dataset from deployedbyai.com and regenerate README.md and CITATION.cff from its own metadata.

Run daily by .github/workflows/refresh.yml. The data files are copied byte for byte; every
number in the README is counted from data.json, never typed. A hub page is linked only when
its exact URL is in the record's live sitemap.
"""
import csv
import datetime
import html
import io
import json
import re
import sys
import urllib.error
import urllib.request
import zoneinfo
from collections import Counter

BASE = "https://deployedbyai.com/log/"
UA = "the-deploy-log-refresh (+https://github.com/dotcomjack/the-deploy-log)"
REPO = "https://github.com/dotcomjack/the-deploy-log"
INDEXES = (("", "The Deploy Log"), ("company/", "Companies"), ("model/", "Models"),
           ("platform/", "Platforms"), ("week/", "Week by week"), ("month/", "Month by month"))
SPDX = {"CC BY 4.0": "CC-BY-4.0"}
ET = zoneinfo.ZoneInfo("America/New_York")
TOP = 15


def fetch(name):
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status != 200:
                    sys.exit(f"{name}: HTTP {r.status}")
                return r.read()
        except (urllib.error.URLError, ConnectionError):
            # One retry: a reset handshake was measured on 2026-10-06; a second failure stops the run.
            if attempt == 2:
                raise


def num(n):
    return f"{n:,}"


def long_date(day):
    d = datetime.date.fromisoformat(day) if isinstance(day, str) else day
    return f"{d:%B} {d.day}, {d.year}"


def span(a, b):
    """Two dates the way the record's week pages print them: October 5 to 11, 2026."""
    if a.year != b.year:
        return f"{long_date(a)} to {long_date(b)}"
    if a.month != b.month:
        return f"{a:%B} {a.day} to {b:%B} {b.day}, {b.year}"
    return f"{a:%B} {a.day} to {b.day}, {b.year}"


def rows_word(n):
    return f"{num(n)} row" if n == 1 else f"{num(n)} rows"


def and_list(items):
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " and " + items[-1]


def added_et(r):
    """When the row entered the record, on New York's clock, the day the record's own pages print."""
    return datetime.datetime.fromisoformat(r["added_at"].replace("Z", "+00:00")).astimezone(ET)


def cell(text):
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def link(text, url):
    return f"[{cell(text)}]({url})" if url else cell(text)


def listed(r):
    """The date a row is listed for: the publisher's date, otherwise its edition's date."""
    return r.get("published_date") or r.get("edition_date")


def iso_week(day):
    y, w, _ = datetime.date.fromisoformat(day).isocalendar()
    return f"{y}-W{w:02d}"


def anchors(page, kind, locs):
    """Hub URLs of one kind linked from a page, keyed by their link text, kept only if the sitemap lists them."""
    found = {}
    for href, inner in re.findall(r'<a[^>]+href="(/log/' + kind + r'/[^"]+/)"[^>]*>(.*?)</a>', page, flags=re.S):
        url = "https://deployedbyai.com" + href
        name = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
        if url in locs and name:
            found[name] = url
    return found


def hubs():
    """What the live sitemap lists, plus lane and company hub URLs keyed by the name the record links them by."""
    locs = set(re.findall(r"<loc>([^<]+)</loc>", fetch("sitemap.xml").decode("utf-8")))
    if BASE not in locs:
        sys.exit("sitemap.xml does not list the record itself")
    lanes = anchors(fetch("").decode("utf-8"), "lane", locs)
    companies = anchors(fetch("company/").decode("utf-8"), "company", locs) if BASE + "company/" in locs else {}
    return locs, lanes, companies


def validate(d):
    rows = d["rows"]
    if len(rows) != d["count"]:
        sys.exit(f"data.json count {d['count']} but {len(rows)} rows")
    if not rows:
        sys.exit("data.json has no rows")
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", listed(r) or "") for r in rows):
        sys.exit("a row has no ISO date")
    if not all(r.get("source_url") and r.get("record_url") for r in rows):
        sys.exit("a row has no source_url or record_url")
    if any(r.get("published_date") and r.get("edition_date") for r in rows):
        sys.exit("a row carries both a publisher's date and an edition's date")
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}T.+Z", r.get("added_at") or "") for r in rows):
        sys.exit("a row has no UTC added_at")
    if not all(r.get("company") and r.get("subject") for r in rows):
        sys.exit("a row has no company or subject")
    if any(r.get("lane") is None and not r.get("edition_n") for r in rows):
        sys.exit("a row in no lane was carried by no edition")
    if not all(re.fullmatch(r"[0-9a-f]{12}", r.get("row_key") or "") for r in rows):
        sys.exit("a row_key is not 12 lowercase hexadecimal characters")
    if not all(r["date_label"].startswith("Published " if r.get("published_date") else f"Edition {r.get('edition_n')}, ")
               for r in rows):
        sys.exit("a date_label does not match the row's date")
    names = [e.get("name") for e in d.get("dictionary") or []]
    if names != d["fields"] or not all(e.get("description") for e in d["dictionary"]):
        sys.exit("data.json dictionary does not describe exactly its fields")
    lane_words = d["dictionary"][names.index("lane")]["description"]
    if any(r.get("lane") and r["lane"] not in lane_words for r in rows):
        sys.exit("a row's lane is not one the dictionary names")
    if d["license"]["name"] not in SPDX:
        sys.exit(f"license {d['license']['name']!r} has no SPDX id here")


def readme(d, locs, lanes, companies):
    validate(d)
    rows = d["rows"]
    total = d["count"]
    url = d["url"]
    pub = [r for r in rows if r.get("published_date")]
    days = sorted(listed(r) for r in rows)
    by_company = Counter(r["company"] for r in rows)
    hub = lambda u: u if u in locs else None
    today = datetime.datetime.now(ET).date()
    newest = datetime.date.fromisoformat(days[-1])
    monday = newest - datetime.timedelta(days=newest.weekday())
    sunday = monday + datetime.timedelta(days=6)
    open_week = monday <= today <= sunday

    wk = iso_week(monday.isoformat())
    week_rows = [r for r in rows if iso_week(listed(r)) == wk]
    week_pub = sum(1 for r in week_rows if r.get("published_date"))
    wc = Counter(r["company"] for r in week_rows)
    tiers = sorted(set(wc.values()), reverse=True)
    tier = lambda n: sorted((c for c in wc if wc[c] == n), key=lambda c: (c.casefold(), c))
    first = tier(tiers[0])
    most = (f"{first[0]} shipped the most, {rows_word(tiers[0])}" if len(first) == 1
            else f"{and_list(first)} shipped the most, {rows_word(tiers[0])} each")
    if len(tiers) > 1:
        second = tier(tiers[1])
        who = and_list(second) if len(second) <= 5 else f"{num(len(second))} companies"
        most += f", then {who} with {num(tiers[1])}" + (" each" if len(second) > 1 else "")
    title = f"What shipped in AI, week of {long_date(monday)}"
    week_url = hub(f"{BASE}week/{wk}/")
    out = [f"# {d['name']}", "", d["description"], "",
           f"## {link(title, week_url)}", "",
           f"{rows_word(len(week_rows))} are listed for {span(monday, sunday)} in The Deploy Log, from "
           f"{num(len(wc))} {'company' if len(wc) == 1 else 'companies'}. {most}. {num(week_pub)} carry a "
           f"publisher's date and {num(len(week_rows) - week_pub)} are placed by their edition."
           + (f" The week runs to Sunday, {long_date(sunday)}, and was still in progress when this file was "
              f"built on {long_date(today)} (ET)." if open_week else ""), "",
           "## The record", "",
           f"The record holds {num(total)} rows, {num(len(pub))} with a publisher's date, "
           f"{num(total - len(pub))} placed by their edition, from {num(len(by_company))} companies. "
           f"Rows are listed from {long_date(days[0])} to {long_date(days[-1])}, each by its publisher's date "
           f"or, where the record carries none, its edition's date. The newest row entered the record on "
           f"{long_date(max(added_et(r) for r in rows).date())} (ET). Every row carries `source_url`, the "
           f"publisher's own page, and `record_url`, its page in the record at {url}", ""]

    idx = [(BASE + p, label) for p, label in INDEXES if BASE + p in locs]
    if idx:
        out += ["## Indexes", ""]
        for u, label in idx:
            n = sum(1 for x in locs if x.startswith(u) and x != u and u != BASE)
            out.append(f"- [{label}]({u})" + (f": {num(n)} pages listed in the record's sitemap" if n else ""))
        out.append("")

    lane_rows = Counter(r.get("lane") for r in rows)
    lane_pub = Counter(r.get("lane") for r in pub)
    out += ["## Rows by lane", "",
            f"Each row is filed in one of {num(len([k for k in lane_rows if k]))} lanes, except an edition's "
            f"lead, which is filed in no lane.", "",
            "| Lane | Rows | With a publisher's date | Placed by their edition |", "|---|---:|---:|---:|"]
    order = sorted(lane_rows, key=lambda k: (k is None, -lane_rows[k], k or ""))
    for k in order:
        name = link(k, lanes.get(k)) if k else "Leads (filed in no lane)"
        out.append(f"| {name} | {num(lane_rows[k])} | {num(lane_pub[k])} | {num(lane_rows[k] - lane_pub[k])} |")
    if sum(lane_rows.values()) != total:
        sys.exit("lane counts do not sum to the row count")
    out += [f"| Total | {num(total)} | {num(len(pub))} | {num(total - len(pub))} |", ""]

    ranked = sorted(by_company, key=lambda c: (-by_company[c], c.casefold(), c))
    # Every company tied with the last one shown is shown too, so the cut never drops a tie.
    top = [c for c in ranked if by_company[c] >= by_company[ranked[min(TOP, len(ranked)) - 1]]]
    out += [f"## The {len(top)} companies with the most rows", "",
            f"Ordered by rows, then by name. First and latest are the earliest and newest publisher's date "
            f"among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.", "",
            "| Company | Rows | With a publisher's date | First | Latest |", "|---|---:|---:|---|---|"]
    for c in top:
        ds = sorted(r["published_date"] for r in pub if r["company"] == c)
        first, last = (ds[0], ds[-1]) if ds else ("none", "none")
        out.append(f"| {link(c, companies.get(c))} | {num(by_company[c])} | {num(len(ds))} | {first} | {last} |")
    out.append("")

    by_week = Counter(iso_week(listed(r)) for r in rows)
    pub_week = Counter(iso_week(r["published_date"]) for r in pub)
    weeks = [monday - datetime.timedelta(weeks=i) for i in range(8)]
    out += ["## Rows per week, the 8 newest ISO weeks", "",
            "A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its "
            "edition's date where the record carries none. The newest week is the one holding the newest listed date.",
            "",
            "| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |",
            "|---|---|---:|---:|---:|"]
    for m in weeks:
        w = iso_week(m.isoformat())
        mark = " (in progress)" if m <= today <= m + datetime.timedelta(days=6) else ""
        out.append(f"| {link(w, hub(f'{BASE}week/{w}/'))}{mark} | {m.isoformat()} to "
                   f"{(m + datetime.timedelta(days=6)).isoformat()} | {num(by_week[w])} | {num(pub_week[w])} | "
                   f"{num(by_week[w] - pub_week[w])} |")
    out.append("")

    by_month = Counter(listed(r)[:7] for r in rows)
    month_pub = Counter(r["published_date"][:7] for r in pub)
    out += ["## Rows per month", "", "A row counts in the month of its listed date, as above.", "",
            "| Month | Rows | With a publisher's date | Placed by their edition |", "|---|---:|---:|---:|"]
    for m in sorted(by_month, reverse=True):
        label = f"{datetime.date.fromisoformat(m + '-01'):%B %Y}"
        out.append(f"| {link(label, hub(f'{BASE}month/{m}/'))} | {num(by_month[m])} | {num(month_pub[m])} | "
                   f"{num(by_month[m] - month_pub[m])} |")
    if sum(by_month.values()) != total:
        sys.exit("month counts do not sum to the row count")
    out += [f"| Total | {num(total)} | {num(len(pub))} | {num(total - len(pub))} |", ""]

    latest = sorted(rows, key=lambda r: (added_et(r), r["row_key"]), reverse=True)[:10]
    out += [f"## The {len(latest)} rows added most recently", "",
            "Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.", "",
            "| Added (ET) | Company | Row | Source |", "|---|---|---|---|"]
    for r in latest:
        out.append(f"| {added_et(r).date().isoformat()} | {link(r['company'], companies.get(r['company']))} | "
                   f"{link(r['subject'], r['record_url'])} | {link(r['source'], r['source_url'])} |")
    out.append("")

    out += ["## Files", "",
            "- `data.csv`: the record, one line per row",
            "- `data.json`: the same rows with this metadata",
            "- `CITATION.cff`: how to cite the record", "",
            f"Both data files are copied daily from {url}data.csv and {url}data.json, unchanged.", "",
            "## Data dictionary", "",
            "Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.", "",
            "| Field | Rows with a value | What it holds |", "|---|---:|---|"]
    for e in d["dictionary"]:
        filled = sum(1 for r in rows if r.get(e["name"]) not in (None, ""))
        out.append(f"| `{e['name']}` | {num(filled)} | {cell(e['description'])} |")
    lic = d["license"]
    out += ["", "## Cite this", "",
            "`CITATION.cff` in this repository gives the record's title, author, license and URL.", "",
            "## License", "",
            f"[{lic['name']}]({lic['url']}). Attribution: {lic['attribution']}", ""]
    return "\n".join(out)


def citation(d):
    site = re.match(r"https://[^/]+/", d["url"]).group(0)
    q = json.dumps
    return "\n".join([
        "cff-version: 1.2.0",
        f"message: {q('If you use this dataset, please cite it as below.')}",
        "type: dataset",
        f"title: {q(d['name'])}",
        f"abstract: {q(d['description'])}",
        "authors:",
        f"  - name: {q(d['publisher'])}",
        f"    website: {q(site)}",
        f"license: {SPDX[d['license']['name']]}",
        f"url: {q(d['url'])}",
        f"repository-code: {q(REPO)}",
        "",
    ])


def check_csv(raw, d):
    table = list(csv.reader(io.StringIO(raw.decode("utf-8"))))
    if not table or table[0] != d["fields"]:
        sys.exit("data.csv header does not match data.json fields")
    if len(table) - 1 != d["count"]:
        sys.exit(f"data.csv has {len(table) - 1} rows, data.json says {d['count']}")


def snapshot(site):
    raw_json = fetch("data.json")
    raw_csv = fetch("data.csv")
    d = json.loads(raw_json.decode("utf-8"))
    text = readme(d, *site).encode("utf-8")
    check_csv(raw_csv, d)
    return d, raw_json, raw_csv, text


def main():
    site = hubs()
    # A row can land between the two fetches; one fresh pair settles it.
    try:
        d, raw_json, raw_csv, text = snapshot(site)
    except SystemExit:
        d, raw_json, raw_csv, text = snapshot(site)
    outputs = (("data.json", raw_json), ("data.csv", raw_csv), ("README.md", text),
               ("CITATION.cff", citation(d).encode("utf-8")))
    for name, data in outputs:
        with open(name, "wb") as f:
            f.write(data)
    missing = [BASE + p for p, _ in INDEXES if BASE + p not in site[0]]
    print(f"{d['count']} rows; sitemap lacks: {', '.join(missing) or 'no index'}")


if __name__ == "__main__":
    main()
