"""Refresh the dataset from deployedbyai.com and regenerate README.md and CITATION.cff from its own metadata.

Run daily by .github/workflows/refresh.yml. The data files are copied byte for byte; every
number in the README is counted from data.json, never typed. A hub page is linked only when
its exact URL is in the record's live sitemap.

The same build writes the record as pages a reader opens in the repository: weeks/<ISO week>.md and
companies/<name>.md, each under an index. Every row on them is printed from data.json, with its source.
"""
import csv
import datetime
import html
import io
import json
import os
import posixpath
import re
import sys
import tempfile
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
DASHES = ("\u2014", "\u2013")
# What a page under weeks/ or companies/ prints of a row: its text and its two links.
PRINTED = ("company", "subject", "what_shipped", "source", "source_url", "record_url")
ROW = ("Row", "What shipped", "Source")
ENCODED = {"|": "%7C", " ": "%20", "(": "%28", ")": "%29", "<": "%3C", ">": "%3E", "\\": "%5C"}
HUB = re.compile(re.escape(BASE) + r"company/([0-9a-f]{12})/([a-z0-9][a-z0-9-]*)/")


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


def prose(text):
    """Row text on the pages under weeks/ and companies/. cell() stays as it is, so the README's bytes do not move;
    these pages print every row's own sentence, where emphasis, a strikethrough, a tag or math would redraw it."""
    text = re.sub(r"\s+", " ", text).strip().replace("&", "&amp;")
    text = re.sub(r"([\\*_\[\]`~|])", r"\\\1", text).replace("<", "&lt;").replace(">", "&gt;")
    # Measured on GitHub's renderer on 2026-11-04: two dollar signs in one cell render as math ('($2)$' did), a
    # backslash or &#36; does not stop it and a span around each sign does. Signs in two cells never pair, so a
    # lone one stays bare.
    return text.replace("$", "<span>$</span>") if text.count("$") > 1 else text


def dest(url):
    """A URL as a link's destination on the pages. A pipe would end its table cell, and a space, a bracket or a
    backslash can end the link early, so those seven are percent encoded and nothing else is touched."""
    return "".join(ENCODED.get(ch, ch) for ch in url)


def plink(text, url):
    return f"[{prose(text)}]({dest(url)})"


def keyed(url):
    """A page of the record as the pages here link it. The record counts a visit by its ?k= key, and record_url in
    the data files carries theirs, ?k=data: a reader who comes from a page here did not come from the data files."""
    return (url[:-len("?k=data")] if url.endswith("?k=data") else re.split(r"[?#]", url, maxsplit=1)[0]) + "?k=repo"


def dashed(r):
    """True for a row whose printed text or links carry an em dash or an en dash. The pages print neither, and one
    row's punctuation must not stop the daily refresh, so such a row is left out of them and named, as the dated
    release's notes do."""
    return any(d in (r.get(k) or "") for k in PRINTED for d in DASHES)


def ahead(r, today):
    """True for a row whose publisher's date has not yet come in New York. The record keeps that date in the data,
    labels the row 'Undated until its day', and prints no date for it until that day; nothing built here may either."""
    return bool(r.get("published_date")) and r["published_date"] > today.isoformat()


def check_ahead(text, rows, today, name):
    """Stops the build when the README prints, as a row's date, a publisher's date that has not come in New York:
    in the data's own words, alone in a table's cell, or as the end of the range the record is listed over. The
    open week's own sentence may name such a day (it runs to its Sunday), and so may a UTC stamp that opens with it."""
    for day in sorted({r["published_date"] for r in rows if ahead(r, today)}):
        if (f'"published_date": "{day}"' in text or f"| {day} |" in text
                or re.search(r"Rows are listed from [^.]*? to " + re.escape(long_date(day)) + ", each", text)):
            sys.exit(f"{name} prints {day}, a publisher's date that has not yet come in New York")


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
    # The example is a row whose day has come: one dated ahead would print, as data, a day the record does not print.
    shown = next((r for r in rows if not ahead(r, today)), None)
    if shown is None:
        sys.exit("every row in data.json carries a publisher's date that has not yet come in New York")
    which = "" if shown is rows[0] else " whose publisher's date has come in New York"
    first = {k: v[:CLIP].rsplit(" ", 1)[0] + "..." if isinstance(v, str) and len(v) > CLIP and " " in v[:CLIP] else v
             for k, v in shown.items()}
    out += ["", f"Example: the first object in `rows`{which}, as `data.json` served it when this file was built on "
                f"{long_date(today)} (ET)"
            + (f". A string longer than {CLIP} characters is cut here and ends in `...`:" if first != shown else ":"),
            "", "```json", json.dumps(first, indent=2, ensure_ascii=False), "```", ""]
    return out


def validate(d, today):
    rows = d["rows"]
    if len(rows) != d["count"]:
        sys.exit(f"data.json count {d['count']} but {len(rows)} rows")
    if not rows:
        sys.exit("data.json has no rows")
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", listed(r) or "") for r in rows):
        sys.exit("a row has no ISO date")
    if not all(r.get("source_url") and r.get("record_url") for r in rows):
        sys.exit("a row has no source_url or record_url")
    # An edition that carries a wire row keeps the publisher's date on it (8 rows in edition 57, 2026-10-24); it is
    # listed by that date, as the record's own openings list it. Both dates on a row no edition carried is refused.
    if any(r.get("published_date") and r.get("edition_date") and not r.get("edition_n") for r in rows):
        sys.exit("a row carries both a publisher's date and an edition's date but no edition number")
    if any(bool(r.get("edition_n")) != bool(r.get("edition_date")) for r in rows):
        sys.exit("a row carries an edition number without its edition's date, or the reverse")
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}T.+Z", r.get("added_at") or "") for r in rows):
        sys.exit("a row has no UTC added_at")
    if not all(r.get("company") and r.get("subject") for r in rows):
        sys.exit("a row has no company or subject")
    if any(r.get("lane") is None and not r.get("edition_n") for r in rows):
        sys.exit("a row in no lane was carried by no edition")
    if not all(re.fullmatch(r"[0-9a-f]{12}", r.get("row_key") or "") for r in rows):
        sys.exit("a row_key is not 12 lowercase hexadecimal characters")
    # A row no edition carried reads 'Published' and its date, except while that date has not come in New York:
    # then it carries the record's own words in its place (the dictionary's date_label), and must not read Published.
    if not all(r["date_label"].startswith(f"Edition {r['edition_n']}, ") if r.get("edition_n")
               else r["date_label"].startswith("Published ") != ahead(r, today) for r in rows):
        sys.exit("a date_label does not match the row's date")
    names = [e.get("name") for e in d.get("dictionary") or []]
    if names != d["fields"] or not all(e.get("description") for e in d["dictionary"]):
        sys.exit("data.json dictionary does not describe exactly its fields")
    lane_words = d["dictionary"][names.index("lane")]["description"]
    if any(r.get("lane") and r["lane"] not in lane_words for r in rows):
        sys.exit("a row's lane is not one the dictionary names")
    if d["license"]["name"] not in SPDX:
        sys.exit(f"license {d['license']['name']!r} has no SPDX id here")


def company_lead(wc):
    """Who shipped the most this week, from the counts alone: the engine's companyLead (dcj-newsletter log.ts), so the
    README and the week page say the same sentence. One company shipped it, or all of them; every company tied names
    them all with 'each'; otherwise the top tier, then the next, named at three or fewer and counted above that."""
    tiers = sorted(set(wc.values()), reverse=True)
    tier = lambda n: sorted((c for c in wc if wc[c] == n), key=lambda c: (c.casefold(), c))
    first = tier(tiers[0])
    if len(wc) == 1:
        return f"{first[0]} shipped {'it' if tiers[0] == 1 else f'all {num(tiers[0])}'}."
    if len(first) == len(wc):
        return f"{and_list(first)} shipped {rows_word(tiers[0])} each."
    each = " each" if len(first) > 1 else ""
    second = tier(tiers[1])
    then = (f"{and_list(second)} with {num(tiers[1])}" + (" each" if len(second) > 1 else "") if len(second) <= 3
            else f"{num(len(second))} companies with {num(tiers[1])} each")
    return f"{and_list(first)} shipped the most, {rows_word(tiers[0])}{each}, then {then}."


