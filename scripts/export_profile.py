"""Generate the organization profile from immutable competitive evidence."""

from __future__ import annotations

import argparse
import json
import textwrap
from pathlib import Path
from string import Template
from typing import Any
from urllib.request import urlopen

import tomllib

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data" / "ecosystem.toml"
TEMPLATE = ROOT / "profile" / "README.md.in"
OUTPUT = ROOT / "profile" / "README.md"

FRAMEWORK_ORDER = ("hayate", "fastapi", "django", "hono")
FRAMEWORK_NAMES = {
    "hayate": "Hayate",
    "fastapi": "FastAPI",
    "django": "Django",
    "hono": "Hono",
}
PROFILE_ORDER = (
    "portable_agent_api",
    "typed_python_api",
    "traditional_full_stack",
    "javascript_edge",
)
PROFILE_POSITIONS = {
    "portable_agent_api": "advantaged",
    "typed_python_api": "competitive",
    "traditional_full_stack": "competitor_advantaged",
    "javascript_edge": "competitor_advantaged",
}
POSITION_LABELS = {
    "advantaged": "Hayate advantaged",
    "competitive": "competitive",
    "competitor_advantaged": "competitor advantaged",
}


def _fetch_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=30) as response:
        value = json.load(response)
    if not isinstance(value, dict):
        raise ValueError(f"expected a JSON object from {url}")
    return value


def _source_url(commit: str, path: str, *, raw: bool) -> str:
    host = "raw.githubusercontent.com" if raw else "github.com"
    middle = "" if raw else "blob/"
    return f"https://{host}/hayatepy/hayate/{middle}{commit}/{path}"


def _load() -> tuple[dict[str, Any], dict[str, Any], dict[str, str]]:
    manifest = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
    source = manifest["profile_evidence"]
    commit = source["commit"]
    benchmark_path = source["benchmark_path"]
    capabilities_path = source["capabilities_path"]
    benchmark = _fetch_json(_source_url(commit, benchmark_path, raw=True))
    capabilities = _fetch_json(_source_url(commit, capabilities_path, raw=True))
    _validate(benchmark, capabilities, source)
    links = {
        "benchmark_url": _source_url(
            commit,
            str(Path(benchmark_path).with_suffix(".md")),
            raw=False,
        ),
        "capabilities_url": _source_url(
            commit,
            "docs/capabilities.md",
            raw=False,
        ),
    }
    return benchmark, capabilities, links


def _validate(
    benchmark: dict[str, Any],
    capabilities: dict[str, Any],
    source: dict[str, Any],
) -> None:
    if benchmark.get("schema_version") != 2:
        raise ValueError("unsupported competitive benchmark schema")
    if benchmark.get("git_commit") != source["benchmark_result_commit"]:
        raise ValueError("competitive benchmark result commit does not match manifest")
    frameworks = benchmark.get("frameworks")
    if not isinstance(frameworks, dict) or set(frameworks) != set(FRAMEWORK_ORDER):
        raise ValueError("competitive benchmark must contain exactly four frameworks")

    for framework_id in FRAMEWORK_ORDER:
        row = frameworks[framework_id]
        required = (
            row.get("payload", {}).get("framework_version"),
            row.get("payload", {}).get("production_packages"),
            row.get("payload", {}).get("production_payload_gzip_bytes"),
            row.get("startup", {}).get("cold_start_ms"),
            row.get("throughput", {}).get("geometric_mean_requests_per_second"),
            row.get("http_contract", {}).get("passed"),
            row.get("http_contract", {}).get("total"),
        )
        if any(value is None for value in required):
            raise ValueError(f"incomplete benchmark row for {framework_id}")

    if capabilities.get("schema_version") != 1:
        raise ValueError("unsupported capability schema")
    if capabilities.get("as_of") != source["as_of"]:
        raise ValueError("capability evidence date does not match manifest")
    if capabilities.get("universal_winner") is not None:
        raise ValueError("organization profile must not publish a universal winner")
    profiles = {
        profile["id"]: profile
        for profile in capabilities.get("profiles", [])
        if isinstance(profile, dict) and "id" in profile
    }
    if set(profiles) != set(PROFILE_ORDER):
        raise ValueError("capability evidence must contain exactly four profiles")
    for profile_id, expected_position in PROFILE_POSITIONS.items():
        profile = profiles[profile_id]
        if profile.get("position") != expected_position:
            raise ValueError(f"unexpected position for profile {profile_id}")
        if not profile.get("title") or not profile.get("summary"):
            raise ValueError(f"incomplete capability profile {profile_id}")


def _best(values: dict[str, float], *, higher: bool) -> set[str]:
    target = (max if higher else min)(values.values())
    return {key for key, value in values.items() if value == target}


def _emphasize(value: str, framework_id: str, best: set[str]) -> str:
    return f"**{value}**" if framework_id in best else value


