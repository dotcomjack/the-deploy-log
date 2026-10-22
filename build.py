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
# The record counts the requests it serves, page and data file reads and every MCP tools/call, and files a client that
# names deployedbyai as one of the brand's own tools, not a reader (dcj-newsletter src/publisher/log.ts, ROBOT). This
# build reads /log/, the hub indexes, both data files and the MCP server daily, so every request it sends names itself.
UA = "deployedbyai the-deploy-log-refresh (+https://github.com/dotcomjack/the-deploy-log)"
MCP_UA = UA
REPO = "https://github.com/dotcomjack/the-deploy-log"
INDEXES = (("", "The Deploy Log"), ("company/", "Companies"), ("model/", "Models"),
           ("platform/", "Platforms"), ("week/", "Week by week"), ("month/", "Month by month"))
SPDX = {"CC BY 4.0": "CC-BY-4.0"}
ET = zoneinfo.ZoneInfo("America/New_York")
TOP = 15
# The API section's CORS line, and the CORS column of any API directory that lists the record, say this; a data file
# answered with any other access-control-allow-origin stops the build.
CORS = "*"
MEDIA = {"data.json": "application/json", "data.csv": "text/csv"}
CLIP = 160  # the example row cuts a prose string longer than this, and says so


def get(name):
    """One GET's body, headers and final URL, so a claim about a response is read off the response the file came from."""
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                if r.status != 200:
                    sys.exit(f"{name}: HTTP {r.status}")
                return r.read(), r.headers, r.geturl()
        except (urllib.error.URLError, ConnectionError):
            # One retry: a reset handshake was measured on 2026-10-06; a second failure stops the run.
            if attempt == 2:
                raise


def fetch(name):
    return get(name)[0]


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
    text = re.sub(r"\s+", " ", text).strip()  # a newline in a cell would end its table row
    return (text.replace("\\", "\\\\").replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
            .replace("`", "\\`").replace("<", "&lt;"))


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


def mcp_post(body, what):
    """One JSON-RPC body POSTed to the record's MCP server, and its answer parsed."""
    req = urllib.request.Request(BASE + "mcp", data=body, method="POST", headers={
        "User-Agent": MCP_UA, "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                raw = r.read()
            break
        except (urllib.error.URLError, ConnectionError, TimeoutError) as e:
            # One retry, as fetch() does; a second failure stops the run before any file is written.
            if attempt == 2:
                sys.exit(f"mcp {what}: {e}")
    try:
        return json.loads(raw.decode("utf-8"))
    except ValueError as e:
        sys.exit(f"mcp {what}: the answer is not JSON ({e!r})")


def mcp_tools():
    """The record's MCP server and its tools as the server itself lists them, so the README never types a tool name."""
    answer = mcp_post(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}).encode("utf-8"), "tools/list")
    try:
        tools = answer["result"]["tools"]
    except (KeyError, TypeError) as e:
        sys.exit(f"mcp tools/list: no tools in the answer ({e!r})")
    check_tools(tools)
    fetch("mcp/")  # the server's own page, linked below with ?k=mcp, which this daily robot must not count as a visit
    return tools