def week_paragraph(n_rows, n_pub, wc, monday, sunday, built_on):
    """The README's opening sentence for the newest week: every word a count, a company's name or a date."""
    text = (f"{rows_word(n_rows)} {'is' if n_rows == 1 else 'are'} listed for {span(monday, sunday)} in The Deploy Log, from "
            f"{num(len(wc))} {'company' if len(wc) == 1 else 'companies'}. {company_lead(wc)} {num(n_pub)} "
            f"{'carries' if n_pub == 1 else 'carry'} a publisher's date and {num(n_rows - n_pub)} "
            f"{'is' if n_rows - n_pub == 1 else 'are'} placed by their edition.")
    if built_on:
        text += (f" The week runs to Sunday, {long_date(sunday)}, and was still in progress when this file was "
                 f"built on {long_date(built_on)} (ET).")
    return text


def company_paragraph(name, n, dates, late=0):
    """A company page's opening: every word a count, the company's name or a date. dates are the publisher's dates
    among its n rows that have come in New York, oldest first; late is how many more have not. Those are counted,
    since the rows carry them, and never printed: a day or a range here is one that has come."""
    k = len(dates) + late
    text = f"{rows_word(n)} in The Deploy Log {'is' if n == 1 else 'are'} filed under {prose(name)}."
    if not k:
        return text + (" It is placed by its edition." if n == 1 else " Every one is placed by its edition.")
    if n == 1 and late:
        return text + " It carries a publisher's date, which has not yet come in New York."
    if not dates:
        when = ""
    elif dates[0] != dates[-1]:
        when = f", from {long_date(dates[0])} to {long_date(dates[-1])}"
    elif late:
        when = f", {num(len(dates))} on {long_date(dates[0])}"  # 'all on' would be untrue of the dates still to come
    else:
        when = f", {long_date(dates[0])}" if k == 1 else f", all on {long_date(dates[0])}"
    tail = ("" if not late else " That date has not yet come in New York." if k == 1
            else f" {num(late)} of those dates {'has' if late == 1 else 'have'} not yet come in New York.")
    if k == n:
        return text + f" {'It carries' if n == 1 else 'Every one carries'} a publisher's date{when}.{tail}"
    rest = "1 is placed by its edition" if n - k == 1 else f"{num(n - k)} are placed by their edition"
    return (text + f" {num(k)} {'carries' if k == 1 else 'carry'} a publisher's date{when}{',' if when else ''} "
                   f"and {rest}.{tail}")


def placed_line(n, where=""):
    """What stands over a table of rows no publisher dated: an edition's Saturday is not the day a thing shipped."""
    if n == 1:
        return (f"1 row carries no publisher's date in the record and is listed{where} by the date of the edition "
                f"that carried it, which is not the day it shipped.")
    return (f"{num(n)} rows carry no publisher's date in the record and are listed{where} by the date of the edition "
            f"that carried them, which is not the day they shipped.")


def ahead_line(n, page=False):
    """How many rows carry a publisher's date that has not come: over their table on a page, or in the README's
    paragraph about the record, where it is left out when there is none."""
    if not n:
        return ""
    lead = f"{rows_word(n)} {'carries' if n == 1 else 'carry'} a publisher's date that has not yet come in New York"
    if page:
        return (f"{lead}. The record prints no date for {'it' if n == 1 else 'them'} until that day, and neither "
                f"does this page.")
    return f"{lead}, and {'is' if n == 1 else 'are'} listed from that day."


def left_line(keys, more=False):
    """A page that prints fewer rows than its opening counts says which, so a reader can make the two numbers meet.
    more is for a week's rows under a company name that carries a dash: its opening can neither name nor rank that
    company, so it counts them here instead, and the week's rows still sum."""
    named = and_list([f"`{k}`" for k in keys])
    if more:
        # One clause for where the row counts and one for where it is not, so the sentence does not say both at once
        # (review round 2): the index's Rows cell for the week holds it, this page's tables do not.
        return (f"{'1 more row counts' if len(keys) == 1 else f'{num(len(keys))} more rows count'} in this week but "
                f"{'is' if len(keys) == 1 else 'are'} left out of this page for a dash in "
                f"{'its' if len(keys) == 1 else 'their'} company's name, and {'is' if len(keys) == 1 else 'are'} in "
                f"`data.csv` as {named}.")
    if len(keys) == 1:
        return f"1 of these rows is left out of this page for a dash in its text, and is in `data.csv` as {named}."
    return (f"{num(len(keys))} of these rows are left out of this page for a dash in their text, and are in "
            f"`data.csv` as {named}.")


def index_lead(n, paged, things, thing, order, rest):
    """An index's opening: how many of the record's weeks or companies have a page there, and so a page here."""
    if n == 1:
        return f"The 1 {thing} has a page there, and it is listed here."
    if paged == n:
        return f"Each of the {num(n)} {things} has a page there, and each is listed here, {order}."
    has = ("1 has a page there, and it is listed here" if paged == 1
           else f"{num(paged)} have a page there, and each is listed here, {order}")
    return f"Of the {num(n)} {things}, {has}. The rows of {rest} are in `data.csv`."


def pages_line(wk, paged):
    """The README's one paragraph about the pages beside it: each link only when this build wrote its file."""
    here = [f"[{label}]({path})" for label, path in (("week by week", "weeks/README.md"),
                                                     ("company by company", "companies/README.md")) if path in paged]
    if not here:
        return None
    this = f"weeks/{wk}.md"
    return ((f"Every row of this week, with its source: [{this}]({this}). " if this in paged else "")
            + f"The record {' and '.join(here)}.")


def files_lines(paged):
    """The README's Files bullets for the two folders, each only when this build wrote pages into it."""
    how = "every row with its source and its page in the record"
    weeks = [f"- `weeks/`: one page per week the record lists, {how}"] if "weeks/README.md" in paged else []
    return weeks + ([f"- `companies/`: one page per company the record lists, {'the same way' if weeks else how}"]
                    if "companies/README.md" in paged else [])


def week_days(wk):
    monday = datetime.date.fromisocalendar(int(wk[:4]), int(wk[6:]), 1)
    return monday, monday + datetime.timedelta(days=6)


def company_files(companies, by_company):
    """The page each company gets here, named by the last segment of its hub URL, the name the record files it
    under. Two companies with one segment both carry their hub's id too, and so does a segment that would stand
    in for the folder's index."""
    parts = {}
    for c, url in companies.items():
        # A name that carries a dash has every row left out (dashed), so there is no page for it to head.
        if c in by_company and not any(d in c for d in DASHES):
            m = HUB.fullmatch(url)
            if not m:
                sys.exit(f"{url} is not a company page as the record links them: company/<12 hexadecimal "
                         f"characters>/<name>/")
            parts[c] = m.groups()
    taken = Counter(slug for _, slug in parts.values())
    files = {c: f"{slug}-{key}.md" if taken[slug] > 1 or slug == "readme" else f"{slug}.md"
             for c, (key, slug) in parts.items()}
    if len(set(files.values())) != len(files):
        sys.exit("two companies would share one page under companies/")
    return files


def table(cols, lines, right=()):
    rule = "".join("---:|" if i in right else "---|" for i in range(len(cols)))
    return ["| " + " | ".join(cols) + " |", "|" + rule, *lines, ""]


def table_lines(text):
    """The rows a page's tables print: every line that opens with a pipe, less each table's header and its rule."""
    lines = text.split("\n")
    rule = lambda s: re.fullmatch(r"\|[-:|]+\|", s) is not None
    return [s for i, s in enumerate(lines)
            if s.startswith("|") and not rule(s) and not (i + 1 < len(lines) and rule(lines[i + 1]))]


