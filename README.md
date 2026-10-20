# The Deploy Log

Every deployment deployedbyai has carried. Every item sourced to the publisher's own page.

## [What shipped in AI, week of October 19, 2026](https://deployedbyai.com/log/week/2026-W43/)

42 rows are listed for October 19 to 25, 2026 in The Deploy Log, from 25 companies. GitHub shipped the most, 5 rows, then Amazon Web Services and Cloudflare with 3 each. 42 carry a publisher's date and 0 are placed by their edition. The week runs to Sunday, October 25, 2026, and was still in progress when this file was built on October 20, 2026 (ET).

## Load it

deployedbyai.com refuses a request that carries Python's default User-Agent, which `pandas.read_csv` sends by default, so the Python example reads this repository's copy, refreshed daily.

```sh
curl -sO https://deployedbyai.com/log/data.csv
```

```python
import pandas as pd

rows = pd.read_csv("https://raw.githubusercontent.com/dotcomjack/the-deploy-log/main/data.csv")
```

The newest dated release, [2026-10-20](https://github.com/dotcomjack/the-deploy-log/releases/tag/2026-10-20), carries `data.csv` and `data.json` as files; every release is at https://github.com/dotcomjack/the-deploy-log/releases

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
  -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "search_deployments", "arguments": {"query": "GitHub", "limit": 3}}}'