def default_ua_refused():
    """True when deployedbyai.com refuses Python's default User-Agent on data.csv, False when it serves it, None unread."""
    # A GET of one byte, the method pandas uses, not a HEAD, which a site may answer differently.
    req = urllib.request.Request(BASE + "data.csv", headers={
        "User-Agent": f"Python-urllib/{sys.version_info[0]}.{sys.version_info[1]}", "Range": "bytes=0-0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status not in (200, 206)
    except urllib.error.HTTPError as e:
        return e.code == 403 or None
    except (urllib.error.URLError, ConnectionError, TimeoutError):
        return None


def check_tools(tools):
    names = [t.get("name") for t in tools]
    if len(tools) < 3 or not all(names) or not all(t.get("description") for t in tools):
        sys.exit(f"mcp tools/list returned {len(tools)} tool(s), or one without a name or description")
    if "search_deployments" not in names:
        sys.exit("mcp tools/list has no search_deployments, the tool the README's example calls")


def example_answer(call, args, tools, rows):
    """The README's tools/call, made with the very body it prints, and the answer cut to its first row. Returns the
    answer to print and how many objects and lines were cut. Refuses an argument the tool's own schema does not list,
    an error, no row, more rows than asked, a row without its URLs, or rows that data.json does not hold."""
    schema = next(t for t in tools if t["name"] == "search_deployments").get("inputSchema") or {}
    known, need = set(schema.get("properties") or {}), set(schema.get("required") or [])
    if not set(args) <= known or not need <= set(args):
        sys.exit(f"search_deployments lists arguments {sorted(known)}, {sorted(need)} required; the README's call "
                 f"sends {sorted(args)}")
    answer = mcp_post(call.encode("utf-8"), "tools/call")
    if "error" in answer or (answer.get("result") or {}).get("isError"):
        sys.exit(f"mcp tools/call answered an error: {json.dumps(answer)[:300]}")
    try:
        items = answer["result"]["structuredContent"]["items"]
        lines = answer["result"]["content"][0]["text"].split("\n")
    except (KeyError, IndexError, TypeError, AttributeError) as e:
        sys.exit(f"mcp tools/call: no rows in the answer ({e!r})")
    if not 1 <= len(items) <= args["limit"]:
        sys.exit(f"mcp tools/call answered {len(items)} row(s) to {json.dumps(args)}")
    if not all(i.get("id") and i.get("source_url") and i.get("record_url") for i in items):
        sys.exit("mcp tools/call answered a row without its id, source_url or record_url")
    if not {i["id"] for i in items} & {r["row_key"] for r in rows}:
        sys.exit("mcp tools/call answered no row that data.json holds")
    # The text carries one line per row after a count line; keep it to the line that names the first row's record_url.
    kept = next((n + 1 for n, line in enumerate(lines) if items[0]["record_url"] in line), len(lines))
    shown = json.loads(json.dumps(answer))
    shown["result"]["structuredContent"]["items"] = items[:1]
    shown["result"]["content"][0]["text"] = "\n".join(lines[:kept])
    return shown, len(items) - 1, len(lines) - kept


def latest_release():
    """The newest dated release of this repository and the names of its files, or None when GitHub does not answer
    (the line is then left out)."""
    req = urllib.request.Request("https://api.github.com/repos/dotcomjack/the-deploy-log/releases/latest",
                                 headers={"User-Agent": UA, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            rel = json.loads(r.read().decode("utf-8"))
        return rel["tag_name"], rel["html_url"], {a["name"] for a in rel.get("assets") or []}
    except (urllib.error.URLError, ConnectionError, TimeoutError, KeyError, TypeError, ValueError):
        return None


def arguments(tool):
    """A tool's arguments in words, from its own input schema: each name, marked where it is required."""
    schema = tool.get("inputSchema") or {}
    need = set(schema.get("required") or [])
    return ", ".join(f"`{k}`" + (" (required)" if k in need else "")
                     for k in (schema.get("properties") or {})) or "none"


def json_type(v):
    return ("boolean" if isinstance(v, bool) else "number" if isinstance(v, (int, float)) else
            "string" if isinstance(v, str) else "array" if isinstance(v, list) else
            "object" if isinstance(v, dict) else "null")


def api(d, served, refused, today):
    """The API section. Each header it prints is read off the response the data files were copied from, and each
    sentence holds only while its check here, in validate() or in check_csv() passes."""
    for name, media in MEDIA.items():
        headers, final = served[name]
        if not final.startswith("https://"):
            sys.exit(f"{name}: answered from {final}, not over HTTPS")
        if (headers.get("Content-Type") or "").split(";")[0].strip().lower() != media:
            sys.exit(f"{name}: Content-Type {headers.get('Content-Type')!r}, not {media}")
        if headers.get("Access-Control-Allow-Origin") != CORS:
            sys.exit(f"{name}: access-control-allow-origin {headers.get('Access-Control-Allow-Origin')!r}, "
                     f"the README says {CORS!r}")
    rows = d["rows"]
    if not all(list(r) == d["fields"] for r in rows):
        sys.exit("a row in data.json is not keyed by exactly its fields, in their order")
    url, total = d["url"], d["count"]
    ctype = {n: served[n][0]["Content-Type"] for n in MEDIA}
    out = ["## API", "",
           "Two GET endpoints return the whole record, every row in one response. A row's fields are described in "
           "the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see "
           "[Ask it from an agent](#ask-it-from-an-agent).", "",
           "| Method | URL | Content-Type | Returns |", "|---|---|---|---|",
           f"| GET | {url}data.json | `{ctype['data.json']}` | One JSON object, with the keys below |",
           f"| GET | {url}data.csv | `{ctype['data.csv']}` | The {num(total)} rows as CSV, under a header line of "
           f"the field names |", "",
           "- Auth: none. A GET that carries no key, token or cookie answers 200.",
           "- HTTPS: yes.",
           f"- CORS: both answer with `access-control-allow-origin: {CORS}`."]
    if refused:
        out.append("- User-Agent: send your own. deployedbyai.com refuses Python's default one "
                   "([Load it](#load-it)).")
    # Meanings checked: fields against data.csv's header (check_csv), dictionary and count (validate), rows above.
    said = {"fields": f"The {num(len(d['fields']))} field names, in the order of `data.csv`'s header",
            "dictionary": f"{num(len(d['dictionary']))} objects, a `name` and a `description` per field: the "
                          f"[Data dictionary](#data-dictionary)",
            "count": f"{num(total)}, the number of objects in `rows`",
            "rows": f"{num(len(rows))} objects, one per row, each keyed by the names in `fields`, in that order"}

    def holds(k, v):
        if k in said:
            return said[k]
        if isinstance(v, str):
            return cell(v)
        if isinstance(v, dict):
            return "Keys " + ", ".join(f"`{x}`" for x in v)
        return f"{num(len(v))} items" if isinstance(v, list) else cell(json.dumps(v))

    out += ["", "`data.json` holds these keys, in this order:", "",
            "| Key | Type | Holds |", "|---|---|---|"]
    out += [f"| `{k}` | {json_type(v)} | {holds(k, v)} |" for k, v in d.items()]
    first = {k: v[:CLIP].rsplit(" ", 1)[0] + "..." if isinstance(v, str) and len(v) > CLIP and " " in v[:CLIP] else v
             for k, v in rows[0].items()}
    out += ["", f"Example: the first object in `rows`, as `data.json` served it when this file was built on "
                f"{long_date(today)} (ET)"
            + (f". A string longer than {CLIP} characters is cut here and ends in `...`:" if first != rows[0] else ":"),
            "", "```json", json.dumps(first, indent=2, ensure_ascii=False), "```", ""]
    return out


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


def readme(d, served, locs, lanes, companies, tools, release, refused):
    validate(d)
    check_tools(tools)
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
              f"built on {long_date(today)} (ET)." if open_week else ""), ""]
    record = ["## The record", "",
           f"The record holds {num(total)} rows, {num(len(pub))} with a publisher's date, "
           f"{num(total - len(pub))} placed by their edition, from {num(len(by_company))} companies. "
           f"Rows are listed from {long_date(days[0])} to {long_date(days[-1])}, each by its publisher's date "
           f"or, where the record carries none, its edition's date. The newest row entered the record on "
           f"{long_date(max(added_et(r) for r in rows).date())} (ET). Every row carries `source_url`, the "
           f"publisher's own page, and `record_url`, its page in the record at {url}", ""]

    raw = REPO.replace("https://github.com/", "https://raw.githubusercontent.com/") + "/main/data.csv"
    # Measured at build time (default_ua_refused): only while the site refuses Python's default User-Agent does
    # the pandas line read this repository's copy and say why; unread, it reads the copy and says nothing.
    out += ["## Load it", ""]
    if refused:
        out += [f"deployedbyai.com refuses a request that carries Python's default User-Agent, which "
                f"`pandas.read_csv` sends by default, so the Python example reads this repository's copy, "
                f"refreshed daily.", ""]
    out += ["```sh", f"curl -sO {url}data.csv", "```", "",
            "```python", "import pandas as pd", "",
            f'rows = pd.read_csv("{url + "data.csv" if refused is False else raw}")', "```", ""]
    if release and {"data.csv", "data.json"} <= release[2]:
        out += [f"The newest dated release, [{release[0]}]({release[1]}), carries `data.csv` and `data.json` as "
                f"files; every release is at {REPO}/releases", ""]
    out += api(d, served, refused, today)

    # The example asks for this week's leading company, a name the record holds, never one typed here.
    ask = next((c for c in sorted(wc, key=lambda c: (-wc[c], c.casefold(), c))
                if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9 .-]{1,79}", c)), "AI")
    args = {"query": ask, "limit": 3}
    call = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": "search_deployments", "arguments": args}})
    shown, cut_items, cut_lines = example_answer(call, args, tools, rows)
    many = lambda n, one, more: f"{num(n)} {one if n == 1 else more}"
    out += ["## Ask it from an agent", "",
            f"The record answers over the Model Context Protocol at `{url}mcp`: "
            + ("read only, " if all((t.get("annotations") or {}).get("readOnlyHint") is True for t in tools) else "")
            + f"over Streamable HTTP (POST), with no key. Its tools, as the server lists them "
            f"([the server's page]({url}mcp/?k=mcp) also names the protocol versions it speaks):", "",
            "| Tool | What it returns | Arguments |", "|---|---|---|"]
    for t in tools:
        out.append(f"| `{t['name']}` | {cell(t['description'])} | {arguments(t)} |")
    out += ["", "One call, without a client:", "",
            "```sh", f"curl -s {url}mcp -H 'content-type: application/json' \\",
            "  -H 'accept: application/json, text/event-stream' \\", f"  -d '{call}'", "```", "",
            f"The response, as the server answered it when this file was built on {long_date(today)} (ET)"
            + (f", cut to its first row: left out are {many(cut_items, 'more object', 'more objects')} in "
               f"`structuredContent.items` and {many(cut_lines, 'more line', 'more lines')} of `content[0].text`:"
               if cut_items or cut_lines else ":"),
            "", "```json", json.dumps(shown, indent=2, ensure_ascii=False), "```", ""]
    out += record

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
        filled = sum(1 for r in rows if r.get(e["name"]) not in (None, "", []))
        out.append(f"| `{e['name']}` | {num(filled)} | {cell(e['description'])} |")
    lic = d["license"]
    out += ["", "## Cite this", "",
            "`CITATION.cff` in this repository gives the record's title, author, license and URL.", "",
            "## License", "",
            f"[{lic['name']}]({lic['url']}). Attribution: {lic['attribution']}", ""]
    text = "\n".join(out)
    # Every #anchor the README links must be one of its own plain headings, slugged the way GitHub slugs them.
    slugs = {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
             for h in re.findall(r"^#+ ([^\[\n]+)$", text, flags=re.M)}
    missing = sorted(set(re.findall(r"\]\(#([^)]+)\)", text)) - slugs)
    if missing:
        sys.exit(f"README links #{', #'.join(missing)}, a heading it does not have")
    if "\u2014" in text or "\u2013" in text:
        sys.exit("README would carry an em dash or an en dash")
    return text


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
    raw_json, h_json, u_json = get("data.json")
    raw_csv, h_csv, u_csv = get("data.csv")
    d = json.loads(raw_json.decode("utf-8"))
    text = readme(d, {"data.json": (h_json, u_json), "data.csv": (h_csv, u_csv)}, *site).encode("utf-8")
    check_csv(raw_csv, d)
    return d, raw_json, raw_csv, text


def main():
    site = hubs() + (mcp_tools(), latest_release(), default_ua_refused())
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
