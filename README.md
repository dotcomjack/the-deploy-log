# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of October 19, 2026](https://deployedbyai.com/log/week/2026-W43/)

7 rows are listed for October 19 to 25, 2026 in The Deploy Log, from 6 companies. Qwen shipped the most, 2 rows, then Cloudflare, Docker, Microsoft Azure, OpenAI and Qodo with 1 each. 7 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, October 25, 2026, and was still in progress when this file was built on October 19, 2026 (ET).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-10-18](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-10-18), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

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
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "Qwen", "limit": 3}}}'
```

## The record

The record holds 1,685 rows, 1,154 with a publisher's date, 531 placed by their edition, from 125 companies. Rows are listed from September 17, 2025 to October 19, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on October 19, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 69 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 28 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 2 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 57 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 14 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 1,154 | 928 | 226 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 317 | 175 | 142 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 44 | 23 | 21 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 33 | 21 | 12 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 7 | 7 | 0 |
| Leads (filed in no lane) | 130 | 0 | 130 |
| Total | 1,685 | 1,154 | 531 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 257 | 70 | 2025-09-18 | 2026-10-17 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 209 | 104 | 2025-09-25 | 2026-10-19 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 115 | 71 | 2025-10-16 | 2026-10-18 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 102 | 97 | 2026-09-16 | 2026-10-16 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 88 | 39 | 2025-09-17 | 2026-10-16 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 68 | 61 | 2026-09-17 | 2026-10-16 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 43 | 43 | 2026-09-17 | 2026-10-16 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 43 | 42 | 2026-09-20 | 2026-10-16 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 41 | 41 | 2026-09-22 | 2026-10-16 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 39 | 31 | 2026-08-13 | 2026-10-19 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 36 | 24 | 2026-08-28 | 2026-10-15 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 34 | 8 | 2025-10-25 | 2026-10-14 |
| [Google Research](https://deployedbyai.com/log/company/de1f4bdca32b/google-research/) | 33 | 20 | 2025-10-16 | 2026-07-09 |
| [Notion](https://deployedbyai.com/log/company/4751f64514b9/notion/) | 33 | 21 | 2025-11-10 | 2026-08-07 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 29 | 22 | 2026-09-23 | 2026-10-14 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) (in progress) | 2026-10-19 to 2026-10-25 | 7 | 7 | 0 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 296 | 284 | 12 |
| [2026-W41](https://deployedbyai.com/log/week/2026-W41/) | 2026-10-05 to 2026-10-11 | 273 | 253 | 20 |
| [2026-W40](https://deployedbyai.com/log/week/2026-W40/) | 2026-09-28 to 2026-10-04 | 308 | 290 | 18 |
| [2026-W39](https://deployedbyai.com/log/week/2026-W39/) | 2026-09-21 to 2026-09-27 | 134 | 123 | 11 |
| [2026-W38](https://deployedbyai.com/log/week/2026-W38/) | 2026-09-14 to 2026-09-20 | 39 | 19 | 20 |
| [2026-W37](https://deployedbyai.com/log/week/2026-W37/) | 2026-09-07 to 2026-09-13 | 5 | 0 | 5 |
| [2026-W36](https://deployedbyai.com/log/week/2026-W36/) | 2026-08-31 to 2026-09-06 | 16 | 4 | 12 |

## Rows per month

A row counts in the month of its listed date, as above.

| Month | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 708 | 658 | 50 |
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
| Total | 1,685 | 1,154 | 531 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-10-19 | [Microsoft Azure](https://deployedbyai.com/log/company/1d25b33b529f/microsoft-azure/) | [Browser automation tool in Microsoft Foundry](https://deployedbyai.com/log/ebb2c3651cdb/browser-automation-tool-in-microsoft-foundry/?k=data) | [Microsoft Azure, Browser automation tool in Microsoft Foundry](https://devblogs.microsoft.com/foundry/browser-automation-tool-ga/) |
| 2026-10-19 | [Docker](https://deployedbyai.com/log/company/33dab0a853cb/docker/) | [Docker Agent v1.151.0](https://deployedbyai.com/log/74e223e11b14/docker-agent-v1-151-0/?k=data) | [Docker, Docker Agent v1.151.0](https://github.com/docker/docker-agent/releases/tag/v1.151.0) |
| 2026-10-19 | Qodo | [Qodo v3.1](https://deployedbyai.com/log/24a5b66b0c56/qodo-v3-1/?k=data) | [Qodo, Qodo v3.1](https://www.qodo.ai/blog/latest-updates-to-qodo-october-2026/) |
| 2026-10-19 | [Qwen](https://deployedbyai.com/log/company/abb905e81511/qwen/) | [Qwen Code Desktop v0.25.3](https://deployedbyai.com/log/13e438c9d287/qwen-code-desktop-v0-25-3/?k=data) | [Qwen, Qwen Code Desktop v0.25.3](https://github.com/QwenLM/qwen-code/releases/tag/desktop-v0.25.3) |
| 2026-10-19 | [Qwen](https://deployedbyai.com/log/company/abb905e81511/qwen/) | [Qwen SDK TypeScript v0.1.21](https://deployedbyai.com/log/0df94239df4e/qwen-sdk-typescript-v0-1-21/?k=data) | [Qwen, Qwen SDK TypeScript v0.1.21](https://github.com/QwenLM/qwen-code/releases/tag/sdk-typescript-v0.1.21) |
| 2026-10-19 | [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | [Cloud Workload Security](https://deployedbyai.com/log/0e75624c82b9/cloud-workload-security/?k=data) | [Cloudflare, Cloud Workload Security](https://developers.cloudflare.com/changelog/post/2026-10-19-cloud-workload-security-beta/) |
| 2026-10-18 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [openai-java v4.86.0](https://deployedbyai.com/log/18719bed4645/openai-java-v4-86-0/?k=data) | [OpenAI, openai-java v4.86.0](https://github.com/openai/openai-java/releases/tag/v4.86.0) |
| 2026-10-18 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [openai-node v7.39.0](https://deployedbyai.com/log/7ef7560c9a73/openai-node-v7-39-0/?k=data) | [OpenAI, openai-node v7.39.0](https://github.com/openai/openai-node/releases/tag/v7.39.0) |
| 2026-10-18 | [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | [OpenAI Go SDK v3.82.0](https://deployedbyai.com/log/ffba411c8fbd/openai-go-sdk-v3-82-0/?k=data) | [OpenAI, OpenAI Go SDK v3.82.0](https://github.com/openai/openai-go/releases/tag/v3.82.0) |
| 2026-10-18 | [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | [Claude Agent SDK TypeScript v0.3.303](https://deployedbyai.com/log/b2f361084300/claude-agent-sdk-typescript-v0-3-303/?k=data) | [Anthropic, Claude Agent SDK TypeScript v0.3.303](https://github.com/anthropics/claude-agent-sdk-typescript/releases/tag/v0.3.303) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 1,685 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 1,685 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 1,685 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 1,685 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 1,555 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 531 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 531 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 1,154 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 1,685 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. |
| `source` | 1,685 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 1,685 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 1,685 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 1,685 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 155 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 202 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 1,685 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