def reconcile(out, rows, cfile, today):
    """Every sum the pages print, read back off their text before a file is written: a page prints each of its
    rows once or names it as left out, an index's Rows cell is its page's count, a link between pages lands on a
    page this build wrote, nothing carries a dash, and no day that has not come in New York is printed as a day
    heading, in a date cell or in a company's opening."""
    for path in out:
        # main() writes these paths and clears what it did not write, so none may reach outside the two folders.
        if not re.fullmatch(r"(weeks|companies)/[A-Za-z0-9][A-Za-z0-9-]*\.md", path):
            sys.exit(f"{path} is not a page under weeks/ or companies/")
    own = {f"companies/{f}": [r for r in rows if r["company"] == c] for c, f in cfile.items()}
    own.update({p: [r for r in rows if iso_week(listed(r)) == p[6:-3]]
                for p in out if p.startswith("weeks/") and p != "weeks/README.md"})
    late = sorted({r["published_date"] for r in rows if ahead(r, today)})
    for path, text in out.items():
        if any(d in text for d in DASHES):
            sys.exit(f"{path} would carry an em dash or an en dash")
        lines = text.split("\n")
        for day in late:
            # A week's own range may name such a day (it runs to its Sunday); a heading, a cell or a company's
            # opening that does is a row's date, which the record does not print yet.
            if (any(s.startswith("## ") and long_date(day) in s or s.startswith("|") and f"| {day} |" in s
                    for s in lines) or path.startswith("companies/") and long_date(day) in lines[2]):
                sys.exit(f"{path} prints {day}, a publisher's date that has not yet come in New York")
        folder = path.split("/")[0]
        # prose() escapes a row's own brackets, so an unescaped link to a .md file is one this build made.
        for target in re.findall(r"(?<!\\)\]\(([^):\s]+\.md)\)", text):
            if posixpath.normpath(f"{folder}/{target}") not in out:
                sys.exit(f"{path} links {target}, a page this build did not write")
        printed = table_lines(text)
        if path in own:
            gone = sum(1 for r in own[path] if dashed(r))
            if len(printed) + gone != len(own[path]):
                sys.exit(f"{path} prints {len(printed)} rows and leaves out {gone}, the record holds "
                         f"{len(own[path])}")
            continue
        said = {}
        for line in printed:
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip("|"))]
            m = re.match(r"\[.*\]\(([^):\s]+\.md)\)", cells[0])
            said[f"{folder}/{m.group(1)}" if m else line] = cells[2 if folder == "weeks" else 1]
        want = {p: num(len(mine)) for p, mine in own.items() if p.startswith(folder + "/")}
        if said != want:
            off = sorted(p for p in set(said) | set(want) if said.get(p) != want.get(p))
            sys.exit(f"{path} and its pages disagree on the rows of {len(off)}: {', '.join(off[:5])}")


def pages(rows, locs, companies, today):
    """The record as pages a reader opens in the repository, as {path: text}, and the row_keys left out of them.
    One page per ISO week and one per company, each only where the sitemap lists that page of the record, and an
    index of each. A row no publisher dated is never listed under a day: it sits under its edition, apart. Nor is
    a row whose publisher's date has not come in New York: it sits under the record's own words for it, undated."""
    by_company = Counter(r["company"] for r in rows)
    by_week = Counter(iso_week(listed(r)) for r in rows)
    cfile = company_files(companies, by_company)
    nameable = lambda r: not any(d in r["company"] for d in DASHES)
    # Zero padded, so this is oldest first. A week with no row whose company can be named has no opening to print.
    weeks = sorted(w for w in {iso_week(listed(r)) for r in rows if nameable(r)} if f"{BASE}week/{w}/" in locs)
    newest = lambda day: -datetime.date.fromisoformat(day).toordinal()
    by_name = lambda r: (r["company"].casefold(), r["company"], r["subject"], r["row_key"])
    firm = lambda r: (plink(r["company"], f"../companies/{cfile[r['company']]}") if r["company"] in cfile
                      else prose(r["company"]))
    cells = lambda r: " | ".join((plink(r["subject"], keyed(r["record_url"])),
                                  prose(r.get("what_shipped") or r["subject"]),
                                  plink(r.get("source") or r["source_url"], r["source_url"])))
    edition = lambda r: f"Edition {r['edition_n']}, {r['edition_date']}"
    out = {}

    def parts(mine):
        """A page's rows as it prints them: those under a publisher's date that has come, those whose date has
        not, those placed by their edition, and the keys of the rows it leaves out."""
        shown = [r for r in mine if not dashed(r)]
        return ([r for r in shown if r.get("published_date") and not ahead(r, today)],
                [r for r in shown if ahead(r, today)], [r for r in shown if not r.get("published_date")],
                [r["row_key"] for r in mine if dashed(r)])

    for i, wk in enumerate(weeks):
        monday, sunday = week_days(wk)
        every = [r for r in rows if iso_week(listed(r)) == wk]
        mine = [r for r in every if nameable(r)]
        more = [r["row_key"] for r in every if not nameable(r)]
        dated, late, placed, left = parts(mine)
        same = "The same rows are on " + plink("this week's page of the record", keyed(f"{BASE}week/{wk}/")) + "."
        # The nearest week with a page here, which is not always the week next to this one.
        for label, near in (("Before it", weeks[i - 1:i]), ("After it", weeks[i + 1:i + 2])):
            if near:
                same += f" {label}: {plink(span(*week_days(near[0])), near[0] + '.md')}."
        text = [f"# What shipped in AI, week of {long_date(monday)}", "",
                week_paragraph(len(mine), sum(1 for r in mine if r.get("published_date")),
                               Counter(prose(r["company"]) for r in mine), monday, sunday,
                               today if monday <= today <= sunday else None), ""]
        text += ([left_line(left), ""] if left else []) + ([left_line(more, True), ""] if more else []) + [same, ""]
        for day in sorted({r["published_date"] for r in dated}, reverse=True):
            d = datetime.date.fromisoformat(day)
            text += [f"## {d:%A}, {long_date(d)}", ""] + table(("Company",) + ROW, [
                f"| {firm(r)} | {cells(r)} |" for r in sorted((r for r in dated if r["published_date"] == day),
                                                              key=by_name)])
        if late:
            text += ["## Undated until its day", "", ahead_line(len(late), True), ""] + table(
                ("Company",) + ROW, [f"| {firm(r)} | {cells(r)} |" for r in sorted(late, key=by_name)])
        if placed:
            placed.sort(key=lambda r: (newest(r["edition_date"]),) + by_name(r))
            text += ["## Placed by their edition", "", placed_line(len(placed), " in this week"), ""] + table(
                ("Edition", "Company") + ROW, [f"| {edition(r)} | {firm(r)} | {cells(r)} |" for r in placed])
        out[f"weeks/{wk}.md"] = "\n".join(text)

    for c, file in cfile.items():
        mine = [r for r in rows if r["company"] == c]
        dated, late, placed, left = parts(mine)
        come = sorted(r["published_date"] for r in mine if r.get("published_date") and not ahead(r, today))
        text = [f"# {prose(c)} in The Deploy Log", "",
                company_paragraph(c, len(mine), come, sum(1 for r in mine if ahead(r, today))), ""]
        text += ([left_line(left), ""] if left else []) + [
            f"The same rows are on {plink(f'the {c} page of the record', keyed(companies[c]))}.", ""]
        for month in sorted({r["published_date"][:7] for r in dated}, reverse=True):
            text += [f"## {datetime.date.fromisoformat(month + '-01'):%B %Y}", ""] + table(("Date",) + ROW, [
                f"| {r['published_date']} | {cells(r)} |"
                for r in sorted((r for r in dated if r["published_date"][:7] == month),
                                key=lambda r: (newest(r["published_date"]), r["subject"], r["row_key"]))])
        if late:
            text += ["## Undated until its day", "", ahead_line(len(late), True), ""] + table(
                ROW, [f"| {cells(r)} |" for r in sorted(late, key=lambda r: (r["subject"], r["row_key"]))])
        if placed:
            placed.sort(key=lambda r: (newest(r["edition_date"]), r["subject"], r["row_key"]))
            text += ["## Placed by their edition", "", placed_line(len(placed)), ""] + table(
                ("Edition",) + ROW, [f"| {edition(r)} | {cells(r)} |" for r in placed])
        out[f"companies/{file}"] = "\n".join(text)

    if weeks:
        pub_week = Counter(iso_week(r["published_date"]) for r in rows if r.get("published_date"))
        lines = []
        for wk in reversed(weeks):
            monday, sunday = week_days(wk)
            lines.append(f"| {plink(wk, wk + '.md')}{' (in progress)' if monday <= today <= sunday else ''} | "
                         f"{monday.isoformat()} to {sunday.isoformat()} | {num(by_week[wk])} | {num(pub_week[wk])} | "
                         f"{plink('page', keyed(f'{BASE}week/{wk}/'))} |")
        rest = "the other week" if len(by_week) - len(weeks) == 1 else "the other weeks"
        out["weeks/README.md"] = "\n".join(
            ["# The Deploy Log, week by week", "",
             index_lead(len(by_week), len(weeks), "ISO weeks that hold a row in the record",
                        "ISO week that holds a row in the record", "newest first", rest), ""]
            + table(("Week", "Monday to Sunday", "Rows", "With a publisher's date", "In the record"), lines, (2, 3)))
    if cfile:
        lines = []
        for c in sorted(cfile, key=lambda c: (-by_company[c], c.casefold(), c)):
            mine = [r for r in rows if r["company"] == c and r.get("published_date")]
            come = sorted(r["published_date"] for r in mine if not ahead(r, today))
            first, last = (come[0], come[-1]) if come else ("none", "none")
            lines.append(f"| {plink(c, cfile[c])} | {num(by_company[c])} | {num(len(mine))} | {first} | {last} | "
                         f"{plink('page', keyed(companies[c]))} |")
        rest = "the other one" if len(by_company) - len(cfile) == 1 else "the others"
        out["companies/README.md"] = "\n".join(
            ["# The Deploy Log, company by company", "",
             index_lead(len(by_company), len(cfile), "companies the record files a row under",
                        "company the record files a row under", "by rows, then by name", rest), ""]
            + table(("Company", "Rows", "With a publisher's date", "First", "Latest", "In the record"), lines,
                    (1, 2)))
    reconcile(out, rows, cfile, today)
    return out, [r["row_key"] for r in rows if dashed(r)]


