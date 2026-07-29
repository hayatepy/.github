from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import export_profile


def benchmark() -> dict[str, object]:
    frameworks: dict[str, object] = {}
    values = {
        "hayate": ("0.15.1", 149.0, 5, 305273, 14906.4, 14),
        "fastapi": ("0.140.0", 471.4, 13, 2869443, 10086.4, 12),
        "django": ("6.0.7", 392.6, 6, 5270712, 2557.4, 12),
        "hono": ("4.12.32", 61.3, 2, 288207, 59187.4, 12),
    }
    for name, (
        version,
        cold_start,
        packages,
        gzip_bytes,
        throughput,
        passed,
    ) in values.items():
        frameworks[name] = {
            "payload": {
                "framework_version": version,
                "production_packages": packages,
                "production_payload_gzip_bytes": gzip_bytes,
            },
            "startup": {"cold_start_ms": cold_start},
            "throughput": {"geometric_mean_requests_per_second": throughput},
            "http_contract": {"passed": passed, "total": 14},
        }
    return {
        "schema_version": 2,
        "git_commit": "result",
        "frameworks": frameworks,
    }


def capabilities() -> dict[str, object]:
    positions = {
        "portable_agent_api": "advantaged",
        "typed_python_api": "competitive",
        "traditional_full_stack": "competitor_advantaged",
        "javascript_edge": "competitor_advantaged",
    }
    return {
        "schema_version": 1,
        "as_of": "2026-07-30",
        "universal_winner": None,
        "profiles": [
            {
                "id": profile_id,
                "title": profile_id.replace("_", " ").title(),
                "position": position,
                "summary": f"{profile_id} evidence.",
            }
            for profile_id, position in positions.items()
        ],
    }


def source() -> dict[str, str]:
    return {
        "benchmark_as_of": "2026-07-28",
        "capabilities_as_of": "2026-07-30",
        "benchmark_result_commit": "result",
    }


class ExportProfileTests(unittest.TestCase):
    def test_renders_current_values_and_computed_ratios(self) -> None:
        table = export_profile._benchmark_table(benchmark())
        summary = export_profile._benchmark_summary(benchmark())

        self.assertIn("Hayate 0.15.1", table)
        self.assertIn("**14/14**", table)
        self.assertIn("**59,187 req/s**", table)
        self.assertIn("1.48x FastAPI", summary)
        self.assertIn("5.83x Django", summary)
        self.assertIn("3.97x Hayate", summary)

    def test_uses_source_backed_profile_summaries(self) -> None:
        rendered = export_profile._profile_verdicts(capabilities())

        self.assertIn("Hayate advantaged", rendered)
        self.assertIn("competitor advantaged", rendered)
        self.assertIn("javascript_edge evidence.", rendered)

    def test_rejects_a_missing_framework(self) -> None:
        value = benchmark()
        del value["frameworks"]["hono"]  # type: ignore[index]

        with self.assertRaisesRegex(ValueError, "exactly four frameworks"):
            export_profile._validate(value, capabilities(), source())

    def test_rejects_a_universal_winner(self) -> None:
        value = capabilities()
        value["universal_winner"] = "hayate"

        with self.assertRaisesRegex(ValueError, "universal winner"):
            export_profile._validate(benchmark(), value, source())

    def test_rejects_profile_position_drift(self) -> None:
        value = capabilities()
        profiles = value["profiles"]
        assert isinstance(profiles, list)
        changed = copy.deepcopy(profiles[0])
        changed["position"] = "competitive"
        profiles[0] = changed

        with self.assertRaisesRegex(ValueError, "unexpected position"):
            export_profile._validate(benchmark(), value, source())


if __name__ == "__main__":
    unittest.main()
