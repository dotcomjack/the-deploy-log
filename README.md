# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of October 12, 2026](https://deployedbyai.com/log/week/2026-W42/)

235 rows are listed for October 12 to 18, 2026 in The Deploy Log, from 68 companies. Amazon Web Services shipped the most, 21 rows, then Anthropic with 16. 235 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, October 18, 2026, and was still in progress when this file was built on October 16, 2026 (ET).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-10-16](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-10-16), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

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

## The record

The record holds 1,617 rows, 1,098 with a publisher's date, 519 placed by their edition, from 122 companies. Rows are listed from September 17, 2025 to October 16, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on October 16, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 69 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 28 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 2 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 56 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 14 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 1,097 | 876 | 221 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 307 | 169 | 138 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 44 | 23 | 21 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 34 | 23 | 11 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 7 | 7 | 0 |
| Leads (filed in no lane) | 128 | 0 | 128 |
| Total | 1,617 | 1,098 | 519 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 253 | 66 | 2025-09-18 | 2026-10-15 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 189 | 85 | 2025-09-25 | 2026-10-15 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 112 | 69 | 2025-10-16 | 2026-10-15 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 100 | 96 | 2026-09-16 | 2026-10-15 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 88 | 39 | 2025-09-17 | 2026-10-16 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 66 | 60 | 2026-09-17 | 2026-10-16 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 40 | 40 | 2026-09-17 | 2026-10-15 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 40 | 39 | 2026-09-20 | 2026-10-15 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 39 | 39 | 2026-09-22 | 2026-10-15 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 38 | 30 | 2026-08-13 | 2026-10-15 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 35 | 25 | 2026-08-28 | 2026-10-15 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 34 | 8 | 2025-10-25 | 2026-10-14 |
| [Google Research](https://deployedbyai.com/log/company/de1f4bdca32b/google-research/) | 33 | 20 | 2025-10-16 | 2026-07-09 |
| [Notion](https://deployedbyai.com/log/company/4751f64514b9/notion/) | 33 | 21 | 2025-11-10 | 2026-08-07 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 28 | 22 | 2026-09-23 | 2026-10-14 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) (in progress) | 2026-10-12 to 2026-10-18 | 235 | 235 | 0 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 308 | 290 | 18 |
| [2026-W39](https://deployedbyai.com/log/week/2026-W39/) | 2026-09-21 to 2026-09-27 | 134 | 123 | 11 |
| [2026-W38](https://deployedbyai.com/log/week/2026-W38/) | 2026-09-14 to 2026-09-20 | 39 | 19 | 20 |
| [2026-W37](https://deployedbyai.com/log/week/2026-W37/) | 2026-09-07 to 2026-09-13 | 5 | 0 | 5 |
| [2026-W36](https://deployedbyai.com/log/week/2026-W36/) | 2026-08-31 to 2026-09-06 | 16 | 4 | 12 |
| [2026-W35](https://deployedbyai.com/log/week/2026-W35/) | 2026-08-24 to 2026-08-30 | 16 | 6 | 10 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 640 | 602 | 38 |
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
| Total | 1,617 | 1,098 | 519 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-10-16 | [Netlify](https://deployedbyai.com/log/company/7adffd5ee2c8/netlify/) | [Netlify Support Hub](https://deployedbyai.com/log/34de46f7fffa/netlify-support-hub/?k=data) | [Netlify, Netlify Support Hub](https://www.netlify.com/changelog/2026-10-16-support-tickets-in-the-netlify-ui/) |
| 2026-10-16 | [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | [GitHub Copilot CLI v1.0.99-3](https://deployedbyai.com/log/23340b464bf7/github-copilot-cli-v1-0-99-3/?k=data) | [GitHub, GitHub Copilot CLI v1.0.99-3](https://github.com/github/copilot-cli/releases/tag/v1.0.99-3) |
| 2026-10-16 | Tencent | [Qwen3-8B-DSpine-b16](https://deployedbyai.com/log/9993593633aa/qwen3-8b-dspine-b16/?k=data) | [Tencent, Qwen3-8B-DSpine-b16](https://huggingface.co/tencent/Qwen3-8B-DSpine-b16) |
| 2026-10-16 | [Langfuse](https://deployedbyai.com/log/company/52628f607201/langfuse/) | [Langfuse v4.63.0](https://deployedbyai.com/log/0db02c280cad/langfuse-v4-63-0/?k=data) | [Langfuse, Langfuse v4.63.0](https://github.com/langfuse/langfuse/releases/tag/v4.63.0) |
| 2026-10-16 | [Shopify](https://deployedbyai.com/log/company/24b3b60d3d0e/shopify/) | [Checkout MCP and Cart MCP UCP consent](https://deployedbyai.com/log/be872448a9d0/checkout-mcp-and-cart-mcp-ucp-consent/?k=data) | [Shopify, Checkout MCP and Cart MCP UCP consent](https://shopify.dev/changelog/checkout-mcp-and-cart-mcp-now-support-ucp-buyer-consent) |
| 2026-10-16 | [Agno](https://deployedbyai.com/log/company/18c156da0579/agno/) | [Agno v3.1.4](https://deployedbyai.com/log/2dab8c7a2f0a/agno-v3-1-4/?k=data) | [Agno, Agno v3.1.4](https://github.com/agno-agi/agno/releases/tag/v3.1.4) |
| 2026-10-16 | Red Hat | [MCP gateway for OpenShift](https://deployedbyai.com/log/7b0d2065b524/mcp-gateway-for-openshift/?k=data) | [Red Hat, MCP gateway for OpenShift](https://www.redhat.com/en/blog/model-context-protocol-gateway-red-hat-openshift-now-generally-available) |
| 2026-10-16 | [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | [Transformers v5.20.1](https://deployedbyai.com/log/5c9cfadfe879/transformers-v5-20-1/?k=data) | [Hugging Face, Transformers v5.20.1](https://github.com/huggingface/transformers/releases/tag/v5.20.1) |
| 2026-10-16 | [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | [Beam](https://deployedbyai.com/log/2b0fd10110af/beam/?k=data) | [Hugging Face, Beam](https://huggingface.co/blog/reflection-beam) |
| 2026-10-16 | [Open WebUI](https://deployedbyai.com/log/company/d493030271cb/open-webui/) | [Open WebUI v0.12.3](https://deployedbyai.com/log/e93698ebc7fe/open-webui-v0-12-3/?k=data) | [Open WebUI, Open WebUI v0.12.3](https://github.com/open-webui/open-webui/releases/tag/v0.12.3) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 1,617 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 1,617 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 1,617 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 1,617 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 1,489 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 519 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 519 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 1,098 | The date the publisher's own page gives, as YYYY-MM-DD, on a row no edition carries. Null on a row an edition carries, which is dated by its edition. |
| `date_label` | 1,617 | The row's date in words: Published and the publisher's date where the row has one; otherwise Edition, the edition's number, a comma and the edition's date. |
| `source` | 1,617 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 1,617 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 1,617 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 1,617 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 153 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 192 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 1,617 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
