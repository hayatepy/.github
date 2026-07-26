#!/usr/bin/env bash
set -euo pipefail

generated_project_root="$(mktemp -d)"
cd "${generated_project_root}"

uvx --refresh --from create-hayate==0.4.0 \
  create-hayate my-app --template workers --preset production
cd my-app
uv sync
test -f uv.lock
uv sync --locked
uv run pytest
uv run ruff check .
uv run python scripts/check_sql_contracts.py

echo "canonical start path passed in ${generated_project_root}/my-app"