```

## The record

The record holds 1,721 rows, 1,190 with a publisher's date, 531 placed by their edition, from 125 companies. Rows are listed from September 17, 2025 to October 20, 2026, each by its publisher's date or, where the record carries none, its edition's date. The newest row entered the record on October 20, 2026 (ET). Every row carries `source_url`, the publisher's own page, and `record_url`, its page in the record at https://deployedbyai.com/log/

## Indexes

- [The Deploy Log](https://deployedbyai.com/log/)
- [Companies](https://deployedbyai.com/log/company/): 72 pages listed in the record's sitemap
- [Models](https://deployedbyai.com/log/model/): 28 pages listed in the record's sitemap
- [Platforms](https://deployedbyai.com/log/platform/): 2 pages listed in the record's sitemap
- [Week by week](https://deployedbyai.com/log/week/): 57 pages listed in the record's sitemap
- [Month by month](https://deployedbyai.com/log/month/): 14 pages listed in the record's sitemap

## Rows by lane

Each row is filed in one of 5 lanes, except an edition's lead, which is filed in no lane.

| Lane | Rows | With a publisher's date | Placed by their edition |
|---|---:|---:|---:|
| [Tools and products](https://deployedbyai.com/log/lane/tools_products/) | 1,186 | 960 | 226 |
| [Models and APIs](https://deployedbyai.com/log/lane/models_apis/) | 321 | 179 | 142 |
| [Breakthroughs](https://deployedbyai.com/log/lane/breakthroughs/) | 44 | 23 | 21 |
| [Robotics, hardware and chips](https://deployedbyai.com/log/lane/robotics_hardware_chips/) | 33 | 21 | 12 |
| [Funding and acquisitions](https://deployedbyai.com/log/lane/funding_acquisitions/) | 7 | 7 | 0 |
| Leads (filed in no lane) | 130 | 0 | 130 |
| Total | 1,721 | 1,190 | 531 |

## The 15 companies with the most rows

Ordered by rows, then by name. First and latest are the earliest and newest publisher's date among the company's rows; a row placed by its edition carries no publisher's date in the record and is not in them.

| Company | Rows | With a publisher's date | First | Latest |
|---|---:|---:|---|---|
| [Vercel](https://deployedbyai.com/log/company/0e58b1e76c99/vercel/) | 259 | 72 | 2025-09-18 | 2026-10-19 |
| [OpenAI](https://deployedbyai.com/log/company/8e31fcb84155/openai/) | 209 | 104 | 2025-09-25 | 2026-10-19 |
| [Anthropic](https://deployedbyai.com/log/company/38efbad8cd2a/anthropic/) | 116 | 72 | 2025-10-16 | 2026-10-19 |
| [Amazon Web Services](https://deployedbyai.com/log/company/7bfc964582ce/amazon-web-services/) | 106 | 101 | 2026-09-16 | 2026-10-19 |
| [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | 90 | 41 | 2025-09-17 | 2026-10-20 |
| [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | 73 | 66 | 2026-09-17 | 2026-10-20 |
| [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | 44 | 44 | 2026-09-17 | 2026-10-20 |
| [LangChain](https://deployedbyai.com/log/company/2de245dc5d3a/langchain/) | 43 | 42 | 2026-09-20 | 2026-10-16 |
| [Cloudflare](https://deployedbyai.com/log/company/a248aed96312/cloudflare/) | 41 | 33 | 2026-08-13 | 2026-10-19 |
| [Databricks](https://deployedbyai.com/log/company/9def70023d9f/databricks/) | 41 | 41 | 2026-09-22 | 2026-10-16 |
| [Google Workspace](https://deployedbyai.com/log/company/d690a81815c8/google-workspace/) | 38 | 26 | 2026-08-28 | 2026-10-19 |
| [Google DeepMind](https://deployedbyai.com/log/company/c98c3052b742/google-deepmind/) | 34 | 8 | 2025-10-25 | 2026-10-14 |
| [Google Research](https://deployedbyai.com/log/company/de1f4bdca32b/google-research/) | 33 | 20 | 2025-10-16 | 2026-07-09 |
| [Notion](https://deployedbyai.com/log/company/4751f64514b9/notion/) | 33 | 21 | 2025-11-10 | 2026-08-07 |
| [Google](https://deployedbyai.com/log/company/4b181d6cc893/google/) | 29 | 22 | 2026-09-23 | 2026-10-14 |

## Rows per week, the 8 newest ISO weeks

A row counts in the Monday to Sunday week of its listed date: its publisher's date, or its edition's date where the record carries none. The newest week is the one holding the newest listed date.

| Week | Monday to Sunday | Rows | With a publisher's date | Placed by their edition |
|---|---|---:|---:|---:|
| [2026-W43](https://deployedbyai.com/log/week/2026-W43/) (in progress) | 2026-10-19 to 2026-10-25 | 42 | 42 | 0 |
| [2026-W42](https://deployedbyai.com/log/week/2026-W42/) | 2026-10-12 to 2026-10-18 | 297 | 285 | 12 |
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
| [October 2026](https://deployedbyai.com/log/month/2026-10/) | 744 | 694 | 50 |
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
| Total | 1,721 | 1,190 | 531 |

## The 10 rows added most recently

Added is the day the row entered the record, on Eastern Time, not the day the thing shipped.

| Added (ET) | Company | Row | Source |
|---|---|---|---|
| 2026-10-20 | [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | [copilot-cli v1.0.101-1](https://deployedbyai.com/log/7dc348b61c04/copilot-cli-v1-0-101-1/?k=data) | [GitHub, copilot-cli v1.0.101-1](https://github.com/github/copilot-cli/releases/tag/v1.0.101-1) |
| 2026-10-20 | [FastMCP](https://deployedbyai.com/log/company/11b827318913/fastmcp/) | [FastMCP v3.4.10](https://deployedbyai.com/log/bdcca541c4bb/fastmcp-v3-4-10/?k=data) | [FastMCP, FastMCP v3.4.10](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.10) |
| 2026-10-20 | [Mistral](https://deployedbyai.com/log/company/72d07fed89b4/mistral/) | [Mistral Vibe v3.0.1](https://deployedbyai.com/log/3d870764be6f/mistral-vibe-v3-0-1/?k=data) | [Mistral, Mistral Vibe v3.0.1](https://github.com/mistralai/mistral-vibe/releases/tag/v3.0.1) |
| 2026-10-20 | [FastMCP](https://deployedbyai.com/log/company/11b827318913/fastmcp/) | [FastMCP v4.1.2](https://deployedbyai.com/log/e28b7b85f062/fastmcp-v4-1-2/?k=data) | [FastMCP, FastMCP v4.1.2](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.2) |
| 2026-10-20 | [Langfuse](https://deployedbyai.com/log/company/52628f607201/langfuse/) | [Langfuse v4.65.0](https://deployedbyai.com/log/0785c3034393/langfuse-v4-65-0/?k=data) | [Langfuse, Langfuse v4.65.0](https://github.com/langfuse/langfuse/releases/tag/v4.65.0) |
| 2026-10-20 | [GitHub](https://deployedbyai.com/log/company/057e2e5f0d0b/github/) | [Dependabot package manager support](https://deployedbyai.com/log/d389cbca4da8/dependabot-package-manager-support/?k=data) | [GitHub, Dependabot package manager support](https://github.blog/changelog/2026-10-20-dependabot-now-supports-npm-12-pnpm-11-and-12-and-bun-1-4) |
| 2026-10-20 | [Google Cloud](https://deployedbyai.com/log/company/0cea73712411/google-cloud/) | [llm-d 1.0](https://deployedbyai.com/log/d9033e7a5bb1/llm-d-1-0/?k=data) | [Google Cloud, llm-d 1.0](https://cloud.google.com/blog/topics/ai-infrastructure/llm-d-1-0-an-open-source-stack-for-distributed-inference/) |
| 2026-10-20 | [Hugging Face](https://deployedbyai.com/log/company/45f89a539985/hugging-face/) | [PyTorch 2.15 MPS](https://deployedbyai.com/log/5a3d5eb861a6/pytorch-2-15-mps/?k=data) | [Hugging Face, PyTorch 2.15 MPS](https://huggingface.co/blog/mps-pytorch-2-15) |
| 2026-10-20 | [Pydantic](https://deployedbyai.com/log/company/49425b50f21d/pydantic/) | [Pydantic AI v1.107.8](https://deployedbyai.com/log/0f53d0822221/pydantic-ai-v1-107-8/?k=data) | [Pydantic, Pydantic AI v1.107.8](https://github.com/pydantic/pydantic-ai/releases/tag/v1.107.8) |
| 2026-10-20 | [Pydantic](https://deployedbyai.com/log/company/49425b50f21d/pydantic/) | [Pydantic AI v2.58.0](https://deployedbyai.com/log/4a5da3b5c777/pydantic-ai-v2-58-0/?k=data) | [Pydantic, Pydantic AI v2.58.0](https://github.com/pydantic/pydantic-ai/releases/tag/v2.58.0) |

## Files

- `data.csv`: the record, one line per row
- `data.json`: the same rows with this metadata
- `CITATION.cff`: how to cite the record

Both data files are copied daily from https://deployedbyai.com/log/data.csv and https://deployedbyai.com/log/data.json, unchanged.

## Data dictionary

Each field, in the order of `data.csv`'s header, with the number of rows where it is not empty.

| Field | Rows with a value | What it holds |
|---|---:|---|
| `row_key` | 1,721 | The row's key: 12 lowercase hexadecimal characters, drawn at random when the row enters the record and kept for the life of the row. |
| `company` | 1,721 | The name of the company the row is filed under, as its company page names it. |
| `subject` | 1,721 | What the row is about, in a few words: the heading of the row's own page. |
| `what_shipped` | 1,721 | The row's one sentence on what shipped, as its own page prints it. |
| `lane` | 1,591 | The lane the row is filed in: Models and APIs; Tools and products; Robotics, hardware and chips; Breakthroughs; Funding and acquisitions. Null for an edition's lead, which is filed in no lane. |
| `edition_n` | 531 | The number of the edition that carried the row. Null for a row no edition has carried. |
| `edition_date` | 531 | The date of the edition that carried the row, as YYYY-MM-DD. Null for a row no edition has carried. |
| `published_date` | 1,190 | The date the publisher's own page gives, as YYYY-MM-DD, kept when an edition later carries the row. Null where the row has none, as on a row that entered the record with an edition, which is dated by its edition. |
| `date_label` | 1,721 | The row's date in words: Published and the publisher's date on a row no edition has carried; otherwise Edition, the edition's number, a comma and the edition's date. |
| `source` | 1,721 | The source the row cites, in words: the publisher and its page, as the row's source line prints it. |
| `source_url` | 1,721 | The URL of the publisher's own page the row is sourced to. |
| `record_url` | 1,721 | The row's own page on The Deploy Log, with ?k=data, the key that marks a visit as coming from this file. |
| `added_at` | 1,721 | When the row entered the record, an ISO 8601 timestamp in UTC. It is not the day the thing shipped. |
| `models` | 159 | The ids of the AI models the row's subject names, read by the matcher the model pages use, in the order the subject names them: each is the 12 lowercase hexadecimal characters of the model's page, the page at /log/model/ followed by that id. A model has a page only when rows from 2 or more companies name it; one below that still carries its id here, and the week and month pages count it among the models seen for the first time. Empty when the subject names none. In the CSV, the ids joined by semicolons. |
| `platforms` | 211 | The ids of the platforms the row's subject or what_shipped names, read by the matcher the platform pages use, in the order of the record's list of platforms: each is the 12 lowercase hexadecimal characters of the platform's page, the page at /log/platform/ followed by that id. A platform has a page only when 10 or more rows from 2 or more companies name it, 10 or more of them from companies other than its owners; one below that still carries its id here. A row that names a platform did not necessarily ship on it. Empty when the row names none. In the CSV, the ids joined by semicolons. |
| `updated` | 1,721 | When the row was last written, an ISO 8601 timestamp in UTC: the instant it entered the record, or the instant it was last written again, as when an edition that carries it enters the record. Null where the record holds only a day for it. Each page that lists rows gives, as the day it last changed, New York's day of the newest of these among its rows; a row's own page gives that day or the day the row is dated, whichever is later. It is not the day the thing shipped. |

## Cite this

`CITATION.cff` in this repository gives the record's title, author, license and URL.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution: The Deploy Log, deployedbyai, https://deployedbyai.com/log/, licensed CC BY 4.0
