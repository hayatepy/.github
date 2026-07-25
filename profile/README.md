# hayatepy

**Web-standards-first Python for applications that run across ASGI, Cloudflare
Workers, and AWS Lambda.**

hayate uses WHATWG `Request`, `Response`, `Headers`, `URL`, and `URLPattern` as
its public surface. The application core is a pure
`fetch(Request) -> Response` function; runtimes and ecosystem features are
mounted around that core.

```python
from hayate import Hayate

app = Hayate()

@app.get("/hello/:name")
async def hello(c):
    return c.json({"hello": c.req.param("name")})
```

## Start here

```sh
uvx create-hayate my-app
cd my-app
uv run pytest
uv run uvicorn app:app --reload
```

- [Documentation](https://hayatepy.github.io/hayate/)
- [Core repository](https://github.com/hayatepy/hayate)
- [PyPI](https://pypi.org/project/hayate/)

## Ecosystem and compatibility

| Package | Current line | Role | Runtime requirements |
| --- | ---: | --- | --- |
| [`hayate`](https://github.com/hayatepy/hayate) | 0.10.x | Core framework and runtime adapters | Python 3.12+ |
| [`hayate-auth`](https://github.com/hayatepy/hayate-auth) | 0.9.x | Authentication and OAuth 2.1 authorization server | `hayate>=0.8`, `hayate-fetch>=0.1.2` |
| [`hayate-mcp`](https://github.com/hayatepy/hayate-mcp) | 0.10.x | MCP 2025-11-25 transport, request context, and OAuth resource server | `hayate>=0.8`; official SDK on CPython, schema-validated runtime on Workers |
| [`hayate-openapi`](https://github.com/hayatepy/hayate-openapi) | 0.3.x | OpenAPI 3.1 generation and hardened interactive docs | `hayate>=0.8` |
| [`hayate-fetch`](https://github.com/hayatepy/hayate-fetch) | 0.1.x | Client-side WHATWG fetch for CPython and Workers | `hayate>=0.8` |
| [`create-hayate`](https://github.com/hayatepy/create-hayate) | 0.2.x | Tested API, Workers, and MCP 2025-11-25 scaffolds | Python 3.12+ |

## What is verified

- The documented WHATWG URL scope passes
  [306 of 306 vendored web-platform-tests](https://hayatepy.github.io/hayate/conformance/).
- `hayate-mcp` negotiates MCP 2025-11-25 on both ASGI and Cloudflare Workers.
  Its Workers gate boots real workerd and completes `initialize`, `tools/list`,
  and `tools/call` with the official SDK client.
- [FolioMCP](https://github.com/yhay81/foliomcp-api) uses the published
  `hayate-mcp` Workers runtime with its existing Cloudflare Access identity,
  D1, R2, Queue, and rate-limit bindings. Its CI repeats the full workerd path.
- `create-hayate` generates an auth-optional MCP project that is tested over
  both real ASGI HTTP and local workerd.
- The primary end-to-end path — an MCP server and its OAuth authorization
  server in one application — has been exercised over real HTTP on ASGI,
  local workerd, and a deployed Cloudflare Python Worker with D1.
- Public releases are built by protected tag workflows and include an SPDX
  SBOM plus GitHub build and SBOM attestations.

## Project principles

- **Standards first.** Public behavior names the WHATWG, IETF, W3C, or MCP
  specification it follows.
- **Evidence driven.** Runtime support and performance claims are backed by
  repeatable tests or recorded measurements.
- **Small cores.** Optional resources are injected through protocols instead
  of hidden global integrations.
- **Portable by construction.** Application code should not change when the
  runtime adapter changes.

Every package is still pre-1.0. Public APIs may move before 1.0; each
repository documents its current support and security posture.

## Contributing and security

See the organization-wide [contributing guide](../CONTRIBUTING.md). Report
security vulnerabilities privately through the affected repository's
**Security → Report a vulnerability** flow; do not open a public issue.