def _benchmark_table(benchmark: dict[str, Any]) -> str:
    frameworks = benchmark["frameworks"]
    cold = {
        key: float(frameworks[key]["startup"]["cold_start_ms"])
        for key in FRAMEWORK_ORDER
    }
    packages = {
        key: float(frameworks[key]["payload"]["production_packages"])
        for key in FRAMEWORK_ORDER
    }
    gzip = {
        key: float(frameworks[key]["payload"]["production_payload_gzip_bytes"])
        for key in FRAMEWORK_ORDER
    }
    throughput = {
        key: float(frameworks[key]["throughput"]["geometric_mean_requests_per_second"])
        for key in FRAMEWORK_ORDER
    }
    contract = {
        key: (
            float(frameworks[key]["http_contract"]["passed"])
            / float(frameworks[key]["http_contract"]["total"])
        )
        for key in FRAMEWORK_ORDER
    }
    best = {
        "cold": _best(cold, higher=False),
        "packages": _best(packages, higher=False),
        "gzip": _best(gzip, higher=False),
        "throughput": _best(throughput, higher=True),
        "contract": _best(contract, higher=True),
    }
    headers = " | ".join(
        f"{FRAMEWORK_NAMES[key]} {frameworks[key]['payload']['framework_version']}"
        for key in FRAMEWORK_ORDER
    )

    def cells(metric: str, render: Any) -> str:
        values = {
            "cold": cold,
            "packages": packages,
            "gzip": gzip,
            "throughput": throughput,
        }[metric]
        return " | ".join(
            _emphasize(render(values[key]), key, best[metric])
            for key in FRAMEWORK_ORDER
        )

    contract_cells = " | ".join(
        _emphasize(
            f"{frameworks[key]['http_contract']['passed']}/"
            f"{frameworks[key]['http_contract']['total']}",
            key,
            best["contract"],
        )
        for key in FRAMEWORK_ORDER
    )
    return "\n".join(
        [
            f"| Boundary | {headers} |",
            "|---|---:|---:|---:|---:|",
            f"| Cold start | {cells('cold', lambda value: f'{value:.1f} ms')} |",
            f"| Production packages | {cells('packages', lambda value: f'{value:.0f}')} |",
            f"| gzip payload | {cells('gzip', lambda value: f'{value / 1024:,.1f} KiB')} |",
            f"| Throughput | {cells('throughput', lambda value: f'{value:,.0f} req/s')} |",
            f"| Common HTTP contract | {contract_cells} |",
        ]
    )


def _benchmark_summary(benchmark: dict[str, Any]) -> str:
    frameworks = benchmark["frameworks"]

    def throughput(framework_id: str) -> float:
        return float(
            frameworks[framework_id]["throughput"]["geometric_mean_requests_per_second"]
        )

    hayate = throughput("hayate")
    fastapi = throughput("fastapi")
    django = throughput("django")
    hono = throughput("hono")
    return textwrap.fill(
        f"On this workload Hayate delivered {hayate / fastapi:.2f}x FastAPI's "
        f"and {hayate / django:.2f}x Django's throughput. Hono delivered "
        f"{hono / hayate:.2f}x Hayate's throughput and retained the best "
        "startup, dependency-count, and deployment-payload results.",
        width=88,
        break_long_words=False,
        break_on_hyphens=False,
    )


def _profile_verdicts(capabilities: dict[str, Any]) -> str:
    profiles = {profile["id"]: profile for profile in capabilities["profiles"]}
    return "\n".join(
        textwrap.fill(
            f"**{profiles[profile_id]['title']} — "
            f"{POSITION_LABELS[profiles[profile_id]['position']]}.** "
            f"{profiles[profile_id]['summary']}",
            width=88,
            initial_indent="- ",
            subsequent_indent="  ",
            break_long_words=False,
            break_on_hyphens=False,
        )
        for profile_id in PROFILE_ORDER
    )


def _render(
    benchmark: dict[str, Any],
    capabilities: dict[str, Any],
    links: dict[str, str],
    *,
    benchmark_date: str,
) -> str:
    template = Template(TEMPLATE.read_text(encoding="utf-8"))
    body = template.substitute(
        benchmark_date=benchmark_date,
        benchmark_table=_benchmark_table(benchmark),
        benchmark_summary=_benchmark_summary(benchmark),
        profile_verdicts=_profile_verdicts(capabilities),
        **links,
    )
    return (
        "<!-- Generated by scripts/export_profile.py; edit README.md.in. -->\n\n"
        f"{body.rstrip()}\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    manifest = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))
    benchmark, capabilities, links = _load()
    expected = _render(
        benchmark,
        capabilities,
        links,
        benchmark_date=manifest["profile_evidence"]["as_of"],
    )
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != expected:
            parser.error(
                "profile/README.md is stale; run python3 scripts/export_profile.py"
            )
        return 0
    OUTPUT.write_text(expected, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
