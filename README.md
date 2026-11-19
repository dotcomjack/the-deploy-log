# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 16, 2026](https://deployedbyai.com/log/week/2026-W47/)

302 rows are listed for November 16 to 22, 2026 in The Deploy Log, from 74 companies. Amazon Web Services shipped the most, 43 rows, then OpenAI with 24. 302 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 22, 2026, and was still in progress when this file was built on November 19, 2026 (ET).

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

The newest dated release, [2026-11-19](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-11-19), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 3,180 rows as CSV, under a header line of the field names |

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
| `count` | number | 3,180, the number of objects in `rows` |
| `rows` | array | 3,180 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 19, 2026 (ET):

```json
{
  "row_key": "baad5b74ca58",
  "company": "Databricks",
  "subject": "AI/BI Bulk Migration",
  "what_shipped": "Bulk migrate Tableau and Power BI reports to AI/BI Dashboards with a single /importBI command.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-19",
  "date_label": "Published Thursday 19 Nov 2026",
  "source": "Databricks, AI/BI Bulk Migration",
  "source_url": "https://www.databricks.com/blog/bulk-migrate-your-dashboards-aibi-genie-code",
  "record_url": "https://deployedbyai.com/log/baad5b74ca58/ai-bi-bulk-migration/?k=data",
  "added_at": "2026-11-19T17:13:36.861Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-19T17:13:36.861Z",
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

The response, as the server answered it when this file was built on November 19, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nAmazon Web Services: AWS Revenue Measurement Bedrock. AWS Revenue Measurement now attributes revenue for closed-source model usage in Amazon Bedrock. Published Thursday 19 Nov 2026. Source: https://aws.amazon.com/about-aws/whats-new/2026/11/revenue-measurement-bedrock/ Record: https://deployedbyai.com/log/315ed83a1c2a/aws-revenue-measurement-bedrock/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "315ed83a1c2a",
          "company": "Amazon Web Services",
          "subject": "AWS Revenue Measurement Bedrock",
          "what_shipped": "AWS Revenue Measurement now attributes revenue for closed-source model usage in Amazon Bedrock.",
          "shipped": "Published Thursday 19 Nov 2026",
          "lane": "Tools and products",
          "source": "Amazon Web Services, AWS Revenue Measurement Bedrock",
          "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/11/revenue-measurement-bedrock/",
          "record_url": "https://deployedbyai.com/log/315ed83a1c2a/aws-revenue-measurement-bedrock/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 3,180 rows, 2,621 with a publisher's date, 559 placed by their edition, from 160 companies. Rows are listed from September 17, 2025 to November 19, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 19, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 104 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 39 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 5 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 61 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 2,423 | 2,179 | 244 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 488 | 343 | 145 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 56 | 41 | 15 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 45 | 24 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 29 | 29 | 0 |
| Leads (filed in no lane) | 139 | 5 | 134 |
| Total | 3,180 | 2,621 | 559 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 333 | 223 | 2025-09-25 | 2026-11-18 |
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 332 | 135 | 2025-09-18 | 2026-11-19 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 234 | 189 | 2025-10-16 | 2026-11-19 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 233 | 227 | 2026-09-16 | 2026-11-19 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 127 | 117 | 2026-09-17 | 2026-11-18 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 115 | 114 | 2026-09-20 | 2026-11-19 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 108 | 58 | 2025-09-17 | 2026-11-19 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 96 | 96 | 2026-09-22 | 2026-11-19 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 90 | 90 | 2026-09-17 | 2026-11-18 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 84 | 75 | 2026-09-23 | 2026-11-19 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 76 | 67 | 2026-08-13 | 2026-11-19 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 58 | 52 | 2026-08-20 | 2026-11-17 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 55 | 43 | 2026-08-28 | 2026-11-18 |
| [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | 49 | 47 | 2026-09-28 | 2026-11-18 |
| [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | 48 | 48 | 2026-09-25 | 2026-11-18 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W47](https://deployedbyai.com/log/week/2026-W47/) (in progress) | 2026-11-16 to 2026-11-22 | 302 | 302 | 0 |
| [2026-W46](https://deployedbyai.com/log/week/2026-W46/) | 2026-11-09 to 2026-11-15 | 360 | 354 | 6 |
| [2026-W45](https://deployedbyai.com/log/week/2026-W45/) | 2026-11-02 to 2026-11-08 | 267 | 262 | 5 |
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) | 2026-10-26 to 2026-11-01 | 246 | 239 | 7 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 310 | 292 | 18 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 935 | 924 | 11 |
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
| Total | 3,180 | 2,621 | 559 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-19 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [AWS AppConfig AI Configuration](https://deployedbyai.com/log/d2cfcc55409e/aws-appconfig-ai-configuration/?k=data) | [Amazon Web Services, AWS AppConfig AI Configuration](https://aws.amazon.com/about-aws/whats-new/2026/11/aws-appconfig-native-ai-model-invocation-prompt-configurations/) |
| 2026-11-19 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [AWS Revenue Measurement Bedrock](https://deployedbyai.com/log/315ed83a1c2a/aws-revenue-measurement-bedrock/?k=data) | [Amazon Web Services, AWS Revenue Measurement Bedrock](https://aws.amazon.com/about-aws/whats-new/2026/11/revenue-measurement-bedrock/) |
| 2026-11-19 | [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | [Liquid AI d1.2 and d1.2-ultra](https://deployedbyai.com/log/d1291bcb62a3/liquid-ai-d1-2-and-d1-2-ultra/?k=data) | [Vercel, Liquid AI d1.2 and d1.2-ultra](https://vercel.com/changelog/liquid-ais-d1-2-and-d1-2-ultra-are-now-available-on-ai-gateway) |
| 2026-11-19 | [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | [js-genai v3.2.0](https://deployedbyai.com/log/ab59ebe4c13d/js-genai-v3-2-0/?k=data) | [Google, js-genai v3.2.0](https://github.com/googleapis/js-genai/releases/tag/v3.2.0) |
| 2026-11-19 | [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | [js-genai v3.1.0](https://deployedbyai.com/log/d9a6d4e48afd/js-genai-v3-1-0/?k=data) | [Google, js-genai v3.1.0](https://github.com/googleapis/js-genai/releases/tag/v3.1.0) |
| 2026-11-19 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [ChatGPT Enterprise in AWS Marketplace](https://deployedbyai.com/log/3977f285aac8/chatgpt-enterprise-in-aws-marketplace/?k=data) | [OpenAI, ChatGPT Enterprise in AWS Marketplace](https://openai.com/index/chatgpt-enterprise-aws-marketplace) |
| 2026-11-19 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [GPT-5.6 Cyber in AWS GovCloud](https://deployedbyai.com/log/a8b587e486df/gpt-5-6-cyber-in-aws-govcloud/?k=data) | [OpenAI, GPT-5.6 Cyber in AWS GovCloud](https://openai.com/index/daybreak-red-aws-govcloud) |
| 2026-11-19 | [GitLab](https://deployedbyai.com/log/company/3f8bdd05fc0e/gitlab/) | [GitLab 19.6](https://deployedbyai.com/log/c2827afbe5ed/gitlab-19-6/?k=data) | [GitLab, GitLab 19.6](https://docs.gitlab.com/releases/19/gitlab-19-6-released/) |
| 2026-11-19 | [PostHog](https://deployedbyai.com/log/company/97fc8c3bb9de/posthog/) | [Manage CDC from MCP](https://deployedbyai.com/log/719bc1dd553a/manage-cdc-from-mcp/?k=data) | [PostHog, Manage CDC from MCP](https://posthog.com/changelog?id=3164) |
| 2026-11-19 | [CrewAI](https://deployedbyai.com/log/company/ba61ca23a00b/crewai/) | [CrewAI 1.15.44](https://deployedbyai.com/log/ae6df01ef9b6/crewai-1-15-44/?k=data) | [CrewAI, CrewAI 1.15.44](https://github.com/crewAIInc/crewAI/releases/tag/1.15.44) |

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
| `row_key` | 3,180 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 3,180 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 3,180 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 3,180 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 3,041 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 587 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 587 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 2,621 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 3,180 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 3,180 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 3,180 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 3,180 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 3,180 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 261 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 480 | The ids of the platforms the row's subject or what_shipped names (the subject alone for MCP servers), or whose own source is a model's page on the platform whose file list held weight files when last read (read when the row is admitted and again every day), read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 3,180 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 3,180 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
