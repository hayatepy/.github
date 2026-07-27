#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
create_hayate_version="$(
  python3 - "${root}/data/ecosystem.toml" <<'PY'
import sys
import tomllib
from pathlib import Path

manifest = tomllib.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
versions = {
    package["name"]: package["version"]
    for package in manifest["packages"]
}
print(versions["create-hayate"])
PY
)"
canonical_command="uvx --refresh --from create-hayate==${create_hayate_version} create-hayate my-app --template workers --preset production"
if ! grep -Fqx "${canonical_command}" "${root}/docs/START.md"; then
  echo "docs/START.md does not contain the canonical create-hayate command" >&2
  exit 1
fi

generated_project_root="$(mktemp -d)"
cd "${generated_project_root}"

uvx --refresh --from "create-hayate==${create_hayate_version}" \
  create-hayate my-app --template workers --preset production
cd my-app
uv sync
test -f uv.lock
uv sync --locked
uv run pytest
uv run ruff check .
uv run python scripts/check_sql_contracts.py

echo "canonical start path passed in ${generated_project_root}/my-app"
