# Start with Hayate

This is the canonical first path. It produces a tested application with one
core for ASGI/SQLite and Cloudflare Workers/D1, plus OpenAPI 3.1.1, MCP
2026-07-28, Cloudflare Access integration, checked SQL, and production
middleware.

Install [uv](https://docs.astral.sh/uv/), then run:

```sh
uvx --refresh --from create-hayate==0.12.0 create-hayate my-app --template workers --preset production
cd my-app
uv sync
test -f uv.lock
uv sync --locked
uv run pytest
uv run ruff check .
uv run python scripts/check_sql_contracts.py
```

This exact command sequence is executed from a clean temporary directory in
the documentation CI. The first `uv sync` creates `uv.lock`; commit that file
and use `uv sync --locked` in application CI. The generated `.dev.vars` is a
local-only, ignored development identity configuration.

## Understand the generated shape

- `src/app.py` is the portable application core.
- Uvicorn supplies the ASGI adapter and local SQLite supplies development
  storage.
- Cloudflare workerd supplies the Workers adapter and a D1 binding. ASGI is not
  required on Cloudflare.
- HTTP and MCP receive the same request identity and call the same checked
  storage layer.
- The default Workers export is the feature-complete `WorkerEntrypoint` class,
  which preserves RPC and class handlers such as `scheduled`.
- The optional global export is an HTTP-only compatibility mode. Do not use it
  when the service contract includes named RPC methods or scheduled handlers.

## Continue to production

Do not deploy placeholder tenancy, D1, CORS, or rate-limit values. Compare the
generated project with the public [production golden app](https://github.com/hayatepy/golden-app),
then complete its [production checklist](https://github.com/hayatepy/golden-app/blob/main/PRODUCTION.md)
and review its [trust boundaries](https://github.com/hayatepy/golden-app/blob/main/ARCHITECTURE.md).

For a conventional server deployment, keep the same application core and
choose a verified identity middleware appropriate to that environment.
Cloudflare Access verification in the production preset is Workers-specific.

Next: [choose ecosystem capabilities by outcome](PRODUCTION.md) or inspect the
[tested compatibility snapshot](COMPATIBILITY.md).
