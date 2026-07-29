from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORM = ROOT / ".github" / "ISSUE_TEMPLATE" / "design_partner.yml"
PACKAGE_LABEL = re.compile(r"^        - label: (?P<package>[a-z0-9-]+)$", re.MULTILINE)

EXPECTED_PACKAGES = {
    "create-hayate",
    "hayate",
    "hayate-admin",
    "hayate-auth",
    "hayate-fetch",
    "hayate-htmx",
    "hayate-mcp",
    "hayate-openapi",
    "hayate-sql",
}


class DesignPartnerFormTest(unittest.TestCase):
    def test_exposes_every_public_ecosystem_package(self) -> None:
        packages = PACKAGE_LABEL.findall(FORM.read_text(encoding="utf-8"))

        self.assertEqual(len(packages), len(set(packages)))
        self.assertEqual(set(packages), EXPECTED_PACKAGES)

    def test_preserves_owner_external_and_privacy_confirmations(self) -> None:
        form = FORM.read_text(encoding="utf-8")

        self.assertIn(
            "This application is not owned by the Hayate maintainer.",
            form,
        )
        self.assertIn(
            "I have not included secrets, customer data, proprietary code, "
            "or vulnerability details.",
            form,
        )
        self.assertIn(
            "I can share the measured onboarding outcome, privately if necessary.",
            form,
        )


if __name__ == "__main__":
    unittest.main()
