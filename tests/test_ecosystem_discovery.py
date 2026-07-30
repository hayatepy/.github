from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import check_ecosystem_discovery

CONTRACT = {
    "canonical_home": "https://hayatepy.dev/",
    "canonical_compatibility": "https://hayatepy.dev/evidence/compatibility/",
    "minimum_scaffold_version": "0.13.2",
    "superseded_prefixes": [
        "https://hayatepy.github.io/",
        "https://github.com/hayatepy/.github/blob/main/docs/START.md",
    ],
}
REPOSITORY = {
    "name": "hayate-example",
    "homepage": "https://hayatepy.dev/ecosystem/#hayate-example",
}


def sources() -> dict[str, str]:
    return {
        "README.md": (
            "[Start](https://hayatepy.dev/)\n"
            "[Compatibility](https://hayatepy.dev/evidence/compatibility/)\n"
            "`create-hayate==0.13.2`\n"
        ),
        "pyproject.toml": """
[project]
name = "hayate-example"
[project.urls]
Homepage = "https://hayatepy.dev/ecosystem/#hayate-example"
""",
    }


class EcosystemDiscoveryTests(unittest.TestCase):
    def test_accepts_the_canonical_contract(self) -> None:
        self.assertEqual(
            check_ecosystem_discovery.validate_repository(
                REPOSITORY,
                sources(),
                CONTRACT,
            ),
            [],
        )

    def test_rejects_superseded_links_and_scaffold_pins(self) -> None:
        changed = sources()
        changed["docs/START.md"] = (
            "https://github.com/hayatepy/.github/blob/main/docs/START.md\n"
            "create-hayate==0.13.1\n"
        )

        failures = check_ecosystem_discovery.validate_repository(
            REPOSITORY,
            changed,
            CONTRACT,
        )

        self.assertTrue(any("superseded public URL" in failure for failure in failures))
        self.assertTrue(any("older than 0.13.2" in failure for failure in failures))

    def test_rejects_homepage_drift(self) -> None:
        changed = sources()
        changed["pyproject.toml"] = changed["pyproject.toml"].replace(
            "https://hayatepy.dev/ecosystem/#hayate-example",
            "https://github.com/hayatepy/hayate-example",
        )

        failures = check_ecosystem_discovery.validate_repository(
            REPOSITORY,
            changed,
            CONTRACT,
        )

        self.assertTrue(any("Homepage is" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
