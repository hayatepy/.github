#!/usr/bin/env python3
"""Check public discovery contracts across every Hayate family repository."""

from __future__ import annotations

import io
import re
import sys
import tarfile
import time
import tomllib
import urllib.request
from pathlib import Path, PurePosixPath
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "data" / "public-discovery.toml"
OWNER = "hayatepy"
SCAFFOLD_PIN = re.compile(r"\bcreate-hayate==(?P<version>\d+(?:\.\d+)+)\b")
PUBLIC_SUFFIXES = {".md", ".txt"}


def _version(value: str) -> tuple[int, ...]:
    return tuple(int(part) for part in value.split("."))


def _is_public_source(path: PurePosixPath) -> bool:
    if path.name == "CHANGELOG.md":
        return False
    if len(path.parts) == 1:
        return path.suffix in PUBLIC_SUFFIXES or path.name == "pyproject.toml"
    return path.parts[0] in {"docs", "profile"} and path.suffix in PUBLIC_SUFFIXES


def validate_repository(
    repository: dict[str, Any],
    sources: dict[str, str],
    contract: dict[str, Any],
) -> list[str]:
    """Return actionable contract violations for one repository snapshot."""
    failures: list[str] = []
    name = str(repository["name"])
    readme = sources.get("README.md")
    project_text = sources.get("pyproject.toml")
    if readme is None:
        failures.append(f"{name}: README.md is missing from the default branch")
    else:
        for key in ("canonical_home", "canonical_compatibility"):
            expected = str(contract[key])
            if expected not in readme:
                failures.append(f"{name}: README.md omits {expected}")
    if project_text is None:
        failures.append(f"{name}: pyproject.toml is missing from the default branch")
    else:
        try:
            project = tomllib.loads(project_text)["project"]
            actual_homepage = project["urls"]["Homepage"]
        except (KeyError, tomllib.TOMLDecodeError):
            failures.append(f"{name}: pyproject.toml has no valid project.urls.Homepage")
        else:
            expected_homepage = repository["homepage"]
            if actual_homepage != expected_homepage:
                failures.append(
                    f"{name}: Homepage is {actual_homepage!r}, expected {expected_homepage!r}"
                )

    minimum_scaffold = _version(str(contract["minimum_scaffold_version"]))
    for path, text in sorted(sources.items()):
        for superseded in contract["superseded_prefixes"]:
            if superseded in text:
                failures.append(f"{name}:{path}: superseded public URL: {superseded}")
        for match in SCAFFOLD_PIN.finditer(text):
            found = match.group("version")
            if _version(found) < minimum_scaffold:
                failures.append(
                    f"{name}:{path}: create-hayate=={found} is older than "
                    f"{contract['minimum_scaffold_version']}"
                )
    return failures


def _download_archive(repository: str) -> bytes:
    url = f"https://api.github.com/repos/{OWNER}/{repository}/tarball/main"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "hayatepy-public-discovery-gate/1",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as exc:  # pragma: no cover - exercised only by network failure
            last_error = exc
            if attempt < 2:
                time.sleep(2**attempt)
    raise RuntimeError(f"could not fetch {OWNER}/{repository}@main: {last_error}")


def _public_sources(archive: bytes) -> tuple[str, dict[str, str]]:
    sources: dict[str, str] = {}
    commit = "unknown"
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as snapshot:
        for member in snapshot.getmembers():
            if not member.isfile():
                continue
            parts = PurePosixPath(member.name).parts
            if len(parts) < 2:
                continue
            root, *relative_parts = parts
            if "-" in root:
                commit = root.rsplit("-", 1)[-1]
            relative = PurePosixPath(*relative_parts)
            if not _is_public_source(relative):
                continue
            extracted = snapshot.extractfile(member)
            if extracted is None:
                continue
            try:
                sources[str(relative)] = extracted.read().decode("utf-8")
            except UnicodeDecodeError:
                continue
    return commit, sources


def main() -> int:
    with CONTRACT_PATH.open("rb") as source:
        contract = tomllib.load(source)
    if contract.get("schema_version") != 1:
        print("unsupported public-discovery contract schema", file=sys.stderr)
        return 2

    failures: list[str] = []
    checked: list[str] = []
    for repository in contract["repositories"]:
        name = str(repository["name"])
        try:
            commit, sources = _public_sources(_download_archive(name))
        except RuntimeError as exc:
            failures.append(str(exc))
            continue
        failures.extend(validate_repository(repository, sources, contract))
        checked.append(f"{name}@{commit}")

    if failures:
        print("\n".join(failures), file=sys.stderr)
        return 1
    print(f"public discovery verified across {len(checked)} repositories")
    print("\n".join(checked))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
