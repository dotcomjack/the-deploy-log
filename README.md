# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of October 26, 2026](https://deployedbyai.com/log/week/2026-W44/)

202 rows are listed for October 26 to November 1, 2026 in The Deploy Log, from 68 companies. OpenAI shipped the most, 16 rows, then Vercel with 15. 202 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 1, 2026, and was still in progress when this file was built on October 30, 2026 (ET).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-10-29](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-10-29), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 2,200 rows as CSV, under a header line of the field names |

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
| `count` | number | 2,200, the number of objects in `rows` |
| `rows` | array | 2,200 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on October 30, 2026 (ET):

```json
{
  "row_key": "aec19c6900d1",
  "company": "Anthropic",
  "subject": "Claude Agent SDK Python v0.2.175",
  "what_shipped": "claude-agent-sdk 0.2.175 bundles Claude CLI 2.1.314 and is available on PyPI.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-10-30",
  "date_label": "Published Friday 30 Oct 2026",
  "source": "Anthropic, Claude Agent SDK Python v0.2.175",
  "source_url": "https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.175",
  "record_url": "https://deployedbyai.com/log/aec19c6900d1/claude-agent-sdk-python-v0-2-175/?k=data",
  "added_at": "2026-10-30T02:11:17.328Z",
  "models": [],
  "platforms": [],
  "updated": "2026-10-30T02:11:17.328Z",
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
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "OpenAI", "limit": 3}}}'
```

The response, as the server answered it when this file was built on October 30, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nRetool: GPT 6.1 Terra in Retool. GPT 6.1 Terra is now available in Retool through OpenAI for AI resource queries and building apps. Published Thursday 29 Oct 2026. Source: https://docs.retool.com/changelog/gpt-6.1-terra Record: https://deployedbyai.com/log/6affaee18bb5/gpt-6-1-terra-in-retool/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "6affaee18bb5",
          "company": "Retool",
          "subject": "GPT 6.1 Terra in Retool",
          "what_shipped": "GPT 6.1 Terra is now available in Retool through OpenAI for AI resource queries and building apps.",
          "shipped": "Published Thursday 29 Oct 2026",
          "lane": "Tools and products",
          "source": "Retool, GPT 6.1 Terra in Retool",
          "source_url": "https://docs.retool.com/changelog/gpt-6.1-terra",
          "record_url": "https://deployedbyai.com/log/6affaee18bb5/gpt-6-1-terra-in-retool/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 2,200 rows, 1,663 with a publisher's date, 537 placed by their edition, from 144 companies. Rows are listed from September 17, 2025 to October 30, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on October 30, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 84 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 31 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 2 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 58 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 14 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 1,600 | 1,370 | 230 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 362 | 220 | 142 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 45 | 24 | 21 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 45 | 32 | 13 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 16 | 16 | 0 |
| Leads (filed in no lane) | 132 | 1 | 131 |
| Total | 2,200 | 1,663 | 537 |

