# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of November 9, 2026](https://deployedbyai.com/log/week/2026-W46/)

153 rows are listed for November 9 to 15, 2026 in The Deploy Log, from 47 companies. Anthropic shipped the most, 16 rows, then Amazon Web Services and Databricks with 11 each. 153 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, November 15, 2026, and was still in progress when this file was built on November 11, 2026 (ET).

Every row of this week, with its source: [weeks/2026-W46.md](weeks/2026-W46.md). The record [week by week](weeks/README.md) and [company by company](companies/README.md).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-11-10](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-11-10), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

## API

Two GET endpoints return the whole record, every row in one response. A row's fields are described in the [Data dictionary](#data-dictionary). The record also answers over the Model Context Protocol: see [Ask it from an agent](#ask-it-from-an-agent).

| Method | URL | Content-Type | Returns |
|---|---|---|---|
| GET | https://deployedbyai.com/log/data.json | `application/json; charset=utf-8` | One JSON object, with the keys below |
| GET | https://deployedbyai.com/log/data.csv | `text/csv; charset=utf-8` | The 2,663 rows as CSV, under a header line of the field names |

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
| `count` | number | 2,663, the number of objects in `rows` |
| `rows` | array | 2,663 objects, one per row, each keyed by the names in `fields`, in that order |

Example: the first object in `rows`, as `data.json` served it when this file was built on November 11, 2026 (ET):

```json
{
  "row_key": "8e0c7a228284",
  "company": "Cognition",
  "subject": "Claude Mythos 5.2 in Devin Security",
  "what_shipped": "Claude Mythos 5.2 is available in Devin Security for eligible enterprise customers, with $100M+ in credits offered.",
  "lane": "Tools and products",
  "edition_n": null,
  "edition_date": null,
  "published_date": "2026-11-11",
  "date_label": "Published Wednesday 11 Nov 2026",
  "source": "Cognition, Claude Mythos 5.2 in Devin Security",
  "source_url": "https://devin.ai/blog/claude-mythos-5-2-security",
  "record_url": "https://deployedbyai.com/log/8e0c7a228284/claude-mythos-5-2-in-devin-security/?k=data",
  "added_at": "2026-11-11T00:10:14.544Z",
  "models": [],
  "platforms": [],
  "updated": "2026-11-11T00:10:14.544Z",
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
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "Anthropic", "limit": 3}}}'
```

