# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 23, 2026](https://deployedbyai.com/log/week/2026-W48/)

90 rows are listed for November 23 to 29, 2026 in The Deploy Log, from 38 companies. Amazon Web Services shipped the most, 14 rows, then Anthropic and LangChain with 10 each. 90 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 29, 2026, and was still in progress when this file was built on November 24, 2026 (ET).

Every row of this week, with its source: [weeks/2026-W48.md](weeks/2026-W48.md). The record [week by week](weeks/README.md) and [company by company](companies/README.md).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-11-23](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-11-23), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 3,456 rows as CSV, under a header line of the field names |

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
| `count` | number | 3,456, the number of objects in `rows` |
| `rows` | array | 3,456 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 24, 2026 (ET). A string longer than 160 characters is cut here and ends in `...`:

```json
{
  "row_key": "fbdb6c66b111",
  "company": "Microsoft",
  "subject": "Copilot UX components in Cowork",
  "what_shipped": "Copilot UX components are now supported in Copilot Cowork, packaged as plugins with skills and other assets, governed by the same admin tools as other...",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-24",
  "date_label": "Published Tuesday 24 Nov 2026",
  "source": "Microsoft, Copilot UX components in Cowork",
  "source_url": "https://devblogs.microsoft.com/microsoft365dev/copilot-ux-components-now-available-in-cowork-with-plugins-spfx-roadmap-update-for-november-2026/",
  "record_url": "https://deployedbyai.com/log/fbdb6c66b111/copilot-ux-components-in-cowork/?k=data",
  "added_at": "2026-11-24T12:12:28.407Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-24T12:12:28.407Z",
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

The response, as the server answered it when this file was built on November 24, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nAmazon Web Services: OpenSearch 3.9 on AWS. OpenSearch 3.9 is available on Amazon OpenSearch Service in all regions, adding half-float vectors, 2-bit and 4-bit scalar quantization, and gRPC streaming for model predictions and agent execution. Published Monday 23 Nov 2026. Source: https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-opensearch-opensearch-3-9 Record: https://deployedbyai.com/log/d04b98ea84e2/opensearch-3-9-on-aws/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "d04b98ea84e2",
          "company": "Amazon Web Services",
          "subject": "OpenSearch 3.9 on AWS",
          "what_shipped": "OpenSearch 3.9 is available on Amazon OpenSearch Service in all regions, adding half-float vectors, 2-bit and 4-bit scalar quantization, and gRPC streaming for model predictions and agent execution.",
          "shipped": "Published Monday 23 Nov 2026",
          "lane": "Tools and products",
          "source": "Amazon Web Services, OpenSearch 3.9 on AWS",
          "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-opensearch-opensearch-3-9",
          "record_url": "https://deployedbyai.com/log/d04b98ea84e2/opensearch-3-9-on-aws/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 3,456 rows, 2,889 with a publisher's date, 567 placed by their edition, from 164 companies. Rows are listed from September 17, 2025 to November 24, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 24, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 112 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 61 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 8 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 62 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap
- [AI tools, version by version](https://deployedbyai.com/log/product/): 155 pages listed in the record's sitemap
- [AI coding tools](https://deployedbyai.com/log/ai-coding-tools/)
- [AI news today](https://deployedbyai.com/log/today/)
- [LLM inference engines](https://deployedbyai.com/log/llm-inference-engines/)
- [AI gateways](https://deployedbyai.com/log/ai-gateways/)
- [Vector databases](https://deployedbyai.com/log/vector-databases/)
- [LangChain vs LangGraph](https://deployedbyai.com/log/langchain-vs-langgraph/)

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 2,659 | 2,409 | 250 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 522 | 376 | 146 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 57 | 42 | 15 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 46 | 25 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 31 | 31 | 0 |
| Leads (filed in no lane) | 141 | 6 | 135 |
| Total | 3,456 | 2,889 | 567 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 352 | 242 | 2025-09-25 | 2026-11-24 |
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 339 | 140 | 2025-09-18 | 2026-11-23 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 303 | 295 | 2026-09-16 | 2026-11-23 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 264 | 219 | 2025-10-16 | 2026-11-23 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 136 | 135 | 2026-09-20 | 2026-11-24 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 130 | 117 | 2026-09-17 | 2026-11-18 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 110 | 60 | 2025-09-17 | 2026-11-23 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 98 | 98 | 2026-09-22 | 2026-11-20 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 94 | 94 | 2026-09-17 | 2026-11-23 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 89 | 80 | 2026-09-23 | 2026-11-24 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 79 | 70 | 2026-08-13 | 2026-11-20 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 61 | 55 | 2026-08-20 | 2026-11-24 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 57 | 44 | 2026-08-28 | 2026-11-23 |
| [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | 51 | 49 | 2026-09-28 | 2026-11-24 |
| [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | 51 | 51 | 2026-09-25 | 2026-11-21 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W48](https://deployedbyai.com/log/week/2026-W48/) (in progress) | 2026-11-23 to 2026-11-29 | 90 | 90 | 0 |
| [2026-W47](https://deployedbyai.com/log/week/2026-W47/) | 2026-11-16 to 2026-11-22 | 487 | 479 | 8 |
| [2026-W46](https://deployedbyai.com/log/week/2026-W46/) | 2026-11-09 to 2026-11-15 | 361 | 355 | 6 |
| [2026-W45](https://deployedbyai.com/log/week/2026-W45/) | 2026-11-02 to 2026-11-08 | 267 | 262 | 5 |
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) | 2026-10-26 to 2026-11-01 | 246 | 239 | 7 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 1,211 | 1,192 | 19 |
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
| Total | 3,456 | 2,889 | 567 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-24 | [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | [Copilot UX components in Cowork](https://deployedbyai.com/log/fbdb6c66b111/copilot-ux-components-in-cowork/?k=data) | [Microsoft, Copilot UX components in Cowork](https://devblogs.microsoft.com/microsoft365dev/copilot-ux-components-now-available-in-cowork-with-plugins-spfx-roadmap-update-for-november-2026/) |
| 2026-11-24 | [Roboflow](https://deployedbyai.com/log/company/80d681b2d1d5/roboflow/) | [supervision 0.32.1](https://deployedbyai.com/log/7fdc5d7102c4/supervision-0-32-1/?k=data) | [Roboflow, supervision 0.32.1](https://github.com/roboflow/supervision/releases/tag/0.32.1) |
| 2026-11-24 | [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | [OpenSearch 3.9 on AWS](https://deployedbyai.com/log/d04b98ea84e2/opensearch-3-9-on-aws/?k=data) | [Amazon Web Services, OpenSearch 3.9 on AWS](https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-opensearch-opensearch-3-9) |
| 2026-11-24 | [OpenHands](https://deployedbyai.com/log/company/3073c3e8ba0d/openhands/) | [OpenHands v1.45.0](https://deployedbyai.com/log/6e674cb0a91f/openhands-v1-45-0/?k=data) | [OpenHands, OpenHands v1.45.0](https://github.com/OpenHands/OpenHands/releases/tag/v1.45.0) |
| 2026-11-24 | [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | [Dynamo v1.7.0](https://deployedbyai.com/log/bfc895d976b2/dynamo-v1-7-0/?k=data) | [NVIDIA, Dynamo v1.7.0](https://github.com/ai-dynamo/dynamo/releases/tag/v1.7.0) |
| 2026-11-24 | [Meta](https://deployedbyai.com/log/company/50c5556ca53b/meta/) | [Meta Muse UK](https://deployedbyai.com/log/18973176ea47/meta-muse-uk/?k=data) | [Meta, Meta Muse UK](https://about.fb.com/news/2026/11/muse-now-available-in-the-uk-muse-does-the-work-you-stay-in-control/) |
| 2026-11-24 | [Tencent](https://deployedbyai.com/log/company/ea750d3cf789/tencent/) | [OmniEVIE-4B](https://deployedbyai.com/log/a220202235f9/omnievie-4b/?k=data) | [Tencent, OmniEVIE-4B](https://huggingface.co/tencent/OmniEVIE-4B) |
| 2026-11-24 | [LiteLLM](https://deployedbyai.com/log/company/e6e88af05f6d/litellm/) | [LiteLLM v1.109.4](https://deployedbyai.com/log/ca351b45f26e/litellm-v1-109-4/?k=data) | [LiteLLM, LiteLLM v1.109.4](https://github.com/BerriAI/litellm/releases/tag/v1.109.4) |
| 2026-11-24 | [LiteLLM](https://deployedbyai.com/log/company/e6e88af05f6d/litellm/) | [LiteLLM v1.110.3](https://deployedbyai.com/log/dcc04257444a/litellm-v1-110-3/?k=data) | [LiteLLM, LiteLLM v1.110.3](https://github.com/BerriAI/litellm/releases/tag/v1.110.3) |
| 2026-11-23 | [CrewAI](https://deployedbyai.com/log/company/ba61ca23a00b/crewai/) | [CrewAI 1.15.45](https://deployedbyai.com/log/9ea6c863f2f9/crewai-1-15-45/?k=data) | [CrewAI, CrewAI 1.15.45](https://github.com/crewAIInc/crewAI/releases/tag/1.15.45) |

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
| `row_key` | 3,456 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 3,456 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 3,456 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 3,456 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 3,315 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 603 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 603 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 2,889 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 3,456 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 3,456 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 3,456 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 3,456 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 3,456 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 322 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 537 | The ids of the platforms the row's subject or what_shipped names (the subject alone for MCP servers), or whose own source is a model's page on the platform whose file list held weight files when last read (read when the row is admitted and again every day), read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners, except Google AI Studio, Microsoft Foundry and Google Antigravity, where their owners' rows count too; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 3,456 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 3,456 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
