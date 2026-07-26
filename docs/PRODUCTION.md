# Production path

The [golden app](https://github.com/hayatepy/golden-app) is the only canonical
integrated production reference. It deliberately uses a generic TODO model and
contains no private FolioMCP source, tenant policy, credentials, or product
data.

## Build from outcomes

| Outcome | Production reference |
|---|---|
| Portable HTTP application | Hayate core in the golden app |
| OpenAPI and TypeScript client | Checked `openapi.json` and `client/api-types.ts` |
| Agent tools | MCP 2025-11-25 initialize and `tools/call` E2E |
| Request identity | Fail-closed Cloudflare Access JWT/JWKS verification |
| Data access | Migration-checked SQL over SQLite locally and D1 on Workers |
| Browser boundary | Exact-origin CORS, security headers, and a 1 MiB body limit |
| Abuse control | Identity-keyed native Workers rate-limit binding |
| Supply chain | Locked dependencies, dependency audit, workflow audit, and pinned actions |

## Deployment gate

Before traffic reaches an application derived from the reference:

- replace Access domain and audience placeholders;
- replace D1 IDs and apply migrations as a separate operator action;
- allocate account-unique rate-limit namespaces;
- set exact HTTPS CORS origins;
- define secret, telemetry, retention, migration, rollback, and incident owners;
- exercise health, identity, CRUD, OpenAPI, and MCP through the deployed Access
  boundary;
- record the exact compatibility snapshot and release attestations used.

The golden repository executes the direct, ASGI, and workerd paths on every
change. Its [compatibility artifacts](https://github.com/hayatepy/golden-app/blob/main/COMPATIBILITY.md)
are generated from the checked lock and runtime manifests.
