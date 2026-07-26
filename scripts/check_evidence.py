"""Verify vendored golden evidence against its immutable source commit."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.request import urlopen

import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = tomllib.loads(
        (ROOT / "data" / "ecosystem.toml").read_text(encoding="utf-8")
    )
    commit = manifest["sources"]["golden_app"]["commit"]
    url = (
        "https://raw.githubusercontent.com/hayatepy/golden-app/"
        f"{commit}/compatibility.json"
    )
    with urlopen(url, timeout=30) as response:
        upstream = json.load(response)
    local = json.loads(
        (ROOT / "evidence" / "golden-app-compatibility.json").read_text(
            encoding="utf-8"
        )
    )
    if upstream != local:
        raise SystemExit(
            "vendored golden-app compatibility evidence does not match its commit"
        )
    print(f"golden-app evidence matches {commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
