# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 23, 2026](https://deployedbyai.com/log/week/2026-W48/)

222 rows are listed for November 23 to 29, 2026 in The Deploy Log, from 68 companies. Amazon Web Services shipped the most, 26 rows, then Anthropic with 19. 222 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 29, 2026, and was still in progress when this file was built on November 27, 2026 (ET).

Every row of this week, with its source: [weeks/2026-W48.md](weeks/2026-W48.md). The record [week by week](weeks/README.md), [company by company](companies/README.md) and [model by model](models/README.md).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-11-26](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-11-26), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 3,589 rows as CSV, under a header line of the field names |

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
| `count` | number | 3,589, the number of objects in `rows` |
| `rows` | array | 3,589 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 27, 2026 (ET):

```json
{
  "row_key": "541153be08b8",
  "company": "Model Context Protocol",
  "subject": "MCP Inspector 2.17.0",
  "what_shipped": "MCP Inspector 2.17.0 fixes an SSRF guard bypass for NAT64 and IPv4-embedding IPv6 addresses and adds the Events extension.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-27",
  "date_label": "Published Friday 27 Nov 2026",
  "source": "Model Context Protocol, MCP Inspector 2.17.0",
  "source_url": "https://github.com/modelcontextprotocol/inspector/releases/tag/2.17.0",
  "record_url": "https://deployedbyai.com/log/541153be08b8/mcp-inspector-2-17-0/?k=data",
  "added_at": "2026-11-27T10:11:03.713Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-27T10:11:03.713Z",
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

The response, as the server answered it when this file was built on November 27, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nAmazon Web Services: SageMaker HyperPod NCCL Profiler. The HyperPod NCCL Profiler loads as a plugin in training jobs and sends per-rank bandwidth and timing to CloudWatch or Managed Service for Prometheus, available in all HyperPod regions. Published Monday 23 Nov 2026. Source: https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-sagemaker-hyperpod-nccl-profiler/ Record: https://deployedbyai.com/log/4ffa297b2bcb/sagemaker-hyperpod-nccl-profiler/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "4ffa297b2bcb",
          "company": "Amazon Web Services",
          "subject": "SageMaker HyperPod NCCL Profiler",
          "what_shipped": "The HyperPod NCCL Profiler loads as a plugin in training jobs and sends per-rank bandwidth and timing to CloudWatch or Managed Service for Prometheus, available in all HyperPod regions.",
          "shipped": "Published Monday 23 Nov 2026",
          "lane": "Tools and products",
          "source": "Amazon Web Services, SageMaker HyperPod NCCL Profiler",
          "source_url": "https://aws.amazon.com/about-aws/whats-new/2026/11/amazon-sagemaker-hyperpod-nccl-profiler/",
          "record_url": "https://deployedbyai.com/log/4ffa297b2bcb/sagemaker-hyperpod-nccl-profiler/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 3,589 rows, 3,022 with a publisher's date, 567 placed by their edition, from 167 companies. Rows are listed from September 17, 2025 to November 27, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 27, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 113 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 62 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 8 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 62 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap
- [AI tools, version by version](https://deployedbyai.com/log/product/): 159 pages listed in the record's sitemap
- [AI coding tools](https://deployedbyai.com/log/ai-coding-tools/)
- [AI news today](https://deployedbyai.com/log/today/)
- [LLM inference engines](https://deployedbyai.com/log/llm-inference-engines/)
- [AI gateways](https://deployedbyai.com/log/ai-gateways/)
- [Vector databases](https://deployedbyai.com/log/vector-databases/)
- [LangChain vs LangGraph](https://deployedbyai.com/log/langchain-vs-langgraph/)
- [ChatGPT vs Gemini vs Copilot](https://deployedbyai.com/log/chatgpt-vs-gemini-vs-copilot/)
- [OpenAI vs Anthropic](https://deployedbyai.com/log/openai-vs-anthropic/)
- [GitHub vs GitLab](https://deployedbyai.com/log/github-vs-gitlab/)
- [Databricks vs Snowflake](https://deployedbyai.com/log/databricks-vs-snowflake/)
- [NVIDIA vs AMD](https://deployedbyai.com/log/nvidia-vs-amd/)
- [Claude Opus vs Sonnet](https://deployedbyai.com/log/claude-opus-vs-sonnet/)
- [Claude Fable vs Opus](https://deployedbyai.com/log/claude-fable-vs-opus/)
- [Gemini Argon vs Carbon](https://deployedbyai.com/log/gemini-argon-vs-carbon/)
- [GPT Sol vs Terra](https://deployedbyai.com/log/gpt-sol-vs-terra/)

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 2,781 | 2,531 | 250 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 532 | 386 | 146 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 57 | 42 | 15 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 46 | 25 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 32 | 32 | 0 |
| Leads (filed in no lane) | 141 | 6 | 135 |
| Total | 3,589 | 3,022 | 567 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 362 | 252 | 2025-09-25 | 2026-11-26 |
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 341 | 142 | 2025-09-18 | 2026-11-24 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 315 | 307 | 2026-09-16 | 2026-11-25 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 273 | 228 | 2025-10-16 | 2026-11-25 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 142 | 141 | 2026-09-20 | 2026-11-26 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 133 | 120 | 2026-09-17 | 2026-11-25 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 113 | 63 | 2025-09-17 | 2026-11-26 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 105 | 105 | 2026-09-22 | 2026-11-26 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 99 | 99 | 2026-09-17 | 2026-11-26 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 89 | 80 | 2026-09-23 | 2026-11-24 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 83 | 74 | 2026-08-13 | 2026-11-25 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 62 | 56 | 2026-08-20 | 2026-11-24 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 58 | 45 | 2026-08-28 | 2026-11-24 |
| [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | 53 | 53 | 2026-09-25 | 2026-11-26 |
| [Microsoft](https://deployedbyai.com/log/company/28257922d62c/microsoft/) | 52 | 50 | 2026-09-28 | 2026-11-24 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W48](https://deployedbyai.com/log/week/2026-W48/) (in progress) | 2026-11-23 to 2026-11-29 | 222 | 222 | 0 |
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
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 1,343 | 1,324 | 19 |
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 1,262 | 1,199 | 63 |
| [September 2026](https://deployedbyai.com/log/month/2026-09/) | 373 | 325 | 48 |
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
| Total | 3,589 | 3,022 | 567 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-27 | [PostHog](https://deployedbyai.com/log/company/97fc8c3bb9de/posthog/) | [PostHog mobile SDKs 4.0](https://deployedbyai.com/log/8aebc176d7e7/posthog-mobile-sdks-4-0/?k=data) | [PostHog, PostHog mobile SDKs 4.0](https://posthog.com/changelog?id=3178) |
| 2026-11-27 | [Model Context Protocol](https://deployedbyai.com/log/company/088b60189c15/model-context-protocol/) | [MCP Inspector 2.17.0](https://deployedbyai.com/log/541153be08b8/mcp-inspector-2-17-0/?k=data) | [Model Context Protocol, MCP Inspector 2.17.0](https://github.com/modelcontextprotocol/inspector/releases/tag/2.17.0) |
| 2026-11-27 | [Docker](https://deployedbyai.com/log/company/33dab0a853cb/docker/) | [docker-agent /btw side questions](https://deployedbyai.com/log/9dc09c4f249a/docker-agent-btw-side-questions/?k=data) | [Docker, docker-agent /btw side questions](https://github.com/docker/docker-agent/releases/tag/v1.167.0) |
| 2026-11-27 | [InternLM](https://deployedbyai.com/log/company/0d32feae2eb7/internlm/) | [Sage-Med-Preview](https://deployedbyai.com/log/b64449e86bcc/sage-med-preview/?k=data) | [InternLM, Sage-Med-Preview](https://huggingface.co/internlm/Sage-Med-Preview) |
| 2026-11-26 | [Meta](https://deployedbyai.com/log/company/50c5556ca53b/meta/) | [OGX 2.0](https://deployedbyai.com/log/addc7f6d2591/ogx-2-0/?k=data) | [Meta, OGX 2.0](https://github.com/ogx-ai/ogx/releases/tag/v2.0.0) |
| 2026-11-26 | [Pydantic](https://deployedbyai.com/log/company/49425b50f21d/pydantic/) | [Pydantic AI v2.76.0](https://deployedbyai.com/log/b1a3f73813a2/pydantic-ai-v2-76-0/?k=data) | [Pydantic, Pydantic AI v2.76.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.76.0) |
| 2026-11-26 | [Browser Use](https://deployedbyai.com/log/company/2dcdec0423ec/browser-use/) | [browser-use 1.0.9](https://deployedbyai.com/log/ff49d94cd5da/browser-use-1-0-9/?k=data) | [Browser Use, browser-use 1.0.9](https://github.com/browser-use/browser-use/releases/tag/1.0.9) |
| 2026-11-26 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Gemini Nano Banana 2.1 on Unity Gateway](https://deployedbyai.com/log/5506cf027f48/gemini-nano-banana-2-1-on-unity-gateway/?k=data) | [Databricks, Gemini Nano Banana 2.1 on Unity Gateway](https://docs.databricks.com/aws/en/release-notes/product/2026/november#google-gemini-nano-banana-21-is-now-available-on-unity-gateway) |
| 2026-11-26 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Genie One account-only access](https://deployedbyai.com/log/7b37da5bbd28/genie-one-account-only-access/?k=data) | [Databricks, Genie One account-only access](https://docs.databricks.com/aws/en/ai-bi/release-notes/2026#account-only-user-access-to-genie-one-is-generally-available) |
| 2026-11-26 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Gemini 4 Neon on Unity Gateway](https://deployedbyai.com/log/041ce213c97a/gemini-4-neon-on-unity-gateway/?k=data) | [Databricks, Gemini 4 Neon on Unity Gateway](https://docs.databricks.com/aws/en/release-notes/product/2026/november#google-gemini-4-neon-is-now-available-on-unity-gateway) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record
- `weeks/`: one page per week the record lists, every row with its source and its page in the record
- `companies/`: one page per company the record lists, the same way
- `models/`: one page per model the record lists, the same way

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 3,589 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 3,589 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 3,589 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 3,589 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 3,448 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 603 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 603 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 3,022 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 3,589 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 3,589 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 3,589 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 3,589 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 3,589 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 329 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 555 | The ids of the platforms the row's subject or what_shipped names (the subject alone for MCP servers), or whose own source is a model's page on the platform whose file list held weight files when last read (read when the row is admitted and again every day), read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners, except Google AI Studio, Microsoft Foundry and Google Antigravity, where their owners' rows count too; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 3,589 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 3,589 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
