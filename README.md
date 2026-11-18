# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 16, 2026](https://deployedbyai.com/log/week/2026-W47/)

221 rows are listed for November 16 to 22, 2026 in The Deploy Log, from 57 companies. Amazon Web Services shipped the most, 27 rows, then OpenAI with 24. 221 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 22, 2026, and was still in progress when this file was built on November 18, 2026 (ET).

Every row of this week, with its source: [weeks/2026-W47.md](weeks/2026-W47.md). The record [week by week](weeks/README.md) and [company by company](companies/README.md).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 3,095 rows as CSV, under a header line of the field names |

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
| `count` | number | 3,095, the number of objects in `rows` |
| `rows` | array | 3,095 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 18, 2026 (ET):

```json
{
  "row_key": "a342c3235b03",
  "company": "Google",
  "subject": "ADK Java v1.15.0",
  "what_shipped": "ADK Java v1.15.0 adds FunctionNode, ClassifierNode, LlmClassifier, and workflow routing features.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-18",
  "date_label": "Published Wednesday 18 Nov 2026",
  "source": "Google, ADK Java v1.15.0",
  "source_url": "https://github.com/google/adk-java/releases/tag/v1.15.0",
  "record_url": "https://deployedbyai.com/log/a342c3235b03/adk-java-v1-15-0/?k=data",
  "added_at": "2026-11-18T11:10:53.810Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-18T11:10:53.810Z",
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
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "Amazon Web Services", "limit": 3}}}'
```

The response, as the server answered it when this file was built on November 18, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nAmazon Web Services: OpenSearch Serverless ingest pipelines. Ingest pipelines now clean, enrich, and vectorize documents at index time, with text_chunking, text_embedding, and ml_inference processors. Published Tuesday 17 Nov 2026. Source: https://aws.amazon.com/about-aws/whats-new/2026/11/opensearch-serverless-support-ingest-pipelines Record: https://deployedbyai.com/log/fd3479e164d8/opensearch-serverless-ingest-pipelines/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "fd3479e164d8",
          "company": "Amazon Web Services",
          "subject": "OpenSearch Serverless ingest pipelines",
          "what_shipped": "Ingest pipelines now clean, enrich, and vectorize documents at index time, with text_chunking, text_embedding, and ml_inference processors.",
          "shipped": "Published Tuesday 17 Nov 2026",
          "lane": "Tools and products",
          "source": "Amazon Web Services, OpenSearch Serverless ingest pipelines",
          "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/11/opensearch-serverless-support-ingest-pipelines",
          "record_url": "https://deployedbyai.com/log/fd3479e164d8/opensearch-serverless-ingest-pipelines/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 3,095 rows, 2,536 with a publisher's date, 559 placed by their edition, from 157 companies. Rows are listed from September 17, 2025 to November 18, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 18, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 103 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 37 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 3 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 61 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 2,356 | 2,112 | 244 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 471 | 326 | 145 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 56 | 41 | 15 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 45 | 24 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 28 | 28 | 0 |