def write_pages(made, root="."):
    """Writes the pages, then removes each .md in weeks/ and companies/ that this build did not write: a week or a
    company that left the sitemap has no page here either. Nothing else is removed."""
    for folder in ("weeks", "companies"):
        # Made even when empty: the workflow stages both folders by name, and git refuses one that is not there.
        os.makedirs(os.path.join(root, folder), exist_ok=True)
    for path, text in made.items():
        with open(os.path.join(root, *path.split("/")), "wb") as f:
            f.write(text.encode("utf-8"))
    for folder in ("weeks", "companies"):
        for name in os.listdir(os.path.join(root, folder)):
            full = os.path.join(root, folder, name)
            if name.endswith(".md") and f"{folder}/{name}" not in made and os.path.isfile(full):
                os.remove(full)


def selftest_pages():
    """The pages under weeks/ and companies/, built from rows made here, no network: what a reader would see wrong
    in a cell, an opening at a count of one, a link, a file name, a sum, or a file left behind."""
    def row(n, company, subject, pub=None, ed=None, shipped=None, source="Src", url=None):
        key = f"{n:012x}"
        return {"row_key": key, "company": company, "subject": subject, "published_date": pub,
                "what_shipped": f"{subject} shipped." if shipped is None else shipped, "source": source,
                "edition_n": ed and ed[0], "edition_date": ed and ed[1], "source_url": f"http://example.com/{n}",
                "record_url": url or f"{BASE}{key}/x/?k=data"}

    def stops(fn):
        try:
            fn()
        except SystemExit as e:
            return str(e.code)
        return "did not stop"

    # Three weeks hold a row and the sitemap lists two; four companies hold a row and three have a hub, two of them
    # under one last segment; Ghost has a hub and no row. Row 5 carries an en dash, row 2 a key that is not ?k=data.
    rows = [row(1, "Beta", "Beta one", "2026-11-04", shipped="Beta one costs $5/$6 per 1M tokens."),
            row(2, "alpha", "Small alpha", "2026-11-04", url=f"{BASE}000000000002/x/?ref=1"),
            row(3, "Alpha", "Alpha three", "2026-11-03", shipped="", source=""),
            row(4, "Gamma", "Gamma four", ed=(59, "2026-11-07")),
            row(5, "Alpha", f"Alpha {DASHES[1]} five", "2026-11-04"),
            row(6, "Alpha", "Alpha six", "2026-10-27"),
            row(7, "Alpha", "Alpha seven", "2026-10-13"),
            row(8, "Alpha", "Alpha nine", ed=(56, "2026-10-17")),
            row(9, "Alpha", "Alpha eight", ed=(56, "2026-10-17"))]
    hubs_ = {"Alpha": f"{BASE}company/aaaaaaaaaaaa/alpha/", "Beta": f"{BASE}company/bbbbbbbbbbbb/same/",
             "Gamma": f"{BASE}company/cccccccccccc/same/", "Ghost": f"{BASE}company/dddddddddddd/ghost/"}
    locs = {BASE, f"{BASE}week/2026-W45/", f"{BASE}week/2026-W42/"} | set(hubs_.values())
    today = datetime.date(2026, 11, 4)
    try:
        made, left = pages(rows, locs, hubs_, today)
    except SystemExit as e:
        return [("the pages build from the rows made here and reconcile", False, str(e.code))]
    w45, w42, alpha = (made.get(p, "") for p in ("weeks/2026-W45.md", "weeks/2026-W42.md", "companies/alpha.md"))
    heads = lambda text: re.findall(r"^## (.+)$", text, flags=re.M)
    rec = lambda n: f"{BASE}{n:012x}/x/?k=repo"
    site = [u for text in made.values() for u in re.findall(r"\]\((https://deployedbyai\.com/[^)\s]*)\)", text)]
    cfile = company_files(hubs_, Counter(r["company"] for r in rows))
    nov4 = ["2026-11-04"]
    filed = "in The Deploy Log are filed under X."

    spec = prose("a|b [x] *y* _z_ ~w~ <t> & $5/$6 and ($2)$")
    lone = prose("a\\b `c`  one $5\n&  up")
    url = plink("a_b", "http://x.example/y_z?q=$1&r=$2")
    keys = [keyed(f"{BASE}abc/x/?k=data"), keyed(f"{BASE}abc/x/?ref=1#top"), keyed(f"{BASE}week/2026-W45/")]
    checks = [
        ("prose escapes what would redraw a cell and wraps each dollar sign when the text holds two or more",
         spec == "a\\|b \\[x\\] \\*y\\* \\_z\\_ \\~w\\~ &lt;t&gt; &amp; <span>$</span>5/<span>$</span>6 and "
                 "(<span>$</span>2)<span>$</span>", spec),
        ("prose keeps one dollar sign bare, escapes a backslash and a backtick, and closes up white space",
         lone == "a\\\\b \\`c\\` one $5 &amp; up", lone),
        ("a link's text goes through prose and its URL is untouched", url == "[a\\_b](http://x.example/y_z?q=$1&r=$2)", url),
        ("a record URL is keyed ?k=repo, in place of ?k=data, of any other query, or of none",
         keys == [f"{BASE}abc/x/?k=repo", f"{BASE}abc/x/?k=repo", f"{BASE}week/2026-W45/?k=repo"], keys),
    ]
    for name, n, dates, want in (
            ("some dated and some placed", 177, ["2025-03-03"] + ["2026-01-05"] * 122 + nov4,
             "177 rows in The Deploy Log are filed under Anthropic. 124 carry a publisher's date, from March 3, 2025 "
             "to November 4, 2026, and 53 are placed by their edition."),
            ("every row dated", 3, ["2026-11-02", "2026-11-03"] + nov4,
             f"3 rows {filed} Every one carries a publisher's date, from November 2, 2026 to November 4, 2026."),
            ("every row dated, on one day", 2, nov4 * 2,
             f"2 rows {filed} Every one carries a publisher's date, all on November 4, 2026."),
            ("one row, dated", 1, nov4,
             "1 row in The Deploy Log is filed under X. It carries a publisher's date, November 4, 2026."),
            ("no row dated", 2, [], f"2 rows {filed} Every one is placed by its edition."),
            ("one row, placed", 1, [], "1 row in The Deploy Log is filed under X. It is placed by its edition."),
            ("one dated among several", 3, nov4,
             f"3 rows {filed} 1 carries a publisher's date, November 4, 2026, and 2 are placed by their edition."),
            ("one dated and one placed", 2, nov4,
             f"2 rows {filed} 1 carries a publisher's date, November 4, 2026, and 1 is placed by its edition."),
            ("several dated on one day and one placed", 3, nov4 * 2,
             f"3 rows {filed} 2 carry a publisher's date, all on November 4, 2026, and 1 is placed by its edition.")):
        got = company_paragraph("Anthropic" if n == 177 else "X", n, dates)
        checks.append((f"a company page opens right with {name}", got == want, got))

    one_placed = ("1 row carries no publisher's date in the record and is listed in this week by the date of the "
                  "edition that carried it, which is not the day it shipped.")
    two_placed = ("2 rows carry no publisher's date in the record and are listed by the date of the edition that "
                  "carried them, which is not the day they shipped.")
    same45 = (f"The same rows are on [this week's page of the record]({BASE}week/2026-W45/?k=repo). Before it: "
              f"[October 12 to 18, 2026](2026-W42.md).")
    same42 = (f"The same rows are on [this week's page of the record]({BASE}week/2026-W42/?k=repo). After it: "
              f"[November 2 to 8, 2026](2026-W45.md).")
    gone = "1 of these rows is left out of this page for a dash in its text, and is in `data.csv` as `000000000005`."
    weeks_index = "\n".join([
        "# The Deploy Log, week by week", "",
        "Of the 3 ISO weeks that hold a row in the record, 2 have a page there, and each is listed here, newest "
        "first. The rows of the other week are in `data.csv`.", "",
        "| Week | Monday to Sunday | Rows | With a publisher's date | In the record |", "|---|---|---:|---:|---|",
        f"| [2026-W45](2026-W45.md) (in progress) | 2026-11-02 to 2026-11-08 | 5 | 4 | [page]({BASE}week/2026-W45/?k=repo) |",
        f"| [2026-W42](2026-W42.md) | 2026-10-12 to 2026-10-18 | 3 | 1 | [page]({BASE}week/2026-W42/?k=repo) |", ""])
    companies_index = "\n".join([
        "# The Deploy Log, company by company", "",
        "Of the 4 companies the record files a row under, 3 have a page there, and each is listed here, by rows, "
        "then by name. The rows of the other one are in `data.csv`.", "",
        "| Company | Rows | With a publisher's date | First | Latest | In the record |", "|---|---:|---:|---|---|---|",
        f"| [Alpha](alpha.md) | 6 | 4 | 2026-10-13 | 2026-11-04 | [page]({BASE}company/aaaaaaaaaaaa/alpha/?k=repo) |",
        f"| [Beta](same-bbbbbbbbbbbb.md) | 1 | 1 | 2026-11-04 | 2026-11-04 | [page]({BASE}company/bbbbbbbbbbbb/same/?k=repo) |",
        f"| [Gamma](same-cccccccccccc.md) | 1 | 0 | none | none | [page]({BASE}company/cccccccccccc/same/?k=repo) |", ""])
    all_weeks = index_lead(60, 60, "ISO weeks that hold a row in the record", "", "newest first", "")
    one_paged = index_lead(147, 1, "companies the record files a row under", "", "by rows, then by name", "the others")
    one_week = index_lead(1, 1, "", "ISO week that holds a row in the record", "newest first", "")
    both = pages_line("2026-W45", made)
    no_week = pages_line("2026-W44", made)
    cut = "\n".join(s for s in w45.split("\n") if "Gamma four" not in s)
    off = made["weeks/README.md"].replace("| 5 | 4 |", "| 6 | 4 |")
    lost = w45.replace("(2026-W42.md)", "(2026-W43.md)")
    checks += [
        ("placed rows read right at a count of one, in a week", placed_line(1, " in this week") == one_placed,
         placed_line(1, " in this week")),
        ("placed rows read right above one, on a company page", placed_line(2) == two_placed, placed_line(2)),
        ("a week and a company the sitemap lists get a page, a company without a row or a hub and a week without a "
         "page get none, and two companies under one last segment both carry their hub's id",
         sorted(made) == ["companies/README.md", "companies/alpha.md", "companies/same-bbbbbbbbbbbb.md",
                          "companies/same-cccccccccccc.md", "weeks/2026-W42.md", "weeks/2026-W45.md",
                          "weeks/README.md"], sorted(made)),
        ("a week's days run newest first and its undated rows sit apart, under their edition",
         heads(w45) == ["Wednesday, November 4, 2026", "Tuesday, November 3, 2026", "Placed by their edition"],
         heads(w45)),
        ("a week with one placed row says so in the singular, over that row and its edition",
         one_placed in w45.split("\n") and f"| Edition 59, 2026-11-07 | [Gamma](../companies/same-cccccccccccc.md) "
         f"| [Gamma four]({rec(4)}) | Gamma four shipped. | [Src](http://example.com/4) |" in w45.split("\n"),
         w45.split("## Placed by their edition")[-1]),
        ("a week names the nearest earlier week that has a page here, and no later one when none has",
         same45 in w45.split("\n"), [s for s in w45.split("\n") if s.startswith("The same rows")]),
        ("the oldest week with a page names only the week after it", same42 in w42.split("\n"),
         [s for s in w42.split("\n") if s.startswith("The same rows")]),
        ("a company with a page here is linked to it, and its two dollar signs are wrapped",
         f"| [Beta](../companies/same-bbbbbbbbbbbb.md) | [Beta one]({rec(1)}) | Beta one costs <span>$</span>5/"
         f"<span>$</span>6 per 1M tokens. | [Src](http://example.com/1) |" in w45.split("\n"),
         [s for s in w45.split("\n") if "Beta one" in s]),
        ("a company with no page here is named without a link, and a record URL keyed otherwise is keyed ?k=repo",
         f"| alpha | [Small alpha]({rec(2)}) | Small alpha shipped. | [Src](http://example.com/2) |" in w45.split("\n"),
         [s for s in w45.split("\n") if "Small alpha" in s]),
        ("a row with no sentence prints its subject, and one with no source name prints its source URL",
         f"| [Alpha](../companies/alpha.md) | [Alpha three]({rec(3)}) | Alpha three | [http://example.com/3]"
         f"(http://example.com/3) |" in w45.split("\n"), [s for s in w45.split("\n") if "Alpha three" in s]),
        ("every link to deployedbyai.com on every page ends ?k=repo and none carries ?k=data",
         len(site) == 24 and all(u.endswith("?k=repo") for u in site) and not any("?k=data" in t for t in made.values()),
         [u for u in site if not u.endswith("?k=repo")] or len(site)),
        ("a row whose text carries a dash is left out and named, and its week still counts it",
         left == ["000000000005"] and w45.split("\n")[2].startswith("5 rows are listed") and gone in w45.split("\n")
         and len(table_lines(w45)) == 4 and not any(d in t for t in made.values() for d in DASHES),
         (left, w45.split("\n")[2:5], len(table_lines(w45)))),
        ("a company page counts a left out row, says so, and lists its months and its dates newest first",
         alpha.split("\n")[2] == "6 rows in The Deploy Log are filed under Alpha. 4 carry a publisher's date, from "
         "October 13, 2026 to November 4, 2026, and 2 are placed by their edition." and gone in alpha.split("\n")
         and heads(alpha) == ["November 2026", "October 2026", "Placed by their edition"]
         and [s.split(" | ")[0] for s in table_lines(alpha)] == [
             "| 2026-11-03", "| 2026-10-27", "| 2026-10-13", "| Edition 56, 2026-10-17", "| Edition 56, 2026-10-17"]
         and alpha.index("Alpha eight") < alpha.index("Alpha nine") and two_placed in alpha.split("\n")
         and f"The same rows are on [the Alpha page of the record]({BASE}company/aaaaaaaaaaaa/alpha/?k=repo)."
         in alpha.split("\n"), alpha),
        ("the week index counts each week's rows, marks the week in progress and lists newest first",
         made.get("weeks/README.md") == weeks_index, made.get("weeks/README.md")),
        ("the company index orders by rows, then by name, and prints none where no row is dated",
         made.get("companies/README.md") == companies_index, made.get("companies/README.md")),
        ("an index where every week has a page says each",
         all_weeks == "Each of the 60 ISO weeks that hold a row in the record has a page there, and each is listed "
                      "here, newest first.", all_weeks),
        ("an index with one page says 'has' and 'it'",
         one_paged == "Of the 147 companies the record files a row under, 1 has a page there, and it is listed here. "
                      "The rows of the others are in `data.csv`.", one_paged),
        ("an index of a record that holds one week reads in the singular",
         one_week == "The 1 ISO week that holds a row in the record has a page there, and it is listed here.", one_week),
        ("the README points at this week's page and both indexes when all three were written",
         both == "Every row of this week, with its source: [weeks/2026-W45.md](weeks/2026-W45.md). The record "
                 "[week by week](weeks/README.md) and [company by company](companies/README.md).", both),
        ("the README leaves out a week page that was not written, and the paragraph when no page was",
         no_week == "The record [week by week](weeks/README.md) and [company by company](companies/README.md)."
         and pages_line("2026-W45", {}) is None and pages_line("2026-W45", {"companies/README.md"})
         == "The record [company by company](companies/README.md).", (no_week, pages_line("2026-W45", {}))),
        ("the README's Files list names each folder only when it holds pages",
         files_lines(made) == ["- `weeks/`: one page per week the record lists, every row with its source and its "
                               "page in the record", "- `companies/`: one page per company the record lists, the "
                               "same way"] and files_lines({}) == []
         and files_lines({"companies/README.md"}) == ["- `companies/`: one page per company the record lists, every "
                                                      "row with its source and its page in the record"],
         files_lines(made)),
        ("a company whose hub's last segment would stand in for the index carries its id",
         company_files({"ReadMe": f"{BASE}company/eeeeeeeeeeee/readme/"}, {"ReadMe": 1})
         == {"ReadMe": "readme-eeeeeeeeeeee.md"},
         company_files({"ReadMe": f"{BASE}company/eeeeeeeeeeee/readme/"}, {"ReadMe": 1})),
        ("a company hub URL of another shape stops the build before a file is named after it",
         "is not a company page" in stops(lambda: company_files({"A": f"{BASE}company/../x/"}, {"A": 1})),
         stops(lambda: company_files({"A": f"{BASE}company/../x/"}, {"A": 1}))),
        ("a page that prints one row fewer than the record holds stops the build",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": cut}, rows, cfile, today))
         == "weeks/2026-W45.md prints 3 rows and leaves out 1, the record holds 5",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": cut}, rows, cfile, today))),
        ("an index whose Rows cell is not its page's count stops the build",
         stops(lambda: reconcile({**made, "weeks/README.md": off}, rows, cfile, today))
         == "weeks/README.md and its pages disagree on the rows of 1: weeks/2026-W45.md",
         stops(lambda: reconcile({**made, "weeks/README.md": off}, rows, cfile, today))),
        ("a link to a page this build did not write stops the build",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": lost}, rows, cfile, today))
         == "weeks/2026-W45.md links 2026-W43.md, a page this build did not write",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": lost}, rows, cfile, today))),
        ("a dash that reaches a page stops the build",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": w45 + DASHES[0]}, rows, cfile, today))
         == "weeks/2026-W45.md would carry an em dash or an en dash",
         stops(lambda: reconcile({**made, "weeks/2026-W45.md": w45 + DASHES[0]}, rows, cfile, today))),
        ("a path outside weeks/ and companies/ stops the build",
         stops(lambda: reconcile({**made, "weeks/../README.md": "x"}, rows, cfile, today))
         == "weeks/../README.md is not a page under weeks/ or companies/",
         stops(lambda: reconcile({**made, "weeks/../README.md": "x"}, rows, cfile, today))),
    ]

    # Rows dated ahead: today is 2026-11-04 in New York, and row 12 carries 2026-11-05.
    def labelled(*pairs):
        rs = [dict(row(n, "Alpha", f"Alpha {n}", pub), lane="Tools and products", date_label=label,
                   added_at="2026-11-05T02:10:57.320Z") for n, (pub, label) in enumerate(pairs, 1)]
        return {"url": BASE, "count": len(rs), "rows": rs, "fields": list(rs[0]), "license": {"name": "CC BY 4.0"},
                "dictionary": [{"name": k, "description": "Tools and products" if k == "lane" else "x"}
                               for k in rs[0]]}

    labels = [stops(lambda: validate(labelled((pub, label)), today)) for pub, label in (
        ("2026-11-05", "Undated until its day"), ("2026-11-04", "Published Wednesday 4 Nov 2026"),
        ("2026-11-05", "Published Thursday 5 Nov 2026"), ("2026-11-04", "Undated until its day"))]
    refused = "a date_label does not match the row's date"
    late_rows = [row(11, "Alpha", "Alpha come", "2026-11-03"), row(12, "Alpha", "Alpha late", "2026-11-05"),
                 row(13, "Alpha", "Alpha placed", ed=(59, "2026-11-07")), row(14, "Beta", "Beta come", "2026-11-04"),
                 row(15, "Alpha", "Alpha older", "2026-10-13")]
    lfile = company_files(hubs_, Counter(r["company"] for r in late_rows))
    try:
        late = pages(late_rows, locs, hubs_, today)[0]
        only = pages([row(21, "Beta", "Beta next", "2026-11-09")], {BASE, f"{BASE}week/2026-W46/"}, {}, today)[0]
    except SystemExit as e:
        return checks + [("the pages build from rows dated ahead and reconcile", False, str(e.code))]
    l45, lalpha, w46 = late["weeks/2026-W45.md"], late["companies/alpha.md"], only["weeks/2026-W46.md"]
    one_ahead = ("1 row carries a publisher's date that has not yet come in New York. The record prints no date for "
                 "it until that day, and neither does this page.")
    unprinted = lambda text: "2026-11-05" not in text and "November 5, 2026" not in text
    guard = [stops(lambda: reconcile({**late, path: text}, late_rows, lfile, today)) for path, text in (
        ("weeks/2026-W45.md", l45.replace("## Undated until its day", "## Thursday, November 5, 2026")),
        ("companies/alpha.md", lalpha.replace("| [Alpha late]", "| 2026-11-05 | [Alpha late]")),
        ("companies/README.md", late["companies/README.md"].replace("| 2026-11-03 |", "| 2026-11-05 |")),
        ("companies/alpha.md", lalpha.replace("to November 3, 2026,", "to November 5, 2026,")))]
    checks += [
        ("a row dated ahead must read 'Undated until its day', a row whose day has come must read 'Published', and "
         "either the other way stops the build", labels == ["did not stop", "did not stop", refused, refused], labels),
        ("a week lists a row dated ahead under no day, in its own section, and still counts it in its opening",
         heads(l45) == ["Wednesday, November 4, 2026", "Tuesday, November 3, 2026", "Undated until its day",
                        "Placed by their edition"] and unprinted(l45) and one_ahead in l45.split("\n")
         and f"| [Alpha](../companies/alpha.md) | [Alpha late]({rec(12)}) | Alpha late shipped. | [Src]"
             f"(http://example.com/12) |" in l45.split("\n")
         and l45.split("\n")[2].startswith("4 rows are listed for November 2 to 8, 2026 in The Deploy Log, from 2 "
                                           "companies. Alpha shipped the most, 3 rows, then Beta with 1. 3 carry a "
                                           "publisher's date and 1 is placed by their edition."),
         (heads(l45), l45.split("\n")[2])),
        ("a company page lists a row dated ahead under no month, and its range ends on a day that has come",
         heads(lalpha) == ["November 2026", "October 2026", "Undated until its day", "Placed by their edition"]
         and unprinted(lalpha) and one_ahead in lalpha.split("\n")
         and f"| [Alpha late]({rec(12)}) | Alpha late shipped. | [Src](http://example.com/12) |" in lalpha.split("\n")
         and lalpha.split("\n")[2] == "4 rows in The Deploy Log are filed under Alpha. 3 carry a publisher's date, "
         "from October 13, 2026 to November 3, 2026, and 1 is placed by its edition. 1 of those dates has not yet "
         "come in New York.", (heads(lalpha), lalpha.split("\n")[2])),
        ("the indexes count a row dated ahead as dated, and First and Latest are days that have come",
         f"| [Alpha](alpha.md) | 4 | 3 | 2026-10-13 | 2026-11-03 | [page]({BASE}company/aaaaaaaaaaaa/alpha/?k=repo) |"
         in late["companies/README.md"].split("\n")
         and f"| [2026-W45](2026-W45.md) (in progress) | 2026-11-02 to 2026-11-08 | 4 | 3 | [page]({BASE}week/"
             f"2026-W45/?k=repo) |" in late["weeks/README.md"].split("\n"),
         [s for s in late["companies/README.md"].split("\n") if s.startswith("| [Alpha]")]),
        ("a week whose only row is dated ahead still gets its page, with no day heading",
         heads(w46) == ["Undated until its day"] and one_ahead in w46.split("\n")
         and w46.split("\n")[2] == "1 row is listed for November 9 to 15, 2026 in The Deploy Log, from 1 company. "
         "Beta shipped it. 1 carries a publisher's date and 0 are placed by their edition.",
         (heads(w46), w46.split("\n")[2])),
        ("rows dated ahead read right above one, on a page",
         ahead_line(6, True) == "6 rows carry a publisher's date that has not yet come in New York. The record "
                                "prints no date for them until that day, and neither does this page.",
         ahead_line(6, True)),
        ("the README says how many rows are dated ahead, in the singular, above one, and not at all when none is",
         [ahead_line(1), ahead_line(6), ahead_line(0)] == [
             "1 row carries a publisher's date that has not yet come in New York, and is listed from that day.",
             "6 rows carry a publisher's date that has not yet come in New York, and are listed from that day.", ""],
         [ahead_line(1), ahead_line(6), ahead_line(0)]),
        ("a day heading, a Date cell, an index cell or a company's range that prints a day that has not come stops "
         "the build", guard == [
             f"{path} prints 2026-11-05, a publisher's date that has not yet come in New York"
             for path in ("weeks/2026-W45.md", "companies/alpha.md", "companies/README.md", "companies/alpha.md")],
         guard),
    ]
    for name, n, dates, late_n, want in (
            ("every date ahead and some rows placed", 7, [], 2,
             f"7 rows {filed} 2 carry a publisher's date and 5 are placed by their edition. 2 of those dates have "
             f"not yet come in New York."),
            ("every row dated and every date ahead", 2, [], 2,
             f"2 rows {filed} Every one carries a publisher's date. 2 of those dates have not yet come in New York."),
            ("one row, dated ahead", 1, [], 1,
             "1 row in The Deploy Log is filed under X. It carries a publisher's date, which has not yet come in "
             "New York."),
            ("one date, ahead, among placed rows", 3, [], 1,
             f"3 rows {filed} 1 carries a publisher's date and 2 are placed by their edition. That date has not "
             f"yet come in New York."),
            ("one day that has come and two ahead", 3, nov4, 2,
             f"3 rows {filed} Every one carries a publisher's date, 1 on November 4, 2026. 2 of those dates have "
             f"not yet come in New York."),
            ("a range that has come and three dates ahead", 9, ["2026-11-02"] + nov4, 3,
             f"9 rows {filed} 5 carry a publisher's date, from November 2, 2026 to November 4, 2026, and 4 are "
             f"placed by their edition. 3 of those dates have not yet come in New York.")):
        got = company_paragraph("X", n, dates, late_n)
        checks.append((f"a company page opens right with {name}", got == want, got))

    # Review round 1: the README's example row, names in a week's opening, and a link's destination.
    served = {n: ({"Content-Type": m, "Access-Control-Allow-Origin": CORS}, f"https://example.com/{n}")
              for n, m in MEDIA.items()}
    came, undated = ("2026-11-04", "Published Wednesday 4 Nov 2026"), ("2026-11-05", "Undated until its day")
    built = "as `data.json` served it when this file was built on November 4, 2026 (ET):"

    def example(*pairs):
        d = labelled(*pairs)
        try:
            text = "\n".join(api(d, served, True, today))
        except SystemExit as e:
            return str(e.code)
        return ([s.strip() for s in text.split("\n") if s.startswith("Example: ") or '"published_date"' in s],
                stops(lambda: check_ahead(text, d["rows"], today, "README")))

    two = labelled(undated, came)["rows"]
    no_day = "README prints 2026-11-05, a publisher's date that has not yet come in New York"
    old_readme = [stops(lambda: check_ahead(text, two, today, "README")) for text in (
        json.dumps(two[0], indent=2), "Rows are listed from September 17, 2025 to November 5, 2026, each",
        "| OpenAI | 273 | 166 | 2025-09-25 | 2026-11-05 |", '  "added_at": "2026-11-05T02:10:57.320Z",')]
    # A Saturday evening, with a row dated the Sunday its week runs to: the week's sentence names that Sunday.
    sat, sunday_row = datetime.date(2026, 11, 7), ("2026-11-08", "Undated until its day")
    weekend = labelled(sunday_row, ("2026-11-07", "Published Saturday 7 Nov 2026"))
    saturday = "\n".join([week_paragraph(2, 2, Counter({"Alpha": 2}), datetime.date(2026, 11, 2),
                                         datetime.date(2026, 11, 8), sat),
                          "Rows are listed from November 2, 2026 to November 7, 2026, each by its publisher's date",
                          *api(weekend, served, True, sat)])
    en = DASHES[1]
    try:
        named = pages([row(31, f"Del{en}ta", "Delta one", "2026-11-04"), row(32, f"Del{en}ta", "Delta two", "2026-11-03"),
                       row(33, "Alpha", "Alpha one", "2026-11-04")], locs, hubs_, today)
    except SystemExit as e:
        named = ({}, str(e.code))
    try:
        odd = pages([row(34, "A_B*", "Odd one", "2026-11-04")], locs, {}, today)[0]["weeks/2026-W45.md"]
    except SystemExit as e:
        odd = str(e.code)
    n45, third = named[0].get("weeks/2026-W45.md", ""), lambda text: (text.split("\n") + ["", "", ""])[2]
    checks += [
        ("the README's example is the first object in rows, in the same words, when its day has come",
         example(came, undated) == ([f"Example: the first object in `rows`, {built}", '"published_date": "2026-11-04",'],
                                    "did not stop"), example(came, undated)),
        ("the README's example passes over a row dated ahead, says so, and prints no day that has not come",
         example(undated, came) == ([f"Example: the first object in `rows` whose publisher's date has come in New "
                                     f"York, {built}", '"published_date": "2026-11-04",'], "did not stop"),
         example(undated, came)),
        ("a record whose every row is dated ahead has no example to print, and stops the build",
         example(undated) == "every row in data.json carries a publisher's date that has not yet come in New York",
         example(undated)),
        ("a README that prints a day that has not come stops the build, in the data's words, in prose or in a cell, "
         "and a UTC stamp on that day does not", old_readme == [no_day, no_day, no_day, "did not stop"], old_readme),
        ("a README built on a Saturday with a row dated that week's Sunday passes, while its week names that Sunday",
         "The week runs to Sunday, November 8, 2026, and was still in progress" in saturday
         and '"published_date": "2026-11-07"' in saturday
         and stops(lambda: check_ahead(saturday, weekend["rows"], sat, "README")) == "did not stop",
         stops(lambda: check_ahead(saturday, weekend["rows"], sat, "README"))),
        ("a week whose top company's name carries a dash builds, counts the rows it can name, and names the rest",
         named[1] == ["00000000001f", "000000000020"] and n45 != "" and not any(d in t for t in named[0].values() for d in DASHES)
         and third(n45).startswith("1 row is listed for November 2 to 8, 2026 in The Deploy Log, from 1 "
                                   "company. Alpha shipped it. 1 carries a publisher's date")
         and "2 more rows count in this week but are left out of this page for a dash in their company's name, "
             "and are in `data.csv` as `00000000001f` and `000000000020`." in n45.split("\n")
         and left_line(["00000000001f"], more=True) == "1 more row counts in this week but is left out of this page "
             "for a dash in its company's name, and is in `data.csv` as `00000000001f`."
         and len(table_lines(n45)) == 1 and "| 3 | 3 |" in named[0].get("weeks/README.md", ""),
         (named[1], n45.split("\n")[2:5])),
        ("a company's name in a week's opening goes through prose",
         third(odd).startswith("1 row is listed for November 2 to 8, 2026 in The Deploy Log, from 1 company. "
                               "A\\_B\\* shipped it."), third(odd) or odd),
        ("a link's destination has its pipe, space, brackets and backslash percent encoded, and nothing else",
         [dest("http://e.example/a|b (c)<d>\\e?q=$1&r=_2"), plink("x", "http://e.example/a|b(c)")]
         == ["http://e.example/a%7Cb%20%28c%29%3Cd%3E%5Ce?q=$1&r=_2", "[x](http://e.example/a%7Cb%28c%29)"],
         [dest("http://e.example/a|b (c)<d>\\e?q=$1&r=_2"), plink("x", "http://e.example/a|b(c)")]),
    ]

    with tempfile.TemporaryDirectory() as root:
        for path in ("weeks/old.md", "weeks/keep.txt", "companies/gone.md", "other/old.md", "notes.md"):
            os.makedirs(os.path.dirname(os.path.join(root, path)), exist_ok=True)
            with open(os.path.join(root, path), "w") as f:
                f.write("stale\n")
        write_pages({p: made[p] for p in ("weeks/2026-W45.md", "companies/alpha.md")}, root)
        have = sorted(os.path.relpath(os.path.join(at, name), root).replace(os.sep, "/")
                      for at, _, names in os.walk(root) for name in names)
        with open(os.path.join(root, "weeks", "2026-W45.md"), encoding="utf-8") as f:
            wrote = f.read() == w45
    checks.append(("writing the pages removes a stale .md in the two folders and nothing else",
                   wrote and have == ["companies/alpha.md", "notes.md", "other/old.md", "weeks/2026-W45.md",
                                      "weeks/keep.txt"], have))
    with tempfile.TemporaryDirectory() as root:
        write_pages({}, root)
        checks.append(("a build with no page still leaves both folders, which the workflow stages by name",
                       sorted(os.listdir(root)) == ["companies", "weeks"], sorted(os.listdir(root))))
    return checks


def selftest():
    """Grammar at a count of one, read off the README of 2026-11-02 ('1 row are listed ... NVIDIA shipped the most,
    1 row. 1 carry a publisher's date'), and the engine's phrasing for a full week (log.ts companyLead)."""
    mon = datetime.date(2026, 11, 2); sun = datetime.date(2026, 11, 8)
    one = week_paragraph(1, 1, Counter({"NVIDIA": 1}), mon, sun, mon)
    want = ("1 row is listed for November 2 to 8, 2026 in The Deploy Log, from 1 company. NVIDIA shipped it. "
            "1 carries a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 8, 2026, "
            "and was still in progress when this file was built on November 2, 2026 (ET).")
    full = company_lead(Counter({"OpenAI": 25, "Amazon Web Services": 21, "Google": 9}))
    tied = company_lead(Counter({"A": 2, "B": 2}))
    many = company_lead(Counter({"A": 5, "B": 1, "C": 1, "D": 1, "E": 1}))
    top2 = company_lead(Counter({"A": 3, "B": 3, "C": 1}))
    checks = [
        ("a one row week reads 'is listed', 'shipped it' and 'carries'", one == want, one),
        ("one company with several rows shipped all of them", company_lead(Counter({"NVIDIA": 3})) == "NVIDIA shipped all 3.", company_lead(Counter({"NVIDIA": 3}))),
        ("the full week reads as the week page does", full == "OpenAI shipped the most, 25 rows, then Amazon Web Services with 21.", full),
        ("every company tied names them all with 'each'", tied == "A and B shipped 2 rows each.", tied),
        ("a second tier over three companies is counted, not named", many == "A shipped the most, 5 rows, then 4 companies with 1 each.", many),
        ("a tied top tier with a second tier names both with 'each'", top2 == "A and B shipped the most, 3 rows each, then C with 1.", top2),
    ] + selftest_pages()
    bad = [(name, got) for name, ok, got in checks if not ok]
    for name, got in bad:
        print(f"FAIL {name}: {got!r}")
    print(f"selftest: {len(checks) - len(bad)} of {len(checks)} pass")
    return 1 if bad else 0


def readme(d, served, today, paged, locs, lanes, companies, tools, release, refused):
    validate(d, today)
    check_tools(tools)
    rows = d["rows"]
    total = d["count"]
    url = d["url"]
    pub = [r for r in rows if r.get("published_date")]
    # A day that has not come in New York is printed nowhere: the range and the newest week end on one that has.
    days = sorted(listed(r) for r in rows if not ahead(r, today))
    undated = ahead_line(sum(1 for r in rows if ahead(r, today)))
    by_company = Counter(r["company"] for r in rows)
    hub = lambda u: u if u in locs else None
    newest = datetime.date.fromisoformat(days[-1])
    monday = newest - datetime.timedelta(days=newest.weekday())
    sunday = monday + datetime.timedelta(days=6)
    open_week = monday <= today <= sunday

    wk = iso_week(monday.isoformat())
    week_rows = [r for r in rows if iso_week(listed(r)) == wk]
    week_pub = sum(1 for r in week_rows if r.get("published_date"))
    wc = Counter(r["company"] for r in week_rows)
    title = f"What shipped in AI, week of {long_date(monday)}"
    week_url = hub(f"{BASE}week/{wk}/")
    out = [f"# {d['name']}", "", d["description"], "",
           f"## {link(title, week_url)}", "",
           week_paragraph(len(week_rows), week_pub, wc, monday, sunday, today if open_week else None), ""]
    here = pages_line(wk, paged)
    out += [here, ""] if here else []
    record = ["## The record", "",
           f"The record holds {num(total)} rows, {num(len(pub))} with a publisher's date, "
           f"{num(total - len(pub))} placed by their edition, from {num(len(by_company))} companies. "
           f"Rows are listed from {long_date(days[0])} to {long_date(days[-1])}, each by its publisher's date "
           f"or, where the record carries none, its edition's date. {undated + ' ' if undated else ''}The newest row "
           f"entered the record on "
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
        come = sorted(r["published_date"] for r in pub if r["company"] == c and not ahead(r, today))
        first, last = (come[0], come[-1]) if come else ("none", "none")
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
            "- `CITATION.cff`: how to cite the record", *files_lines(paged), "",
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
    check_ahead(text, rows, today, "README")
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
    # One read of the clock and one d for the README and the pages, so they name one day and count one set of rows.
    # Read here, before validate: at midnight in New York a label and the clock can disagree for a moment, and
    # main()'s second snapshot then reads a fresh clock with its fresh pair.
    today = datetime.datetime.now(ET).date()
    validate(d, today)
    made, left = pages(d["rows"], site[0], site[2], today)
    text = readme(d, {"data.json": (h_json, u_json), "data.csv": (h_csv, u_csv)}, today, made, *site).encode("utf-8")
    check_csv(raw_csv, d)
    return d, raw_json, raw_csv, text, made, left


def main():
    site = hubs() + (mcp_tools(), latest_release(), default_ua_refused())
    # A row can land between the two fetches; one fresh pair settles it.
    try:
        d, raw_json, raw_csv, text, made, left = snapshot(site)
    except SystemExit:
        d, raw_json, raw_csv, text, made, left = snapshot(site)
    outputs = (("data.json", raw_json), ("data.csv", raw_csv), ("README.md", text),
               ("CITATION.cff", citation(d).encode("utf-8")))
    for name, data in outputs:
        with open(name, "wb") as f:
            f.write(data)
    write_pages(made)
    missing = [BASE + p for p, _ in INDEXES if BASE + p not in site[0]]
    print(f"{d['count']} rows; sitemap lacks: {', '.join(missing) or 'no index'}")
    count = lambda folder: sum(1 for p in made if p.startswith(folder) and not p.endswith("/README.md"))
    print(f"{count('weeks/')} week pages, {count('companies/')} company pages; left out of them for a dash in "
          f"their text: {', '.join(left) or 'no row'}")


if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv[1:] else main()