The response, as the server answered it when this file was built on November 11, 2026 (ET), cut to its first row: left out are 2 more objects in `structuredContent.items` and 2 more lines of `content[0].text`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "resultType": "complete",
    "content": [
      {
        "type": "text",
        "text": "3 row(s) matching the words given.\nDatabricks: Claude Fable 5.2 on Unity Gateway. Anthropic Claude Fable 5.2 is available on Unity Gateway via Foundation Model APIs. Published Monday 9 Nov 2026. Source: https://docs.databricks.com/aws/en/release-notes/product/2026/november#anthropic-claude-fable-52-is-now-available-on-unity-gateway Record: https://deployedbyai.com/log/e2eaaefea693/claude-fable-5-2-on-unity-gateway/?k=mcp"
      }
    ],
    "structuredContent": {
      "items": [
        {
          "id": "e2eaaefea693",
          "company": "Databricks",
          "subject": "Claude Fable 5.2 on Unity Gateway",
          "what_shipped": "Anthropic Claude Fable 5.2 is available on Unity Gateway via Foundation Model APIs.",
          "shipped": "Published Monday 9 Nov 2026",
          "lane": "Tools and products",
          "source": "Databricks, Claude Fable 5.2 on Unity Gateway",
          "source_url": "https://docs.databricks.com/aws/en/release-notes/product/2026/november#anthropic-claude-fable-52-is-now-available-on-unity-gateway",
          "record_url": "https://deployedbyai.com/log/e2eaaefea693/claude-fable-5-2-on-unity-gateway/?k=mcp"
        }
      ]
    }
  }
}
```

## The record

The record holds 2,663 rows, 2,114 with a publisher's date, 549 placed by their edition, from 151 companies. Rows are listed from September 17, 2025 to November 11, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on November 11, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 96 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 32 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 3 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 60 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 15 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 2,000 | 1,761 | 239 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 410 | 267 | 143 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 49 | 35 | 14 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 45 | 24 | 21 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 23 | 23 | 0 |
| Leads (filed in no lane) | 136 | 4 | 132 |
| Total | 2,663 | 2,114 | 549 |

## The 16 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 307 | 113 | 2025-09-18 | 2026-11-10 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 287 | 179 | 2025-09-25 | 2026-11-10 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 206 | 162 | 2025-10-16 | 2026-11-10 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 173 | 167 | 2026-09-16 | 2026-11-11 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 108 | 98 | 2026-09-17 | 2026-11-11 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 100 | 51 | 2025-09-17 | 2026-11-10 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 80 | 80 | 2026-09-17 | 2026-11-10 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 78 | 78 | 2026-09-22 | 2026-11-11 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 78 | 77 | 2026-09-20 | 2026-11-10 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 64 | 56 | 2026-08-13 | 2026-11-09 |
| [NVIDIA](https://deployedbyai.com/log/company/c0c1c2efa10a/nvidia/) | 53 | 47 | 2026-08-20 | 2026-11-10 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 51 | 43 | 2026-09-23 | 2026-11-10 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 50 | 38 | 2026-08-28 | 2026-11-10 |
| [OpenRouter](https://deployedbyai.com/log/company/2cc19bb941af/openrouter/) | 38 | 38 | 2026-09-25 | 2026-11-10 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 36 | 10 | 2025-10-25 | 2026-11-09 |
| [Qwen](https://deployedbyai.com/log/company/abb905e81511/qwen/) | 36 | 36 | 2026-09-29 | 2026-11-10 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W46](https://deployedbyai.com/log/week/2026-W46/) (in progress) | 2026-11-09 to 2026-11-15 | 153 | 153 | 0 |
| [2026-W45](https://deployedbyai.com/log/week/2026-W45/) | 2026-11-02 to 2026-11-08 | 266 | 261 | 5 |
| [2026-W44](https://deployedbyai.com/log/week/2026-W44/) | 2026-10-26 to 2026-11-01 | 246 | 239 | 7 |
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) | 2026-10-19 to 2026-10-25 | 319 | 313 | 6 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 308 | 290 | 18 |
| [2026-W39](https://deployedbyai.com/log/week/2026-W39/) | 2026-09-21 to 2026-09-27 | 134 | 123 | 11 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [November 2026](https://deployedbyai.com/log/month/2026-11/) | 425 | 420 | 5 |
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
| Total | 2,663 | 2,114 | 549 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Genie One Chrome extension](https://deployedbyai.com/log/fec3ec047292/genie-one-chrome-extension/?k=data) | [Databricks, Genie One Chrome extension](https://docs.databricks.com/aws/en/release-notes/product/2026/november#the-genie-one-chrome-extension-is-in-beta) |
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Protobuf text/binary inputs for model serving](https://deployedbyai.com/log/59a180c81145/protobuf-text-binary-inputs-for-model-serving/?k=data) | [Databricks, Protobuf text/binary inputs for model serving](https://docs.databricks.com/aws/en/release-notes/product/2026/november#text-and-binary-inputs-for-protobuf-requests-to-custom-model-serving-endpoints-public-preview) |
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Google Gemini 4 Carbon](https://deployedbyai.com/log/cebf6bbbb261/google-gemini-4-carbon/?k=data) | [Databricks, Google Gemini 4 Carbon](https://docs.databricks.com/aws/en/release-notes/product/2026/november#google-gemini-4-carbon-is-now-available-on-unity-gateway) |
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Context-based ingress policies](https://deployedbyai.com/log/4755c5adb8df/context-based-ingress-policies/?k=data) | [Databricks, Context-based ingress policies](https://docs.databricks.com/aws/en/release-notes/product/2026/november#allow-chatgpt-and-claude-as-partner-platforms-in-context-based-ingress-policies) |
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Genie One desktop app for Windows](https://deployedbyai.com/log/0a9b28602327/genie-one-desktop-app-for-windows/?k=data) | [Databricks, Genie One desktop app for Windows](https://docs.databricks.com/aws/en/release-notes/product/2026/november#the-genie-one-desktop-app-for-windows-is-in-beta) |
| 2026-11-11 | [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | [Feature Views](https://deployedbyai.com/log/21d0f1d67b0a/feature-views/?k=data) | [Databricks, Feature Views](https://docs.databricks.com/aws/en/release-notes/product/2026/november#feature-views-are-now-available-by-default-for-workspaces-with-the-compliance-security-profile-enabled) |
| 2026-11-11 | [llama.cpp](https://deployedbyai.com/log/company/5b11e1c65bdb/llama-cpp/) | [llama.cpp CUDA OCP FP8](https://deployedbyai.com/log/6c6a007a883d/llama-cpp-cuda-ocp-fp8/?k=data) | [llama.cpp, llama.cpp CUDA OCP FP8](https://github.com/ggml-org/llama.cpp/releases/tag/b12284) |
| 2026-11-11 | [inclusionAI](https://deployedbyai.com/log/company/0bf2ab34cf07/inclusionai/) | [ZoomGain-9B and ZoomGain-4B](https://deployedbyai.com/log/a18f93946c66/zoomgain-9b-and-zoomgain-4b/?k=data) | [inclusionAI, ZoomGain-9B and ZoomGain-4B](https://huggingface.co/inclusionAI/ZoomGain-9B) |
| 2026-11-11 | [inclusionAI](https://deployedbyai.com/log/company/0bf2ab34cf07/inclusionai/) | [SingVL_S1_4B](https://deployedbyai.com/log/dc3963a582f0/singvl-s1-4b/?k=data) | [inclusionAI, SingVL_S1_4B](https://huggingface.co/inclusionAI/SingVL_S1_4B) |
| 2026-11-10 | [Browser Use](https://deployedbyai.com/log/company/2dcdec0423ec/browser-use/) | [browser-use 1.0.2](https://deployedbyai.com/log/2b7a1406f886/browser-use-1-0-2/?k=data) | [Browser Use, browser-use 1.0.2](https://github.com/browser-use/browser-use/releases/tag/1.0.2) |

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
| `row_key` | 2,663 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 2,663 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 2,663 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 2,663 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 2,527 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 569 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 569 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 2,114 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 2,663 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. A row whose publisher's date has not yet come in New York carries, in place of that date, the words its own page prints for it until that day. |
| `source` | 2,663 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 2,663 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 2,663 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 2,663 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 203 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 339 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 2,663 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |
| `kind` | 2,663 | How the row entered the record: backfill, a release read from the publisher's own page and dated by the publisher's date; edition_lead or edition_row, an item a Saturday edition carried, dated by the edition, including a publisher's row an edition later carried, which keeps its published_date. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