| Leads (filed in no lane) | 139 | 5 | 134 |
| Total | 3,095 | 2,536 | 559 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 331 | 221 | 2025-09-25 | 2026-11-18 |
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 328 | 131 | 2025-09-18 | 2026-11-17 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 231 | 186 | 2025-10-16 | 2026-11-18 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 217 | 211 | 2026-09-16 | 2026-11-17 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 125 | 115 | 2026-09-17 | 2026-11-18 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 108 | 107 | 2026-09-20 | 2026-11-18 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 106 | 56 | 2025-09-17 | 2026-11-18 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 95 | 95 | 2026-09-22 | 2026-11-18 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 90 | 90 | 2026-09-17 | 2026-11-18 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 77 | 68 | 2026-09-23 | 2026-11-18 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 73 | 64 | 2026-08-13 | 2026-11-17 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 58 | 52 | 2026-08-20 | 2026-11-17 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 54 | 42 | 2026-08-28 | 2026-11-17 |
| [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | 47 | 45 | 2026-09-28 | 2026-11-18 |
| [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | 47 | 47 | 2026-09-25 | 2026-11-17 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W47](https://deployedbyai.com/log/week/2026-W47/) (in progress) | 2026-11-16 to 2026-11-22 | 221 | 221 | 0 |
| [2026-W46](https://deployedbyai.com/log/week/2026-W46/) | 2026-11-09 to 2026-11-15 | 357 | 351 | 6 |
| [2026-W45](https://deployedbyai.com/log/week/2026-W45/) | 2026-11-02 to 2026-11-08 | 266 | 261 | 5 |
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) | 2026-10-26 to 2026-11-01 | 246 | 239 | 7 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 310 | 292 | 18 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 850 | 839 | 11 |
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 1,262 | 1,199 | 63 |
| [September 2026](https://deployedbyai.com/log/month/2026-09/) | 372 | 324 | 48 |
| [August 2026](https://deployedbyai.com/log/month/2026-08/) | 60 | 18 | 42 |
| [July 2026](https://deployedbyai.com/log/month/2026-07/) | 57 | 14 | 43 |
| [June 2026](https://deployedbyai.com/log/month/2026-06/) | 52 | 11 | 41 |
| [May 2026](https://deployedbyai.com/log/month/2026-05/) | 43 | 15 | 28 |
| [April 2026](https://deployedbyai.com/log/month/2026-04/) | 58 | 20 | 38 |
| [March 2026](https://deployedbyai.com/log/month/2026-03/) | 53 | 18 | 35 |
| [February 2026](https://deployedbyai.com/log/month/2026-02/) | 53 | 7 | 46 |
| [January 2026](https://deployedbyai.com/log/month/2026-01/) | 50 | 16 | 34 |
| [December 2025](https://deployedbyai.com/log/month/2025-12/) | 47 | 14 | 33 |
| [November 2025](https://deployedbyai.com/log/month/2025-11/) | 68 | 14 | 54 |
| [October 2025](https://deployedbyai.com/log/month/2025-10/) | 49 | 19 | 30 |
| [September 2025](https://deployedbyai.com/log/month/2025-09/) | 21 | 8 | 13 |
| Total | 3,095 | 2,536 | 559 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-18 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [OpenAI GPT-6.2 Astra and Sol](https://deployedbyai.com/log/48caf4199f16/openai-gpt-6-2-astra-and-sol/?k=data) | [Databricks, OpenAI GPT-6.2 Astra and Sol](https://docs.databricks.com/aws/en/release-notes/product/2026/november#openai-gpt-62-astra-and-sol-are-now-available-on-unity-gateway) |
| 2026-11-18 | [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | [deepagents 0.7.40](https://deployedbyai.com/log/e28fb4419fed/deepagents-0-7-40/?k=data) | [LangChain, deepagents 0.7.40](https://github.com/langchain-ai/deepagents/releases/tag/deepagents%3D%3D0.7.40) |
| 2026-11-18 | [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | [deepagents-code 0.2.11](https://deployedbyai.com/log/d8e819d690cb/deepagents-code-0-2-11/?k=data) | [LangChain, deepagents-code 0.2.11](https://github.com/langchain-ai/deepagents/releases/tag/deepagents-code%3D%3D0.2.11) |
| 2026-11-18 | [Promptfoo](https://deployedbyai.com/log/company/bf654b67c0f3/promptfoo/) | [Promptfoo code-scan-action 0.2.3](https://deployedbyai.com/log/3b6e8b5f1db2/promptfoo-code-scan-action-0-2-3/?k=data) | [Promptfoo, Promptfoo code-scan-action 0.2.3](https://github.com/promptfoo/promptfoo/releases/tag/code-scan-action-0.2.3) |
| 2026-11-18 | [Promptfoo](https://deployedbyai.com/log/company/bf654b67c0f3/promptfoo/) | [Promptfoo 0.126.0](https://deployedbyai.com/log/439044eac271/promptfoo-0-126-0/?k=data) | [Promptfoo, Promptfoo 0.126.0](https://github.com/promptfoo/promptfoo/releases/tag/0.126.0) |
| 2026-11-18 | [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | [Playwright MCP v0.0.86](https://deployedbyai.com/log/82bf32cf7c1c/playwright-mcp-v0-0-86/?k=data) | [Microsoft, Playwright MCP v0.0.86](https://github.com/microsoft/playwright-mcp/releases/tag/v0.0.86) |
| 2026-11-18 | [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | [GitHub Copilot team plugin defaults](https://deployedbyai.com/log/fc063eca0dc7/github-copilot-team-plugin-defaults/?k=data) | [GitHub, GitHub Copilot team plugin defaults](https://github.blog/changelog/2026-11-18-customize-github-copilot-for-your-team) |
| 2026-11-18 | [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | [Gemini Enterprise Canvas web apps](https://deployedbyai.com/log/cc05aa672107/gemini-enterprise-canvas-web-apps/?k=data) | [Google Cloud, Gemini Enterprise Canvas web apps](https://docs.cloud.google.com/gemini/enterprise/docs/release-notes#November_18_2026) |
| 2026-11-18 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [OpenSearch Serverless ingest pipelines](https://deployedbyai.com/log/fd3479e164d8/opensearch-serverless-ingest-pipelines/?k=data) | [Amazon Web Services, OpenSearch Serverless ingest pipelines](https://aws.amazon.com/about-aws/whats-new/2026/11/opensearch-serverless-support-ingest-pipelines) |
| 2026-11-18 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [openai-ruby v0.128.1](https://deployedbyai.com/log/e093fe2af48a/openai-ruby-v0-128-1/?k=data) | [OpenAI, openai-ruby v0.128.1](https://github.com/openai/openai-ruby/releases/tag/v0.128.1) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record
- `weeks/`: one page per week the record lists, every row with its source and its page in the record
- `companies/`: one page per company the record lists, the same way

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 3,095 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 3,095 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 3,095 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 3,095 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 2,956 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 587 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 587 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 2,536 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 3,095 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 3,095 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 3,095 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 3,095 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 3,095 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 239 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 409 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 3,095 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 3,095 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
