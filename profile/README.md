# hayatepy

**Web-standards-first Python for applications that run across ASGI, Cloudflare
Workers, and AWS Lambda.**

Hayate keeps one WHATWG `Request`/`Response` application core while runtime
adapters and optional features are mounted around it. Use the same application
logic on a conventional Python server or directly inside Cloudflare workerd.

## Start here

1. Follow the [single quickstart](https://github.com/hayatepy/.github/blob/main/docs/START.md).
2. Use the [executable production golden app](https://github.com/hayatepy/golden-app)
   for Cloudflare Access, OpenAPI, MCP, checked SQL, SQLite/D1, and deployment.
3. Check the [generated compatibility evidence](https://github.com/hayatepy/.github/blob/main/docs/COMPATIBILITY.md)
   before selecting versions or runtimes.

Building a real API, MCP backend, or Workers application? Help shape the v1
contract through the bounded
[design-partner program](https://github.com/hayatepy/.github/blob/main/docs/DESIGN_PARTNERS.md).

## Why Hayate

Hayate is strongest when one Python application must combine typed HTTP,
MCP, authorization, and checked data access across conventional ASGI servers
and native Cloudflare Workers.

The recorded 2026-07-27 same-workload HTTP baseline measured:

| Boundary | Hayate 0.12.1 | FastAPI 0.140.0 | Django 6.0.7 | Hono 4.12.32 |
|---|---:|---:|---:|---:|
| Cold start | 130.3 ms | 220.5 ms | 155.5 ms | **55.0 ms** |
| Production packages | 5 | 13 | 6 | **2** |
| gzip payload | 287.5 KiB | 2,802.1 KiB | 5,147.1 KiB | **281.5 KiB** |
| Throughput | 13,995 req/s | 10,161 req/s | 2,719 req/s | **63,198 req/s** |
| Common HTTP contract | **14/14** | 12/14 | 12/14 | 12/14 |

On this workload Hayate delivered 1.38x FastAPI's and 5.15x Django's
throughput. Hono delivered 4.52x Hayate's throughput and retained the best
startup result. The 14-point contract is a shared-workload result, not a
universal standards score.

Feature breadth is evaluated separately and without a weighted winner. Hayate
is advantaged for a portable Python agent API; FastAPI remains competitive for
conventional typed Python APIs; Django retains integrated admin, ORM,
migrations, forms, and templates; Hono retains broad JavaScript-runtime
portability and route-inferred TypeScript RPC.

Read the
[reproducible benchmark](https://github.com/hayatepy/hayate/blob/main/docs/benchmarks.md)
and the dated, source-backed
[capability matrix](https://github.com/hayatepy/hayate/blob/main/docs/capabilities.md)
for methodology, raw artifacts, profile verdicts, and limitations.

## Choose by outcome

| I want to… | Start with |
|---|---|
| Build a web API on ASGI, Workers, or Lambda | [`hayate`](https://github.com/hayatepy/hayate) |
| Generate OpenAPI 3.1 and typed clients | [`hayate-openapi`](https://github.com/hayatepy/hayate-openapi) |
| Expose MCP 2025-11-25 tools | [`hayate-mcp`](https://github.com/hayatepy/hayate-mcp) |
| Add sessions, API keys, OAuth, or an authorization server | [`hayate-auth`](https://github.com/hayatepy/hayate-auth) |
| Use checked SQL with PostgreSQL, SQLite, or D1 | [`hayate-sql`](https://github.com/hayatepy/hayate-sql) |
| Make portable outbound requests | [`hayate-fetch`](https://github.com/hayatepy/hayate-fetch) |
| Generate an integrated application | [`create-hayate`](https://github.com/hayatepy/create-hayate) |

## Evidence, not platform claims

- The golden app runs direct tests, a real Uvicorn/SQLite flow, and a real
  workerd/D1 flow. HTTP, identity, OpenAPI, and MCP share one application core.
- The core compatibility gate installs an unpublished Hayate wheel into auth,
  fetch, MCP, OpenAPI, and generated application repositories before release.
- The feature-complete Workers default is a `WorkerEntrypoint` class. The
  optional global handler is an explicitly HTTP-only compatibility mode.
- Public releases include locked inputs, SPDX SBOMs, and GitHub attestations.

All packages are pre-1.0. Use the compatibility page for the exact evidence
snapshot rather than assuming every pre-1.0 line can be mixed freely.

## Contributing and security

See the organization-wide
[contributing guide](https://github.com/hayatepy/.github/blob/main/CONTRIBUTING.md).
Report vulnerabilities privately through the affected repository's
**Security → Report a vulnerability** flow.
