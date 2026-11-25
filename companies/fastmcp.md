# FastMCP in The Deploy Log

16 rows in The Deploy Log are filed under FastMCP. Every one carries a publisher's date, from September 25, 2026 to November 25, 2026.

The same rows are on [the FastMCP page of the record](https://deployedbyai.com/log/company/11b827318913/fastmcp/?k=repo).

## November 2026

| Date | Row | What shipped | Source |
|---|---|---|---|
| 2026-11-25 | [FastMCP v4.2.6](https://deployedbyai.com/log/39cd94653d20/fastmcp-v4-2-6/?k=repo) | FastMCP 4.2.6 adds an experimental CodeModeClient that runs CodeMode client-side across servers, moves events to the fastmcp-events package as Pydantic models, and drops Authlib. | [FastMCP, FastMCP v4.2.6](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.6) |
| 2026-11-23 | [FastMCP v4.2.5](https://deployedbyai.com/log/f074815c069c/fastmcp-v4-2-5/?k=repo) | FastMCP v4.2.5 serves subscriptions/listen on 2026-07-28 connections by default, adds opt-in UsageMiddleware recording per-user per-tool OpenTelemetry histograms, and an experimental Events extension. | [FastMCP, FastMCP v4.2.5](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.5) |
| 2026-11-21 | [FastMCP v4.2.4](https://deployedbyai.com/log/cd520266684f/fastmcp-v4-2-4/?k=repo) | FastMCP v4.2.4 fixes a race where concurrent token requests could redeem one OAuth proxy authorization code or refresh token twice, and hides only the failing tool on a bad transform. | [FastMCP, FastMCP v4.2.4](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.4) |
| 2026-11-20 | [FastMCP 4.2.3](https://deployedbyai.com/log/7f6c1bc660a2/fastmcp-4-2-3/?k=repo) | FastMCP 4.2.3 adds an opt-in parent\_task\_spans setting nesting background task worker spans inside the submitting tools/call request, plus three output schema conversion fixes. | [FastMCP, FastMCP 4.2.3](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.3) |
| 2026-11-18 | [FastMCP v4.2.2](https://deployedbyai.com/log/1bd1eb1b1bf0/fastmcp-v4-2-2/?k=repo) | FastMCP 4.2.2 fixes skills discovery for tool-only clients so skills are listed whenever their files are served. | [FastMCP, FastMCP v4.2.2](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.2) |
| 2026-11-17 | [FastMCP 4.2.1](https://deployedbyai.com/log/03c3b9272f57/fastmcp-4-2-1/?k=repo) | FastMCP 4.2.1 ships OAuth and token handling fixes, including rejecting JWTs before their nbf and raising the opentelemetry-api floor. | [FastMCP, FastMCP 4.2.1](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.1) |
| 2026-11-13 | [FastMCP 4.2](https://deployedbyai.com/log/69f1488a57f0/fastmcp-4-2/?k=repo) | FastMCP 4.2 lets servers serve skills via SkillCatalogProvider or SkillsDirectoryProvider, with Client.read\_skill() and to\_directory() for clients. | [FastMCP, FastMCP 4.2](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.2.0) |
| 2026-11-10 | [FastMCP v4.1.7](https://deployedbyai.com/log/f95c6c04621d/fastmcp-v4-1-7/?k=repo) | FastMCP 4.1.7 backports 42 fixes from the 4.2 line. | [FastMCP, FastMCP v4.1.7](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.7) |
| 2026-11-10 | [FastMCP v4.1.8](https://deployedbyai.com/log/196f58e9b890/fastmcp-v4-1-8/?k=repo) | FastMCP 4.1.8 backports 28 fixes from the 4.2 line. | [FastMCP, FastMCP v4.1.8](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.8) |
| 2026-11-03 | [FastMCP v4.1.6](https://deployedbyai.com/log/3985dd4b3d8a/fastmcp-v4-1-6/?k=repo) | ClientGroup keeps tool routes after group context exits. | [FastMCP, FastMCP v4.1.6](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.6) |

## October 2026

| Date | Row | What shipped | Source |
|---|---|---|---|
| 2026-10-26 | [FastMCP v4.1.4](https://deployedbyai.com/log/ae5a29e868b5/fastmcp-v4-1-4/?k=repo) | FastMCP v4.1.4 fixes CLI transport preservation, session visibility, OAuth identity assertions, and adds redis-py credential provider support. | [FastMCP, FastMCP v4.1.4](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.4) |
| 2026-10-20 | [FastMCP v3.4.10](https://deployedbyai.com/log/bdcca541c4bb/fastmcp-v3-4-10/?k=repo) | FastMCP v3.4.10 backports authorization checks after transforms and prevents denied concrete resources from being served by matching templates. | [FastMCP, FastMCP v3.4.10](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.10) |
| 2026-10-20 | [FastMCP v3.4.11](https://deployedbyai.com/log/d17e139dacd9/fastmcp-v3-4-11/?k=repo) | FastMCP v3.4.11 requires certifi 2026.10.19 or later for its HTTP stack and certifi-backed integrations. | [FastMCP, FastMCP v3.4.11](https://github.com/PrefectHQ/fastmcp/releases/tag/v3.4.11) |
| 2026-10-20 | [FastMCP v4.1.2](https://deployedbyai.com/log/e28b7b85f062/fastmcp-v4-1-2/?k=repo) | FastMCP v4.1.2 applies component authorization after transforms and prevents denied resources from falling through matching templates. | [FastMCP, FastMCP v4.1.2](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.2) |
| 2026-10-08 | [FastMCP v4.1.0](https://deployedbyai.com/log/44c900d01ff3/fastmcp-v4-1-0/?k=repo) | FastMCP v4.1.0 released with fixes across OpenAPI, proxies, auth, tasks, CLI, and full Python 3.15 support. | [FastMCP, FastMCP v4.1.0](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.1.0) |

## September 2026

| Date | Row | What shipped | Source |
|---|---|---|---|
| 2026-09-25 | [FastMCP v4.0.10](https://deployedbyai.com/log/1e7f0a3eeb39/fastmcp-v4-0-10/?k=repo) | Task-enabled tools now work behind search transforms and CodeMode. | [FastMCP, FastMCP v4.0.10](https://github.com/PrefectHQ/fastmcp/releases/tag/v4.0.10) |
