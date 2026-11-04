# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 2, 2026](https://deployedbyai.com/log/week/2026-W45/)

95 rows are listed for November 2 to 8, 2026 in The Deploy Log, from 37 companies. Vercel shipped the most, 10 rows, then Anthropic with 9. 95 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 8, 2026, and was still in progress when this file was built on November 4, 2026 (ET).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-11-03](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-11-03), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 2,339 rows as CSV, under a header line of the field names |

- Auth: none. A GET that carries no key, token or cookie answers 200.
- HTTPS: yes.
- CORS: both answer with `access-control-allow-origin: *`.
- User-Agent: send your own. deployedbyai.com refuses Python's default one ([Load it](#load-it)).

`data.json` holds these keys, in this order:

| Key | Type | Holds |
|---|---|---|
| `name` | string | The Deploy Log |
| `publisher` | string | deployedbyai |
| `url` | string | https://deployedbyai.com/log/ |
| `description` | string | Every deployment deployedbyai has carried. Every item sourced to the publisher's own page. |
| `license` | object | Keys `name`, `url`, `attribution` |
| `fields` | array | The 17 field names, in the order of `data.csv`'s header |
| `dictionary` | array | 17 objects, a `name` and a `description` per field: the [Data dictionary](#data-dictionary) |
| `count` | number | 2,339, the number of objects in `rows` |
| `rows` | array | 2,339 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 4, 2026 (ET):

```json
{
  "row_key": "a6ed64c4baa6",
  "company": "Anthropic",
  "subject": "Claude Agent SDK TypeScript v0.3.318",
  "what_shipped": "Claude Agent SDK TypeScript v0.3.318 adds credential_expires_at, config_file_invalid reason, and parity with Claude Code v2.1.318.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-04",
  "date_label": "Published Wednesday 4 Nov 2026",
  "source": "Anthropic, Claude Agent SDK TypeScript v0.3.318",
  "source_url": "https://github.com/anthropics/claude-agent-sdk-typescript/releases/tag/v0.3.318",
  "record_url": "https://deployedbyai.com/log/a6ed64c4baa6/claude-agent-sdk-typescript-v0-3-318/?k=data",
  "added_at": "2026-11-04T00:10:42.846Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-04T00:10:42.846Z",
  "kind": "backfill"
}
```

## Ask it from an agent

The record answers over the Model Context Protocol at `https://deployedbyai.com/log/mcp`: read only, over Streamable HTTP (POST), with no key. Its tools, as the server lists them ([the server's page](https://deployedbyai.com/log/mcp/?k=mcp) also names the protocol versions it speaks):

| Tool | What it returns | Arguments |
|---|---|---|
| `recent_deployments` | The newest rows to enter The Deploy Log, newest first. Optionally one lane or one company. Each row names what shipped, when, and the publisher's own source URL. | `lane`, `company`, `limit` |
| `deployments_in_week` | Every row of The Deploy Log that shipped in one ISO week, the same rows as its week page. Each row carries the publisher's own source URL. | `week` (required) |
| `search_deployments` | Rows of The Deploy Log whose company, subject or what shipped contains the words given, newest first. Each row carries the publisher's own source URL. | `query` (required), `limit` |

One call, without a client:

```sh
curl -s https://deployedbyai.com/log/mcp -H 'content-type: application/json' \
  -H 'accept: application/json, text/event-stream' \
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "Vercel", "limit": 3}}}'
```

The response, as the server answered it when this file was built on November 4, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nVercel: Tencent Hy4 on AI Gateway. Tencent Hy4 is available on AI Gateway at 50% off through December 31, 2026, with a 1M-token context window. Published Tuesday 3 Nov 2026. Source: https://vercel.com/changelog/tencent-hy4-now-available-on-ai-gateway Record: https://deployedbyai.com/log/79fc19048eb6/tencent-hy4-on-ai-gateway/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "79fc19048eb6",
          "company": "Vercel",
          "subject": "Tencent Hy4 on AI Gateway",
          "what_shipped": "Tencent Hy4 is available on AI Gateway at 50% off through December 31, 2026, with a 1M-token context window.",
          "shipped": "Published Tuesday 3 Nov 2026",
          "lane": "Tools and products",
          "source": "Vercel, Tencent Hy4 on AI Gateway",
          "source_url": "https://vercel.com/changelog/tencent-hy4-now-available-on-ai-gateway",
          "record_url": "https://deployedbyai.com/log/79fc19048eb6/tencent-hy4-on-ai-gateway/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 2,339 rows, 1,795 with a publisher's date, 544 placed by their edition, from 147 companies. Rows are listed from September 17, 2025 to November 4, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 4, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 87 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 31 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 2 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 59 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 1,729 | 1,494 | 235 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 365 | 222 | 143 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 46 | 33 | 13 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 45 | 24 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 19 | 19 | 0 |
| Leads (filed in no lane) | 135 | 3 | 132 |
| Total | 2,339 | 1,795 | 544 |

## The 16 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 294 | 102 | 2025-09-18 | 2026-11-03 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 268 | 161 | 2025-09-25 | 2026-11-04 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 177 | 133 | 2025-10-16 | 2026-11-04 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 148 | 142 | 2026-09-16 | 2026-11-03 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 97 | 88 | 2026-09-17 | 2026-11-03 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 97 | 48 | 2025-09-17 | 2026-10-29 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 67 | 67 | 2026-09-17 | 2026-11-03 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 63 | 63 | 2026-09-22 | 2026-11-03 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 63 | 62 | 2026-09-20 | 2026-11-04 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 55 | 47 | 2026-08-13 | 2026-11-03 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 47 | 35 | 2026-08-28 | 2026-10-30 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 47 | 42 | 2026-08-20 | 2026-11-02 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 39 | 31 | 2026-09-23 | 2026-10-29 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 34 | 8 | 2025-10-25 | 2026-10-14 |
| [Google Research](https://deployedbyai.com/log/company/de1f4bdca32b/google-research/) | 33 | 20 | 2025-10-16 | 2026-07-09 |
| [Notion](https://deployedbyai.com/log/company/4751f64514b9/notion/) | 33 | 21 | 2025-11-10 | 2026-08-07 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W45](https://deployedbyai.com/log/week/2026-W45/) (in progress) | 2026-11-02 to 2026-11-08 | 95 | 95 | 0 |
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) | 2026-10-26 to 2026-11-01 | 246 | 239 | 7 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 308 | 290 | 18 |
| [2026-W39](https://deployedbyai.com/log/week/2026-W39/) | 2026-09-21 to 2026-09-27 | 134 | 123 | 11 |
| [2026-W38](https://deployedbyai.com/log/week/2026-W38/) | 2026-09-14 to 2026-09-20 | 39 | 19 | 20 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 101 | 101 | 0 |
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 1,261 | 1,198 | 63 |
| [September 2026](https://deployedbyai.com/log/month/2026-09/) | 370 | 322 | 48 |
| [August 2026](https://deployedbyai.com/log/month/2026-08/) | 59 | 18 | 41 |
| [July 2026](https://deployedbyai.com/log/month/2026-07/) | 55 | 14 | 41 |
| [June 2026](https://deployedbyai.com/log/month/2026-06/) | 51 | 11 | 40 |
| [May 2026](https://deployedbyai.com/log/month/2026-05/) | 43 | 15 | 28 |
| [April 2026](https://deployedbyai.com/log/month/2026-04/) | 58 | 20 | 38 |
| [March 2026](https://deployedbyai.com/log/month/2026-03/) | 53 | 18 | 35 |
| [February 2026](https://deployedbyai.com/log/month/2026-02/) | 53 | 7 | 46 |
| [January 2026](https://deployedbyai.com/log/month/2026-01/) | 50 | 16 | 34 |
| [December 2025](https://deployedbyai.com/log/month/2025-12/) | 47 | 14 | 33 |
| [November 2025](https://deployedbyai.com/log/month/2025-11/) | 68 | 14 | 54 |
| [October 2025](https://deployedbyai.com/log/month/2025-10/) | 49 | 19 | 30 |
| [September 2025](https://deployedbyai.com/log/month/2025-09/) | 21 | 8 | 13 |
| Total | 2,339 | 1,795 | 544 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-04 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [WorkSpaces for AI agents](https://deployedbyai.com/log/354686361ba5/workspaces-for-ai-agents/?k=data) | [Amazon Web Services, WorkSpaces for AI agents](https://aws.amazon.com/about-aws/whats-new/2026/11/workspaces-ai-agents-linux-windows-11) |
| 2026-11-04 | [Pydantic](https://deployedbyai.com/log/company/49425b50f21d/pydantic/) | [Pydantic AI v1.107.10](https://deployedbyai.com/log/bd61a86a072c/pydantic-ai-v1-107-10/?k=data) | [Pydantic, Pydantic AI v1.107.10](https://github.com/pydantic/pydantic-ai/releases/tag/v1.107.10) |
| 2026-11-04 | [Qwen](https://deployedbyai.com/log/company/abb905e81511/qwen/) | [Qwen Code v0.26.7](https://deployedbyai.com/log/566172551697/qwen-code-v0-26-7/?k=data) | [Qwen, Qwen Code v0.26.7](https://github.com/QwenLM/qwen-code/releases/tag/v0.26.7) |
| 2026-11-04 | [Ray](https://deployedbyai.com/log/company/d4a327ffd86a/ray/) | [Ray 2.60.0](https://deployedbyai.com/log/8b639ae29a82/ray-2-60-0/?k=data) | [Ray, Ray 2.60.0](https://github.com/ray-project/ray/releases/tag/ray-2.60.0) |
| 2026-11-04 | [Langfuse](https://deployedbyai.com/log/company/52628f607201/langfuse/) | [Langfuse AI Gateway limits](https://deployedbyai.com/log/02b3ce9b6e20/langfuse-ai-gateway-limits/?k=data) | [Langfuse, Langfuse AI Gateway limits](https://github.com/langfuse/langfuse/releases/tag/v4.75.0) |
| 2026-11-04 | [ElevenLabs](https://deployedbyai.com/log/company/e208273cd56a/elevenlabs/) | [ElevenLabs Python SDK v2.76.0](https://deployedbyai.com/log/9031f701e9ea/elevenlabs-python-sdk-v2-76-0/?k=data) | [ElevenLabs, ElevenLabs Python SDK v2.76.0](https://github.com/elevenlabs/elevenlabs-python/releases/tag/v2.76.0) |
| 2026-11-04 | [Mistral](https://deployedbyai.com/log/company/72d07fed89b4/mistral/) | [mistral-vibe v3.1.0](https://deployedbyai.com/log/2f91520ae57d/mistral-vibe-v3-1-0/?k=data) | [Mistral, mistral-vibe v3.1.0](https://github.com/mistralai/mistral-vibe/releases/tag/v3.1.0) |
| 2026-11-04 | [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | [Tencent Hy4 on AI Gateway](https://deployedbyai.com/log/79fc19048eb6/tencent-hy4-on-ai-gateway/?k=data) | [Vercel, Tencent Hy4 on AI Gateway](https://vercel.com/changelog/tencent-hy4-now-available-on-ai-gateway) |
| 2026-11-04 | Dify | [Dify 1.19.0](https://deployedbyai.com/log/259b539b2214/dify-1-19-0/?k=data) | [Dify, Dify 1.19.0](https://github.com/langgenius/dify/releases/tag/1.19.0) |
| 2026-11-04 | [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | [Tencent Hy4 on OpenRouter](https://deployedbyai.com/log/c6bed531a9b5/tencent-hy4-on-openrouter/?k=data) | [OpenRouter, Tencent Hy4 on OpenRouter](https://openrouter.ai/tencent/hy4) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 2,339 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 2,339 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 2,339 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 2,339 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 2,204 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 558 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 558 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 1,795 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 2,339 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 2,339 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 2,339 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 2,339 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 2,339 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 179 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 285 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 2,339 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 2,339 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
