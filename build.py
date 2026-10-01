"""Refresh the dataset from deployedbyai.com and regenerate README.md from its own metadata.

Run daily by .github/workflows/refresh.yml. The data files are copied byte for byte; every
number in the README is counted from data.json, never typed.
"""
import csv
import io
import json
import re
import sys
import urllib.request

BASE = "https://deployedbyai.com/log/"
UA = "the-deploy-log-refresh (+https://github.com/dotcomjack/the-deploy-log)"


def fetch(name):
    req = urllib.request.Request(BASE + name, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status != 200:
            sys.exit(f"{name}: HTTP {r.status}")
        return r.read()


def readme(d):
    rows = d["rows"]
    if len(rows) != d["count"]:
        sys.exit(f"data.json count {d['count']} but {len(rows)} rows")
    if not rows:
        sys.exit("data.json has no rows")
    dates = sorted(r.get("published_date") or r.get("edition_date") or "" for r in rows)
    if not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", x) for x in dates):
        sys.exit("a row has no ISO date")
    if not all(r.get("source_url") and r.get("record_url") for r in rows):
        sys.exit("a row has no source_url or record_url")
    companies = len({r["company"] for r in rows})
    lic = d["license"]
    fields = "\n".join(f"- `{f}`" for f in d["fields"])
    return f"""# {d['name']}

{d['description']}

{d['count']} rows from {companies} companies, {dates[0]} to {dates[-1]}. Every row carries
`source_url`, the publisher's own page, and `record_url`, its page in the record at
{d['url']}

## Files

- `data.csv`: one row per deployment
- `data.json`: the same rows with this metadata

Both are copied daily from {d['url']}data.csv and {d['url']}data.json, unchanged.

## Fields

{fields}

## License

[{lic['name']}]({lic['url']}). Attribution: {lic['attribution']}
"""


def check_csv(raw, d):
    table = list(csv.reader(io.StringIO(raw.decode("utf-8"))))
    if not table or table[0] != d["fields"]:
        sys.exit("data.csv header does not match data.json fields")
    if len(table) - 1 != d["count"]:
        sys.exit(f"data.csv has {len(table) - 1} rows, data.json says {d['count']}")


def snapshot():
    raw_json = fetch("data.json")
    raw_csv = fetch("data.csv")
    d = json.loads(raw_json.decode("utf-8"))
    text = readme(d).encode("utf-8")
    check_csv(raw_csv, d)
    return d, raw_json, raw_csv, text


def main():
    # A row can land between the two fetches; one fresh pair settles it.
    try:
        d, raw_json, raw_csv, text = snapshot()
    except SystemExit:
        d, raw_json, raw_csv, text = snapshot()
    for name, data in (("data.json", raw_json), ("data.csv", raw_csv), ("README.md", text)):
        with open(name, "wb") as f:
            f.write(data)
    print(f"{d['count']} rows")


if __name__ == "__main__":
    main()