## The 16 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 280 | 91 | 2025-09-18 | 2026-10-29 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 251 | 145 | 2025-09-25 | 2026-10-27 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 166 | 122 | 2025-10-16 | 2026-10-30 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 136 | 131 | 2026-09-16 | 2026-10-29 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 97 | 48 | 2025-09-17 | 2026-10-29 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 94 | 86 | 2026-09-17 | 2026-10-28 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 61 | 61 | 2026-09-17 | 2026-10-29 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 56 | 55 | 2026-09-20 | 2026-10-29 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 54 | 54 | 2026-09-22 | 2026-10-29 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 48 | 40 | 2026-08-13 | 2026-10-27 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 46 | 34 | 2026-08-28 | 2026-10-23 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 45 | 40 | 2026-08-20 | 2026-10-27 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 38 | 31 | 2026-09-23 | 2026-10-29 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 34 | 8 | 2025-10-25 | 2026-10-14 |
| [Google Research](https://deployedbyai.com/log/company/de1f4bdca32b/google-research/) | 33 | 20 | 2025-10-16 | 2026-07-09 |
| [Notion](https://deployedbyai.com/log/company/4751f64514b9/notion/) | 33 | 21 | 2025-11-10 | 2026-08-07 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) (in progress) | 2026-10-26 to 2026-11-01 | 202 | 202 | 0 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 308 | 290 | 18 |
| [2026-W39](https://deployedbyai.com/log/week/2026-W39/) | 2026-09-21 to 2026-09-27 | 134 | 123 | 11 |
| [2026-W38](https://deployedbyai.com/log/week/2026-W38/) | 2026-09-14 to 2026-09-20 | 39 | 19 | 20 |
| [2026-W37](https://deployedbyai.com/log/week/2026-W37/) | 2026-09-07 to 2026-09-13 | 5 | 0 | 5 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 1,223 | 1,167 | 56 |
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
| Total | 2,200 | 1,663 | 537 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-10-30 | [Mistral](https://deployedbyai.com/log/company/72d07fed89b4/mistral/) | [Mistral Vibe v3.0.4](https://deployedbyai.com/log/f7f9ddaa82e4/mistral-vibe-v3-0-4/?k=data) | [Mistral, Mistral Vibe v3.0.4](https://github.com/mistralai/mistral-vibe/releases/tag/v3.0.4) |
| 2026-10-30 | [Qwen](https://deployedbyai.com/log/company/abb905e81511/qwen/) | [cua-driver-rs v0.27.0](https://deployedbyai.com/log/6ca8a4b01821/cua-driver-rs-v0-27-0/?k=data) | [Qwen, cua-driver-rs v0.27.0](https://github.com/QwenLM/qwen-code/releases/tag/cua-driver-rs-v0.27.0) |
| 2026-10-29 | [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | [Claude Agent SDK Python v0.2.175](https://deployedbyai.com/log/aec19c6900d1/claude-agent-sdk-python-v0-2-175/?k=data) | [Anthropic, Claude Agent SDK Python v0.2.175](https://github.com/anthropics/claude-agent-sdk-python/releases/tag/v0.2.175) |
| 2026-10-29 | [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | [Claude Code v2.1.314](https://deployedbyai.com/log/63825b3fa844/claude-code-v2-1-314/?k=data) | [Anthropic, Claude Code v2.1.314](https://github.com/anthropics/claude-code/releases/tag/v2.1.314) |
| 2026-10-29 | [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | [Claude Agent SDK TypeScript v0.3.314](https://deployedbyai.com/log/8b638e0b63ce/claude-agent-sdk-typescript-v0-3-314/?k=data) | [Anthropic, Claude Agent SDK TypeScript v0.3.314](https://github.com/anthropics/claude-agent-sdk-typescript/releases/tag/v0.3.314) |
| 2026-10-29 | [Ultralytics](https://deployedbyai.com/log/company/cc7ab7c8cefb/ultralytics/) | [Ultralytics 8.4.193](https://deployedbyai.com/log/e214aa0cfb69/ultralytics-8-4-193/?k=data) | [Ultralytics, Ultralytics 8.4.193](https://github.com/ultralytics/ultralytics/releases/tag/v8.4.193) |
| 2026-10-29 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Real-Time Mode for Spark Declarative Pipelines](https://deployedbyai.com/log/733e4588683f/real-time-mode-for-spark-declarative-pipelines/?k=data) | [Databricks, Real-Time Mode for Spark Declarative Pipelines](https://www.databricks.com/blog/announcing-general-availability-real-time-mode-spark-declarative-pipelines-databricks) |
| 2026-10-29 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [SageMaker AI SOCI-indexed images](https://deployedbyai.com/log/00e5183d32e4/sagemaker-ai-soci-indexed-images/?k=data) | [Amazon Web Services, SageMaker AI SOCI-indexed images](https://aws.amazon.com/about-aws/whats-new/2026/10/sagemaker-ai-soci-images-training/) |
| 2026-10-29 | [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | [Node.js 26 LTS on Vercel](https://deployedbyai.com/log/6ae0d33c67df/node-js-26-lts-on-vercel/?k=data) | [Vercel, Node.js 26 LTS on Vercel](https://vercel.com/changelog/node-js-26-lts-is-now-generally-available-on-vercel) |
| 2026-10-29 | [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | [ONNX Runtime WebGPU Plugin EP v0.5.0](https://deployedbyai.com/log/91150975d9ce/onnx-runtime-webgpu-plugin-ep-v0-5-0/?k=data) | [Microsoft, ONNX Runtime WebGPU Plugin EP v0.5.0](https://github.com/microsoft/onnxruntime/releases/tag/plugin-ep-webgpu%2Fv0.5.0) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 2,200 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 2,200 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 2,200 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 2,200 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 2,068 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 545 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 545 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 1,663 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 2,200 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 2,200 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 2,200 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 2,200 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 2,200 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 175 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 269 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 2,200 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 2,200 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
