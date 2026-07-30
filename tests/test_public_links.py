from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_HOME = "https://hayatepy.dev/"
CANONICAL_FIRST_APP = "https://hayatepy.dev/get-started/first-app/"
CANONICAL_COMPATIBILITY = "https://hayatepy.dev/evidence/compatibility/"
CANONICAL_DESIGN_PARTNERS = "https://hayatepy.dev/contribute/#design-partners"
SUPERSEDED_DOCS_PREFIX = "https://hayatepy.github.io/"


class PublicLinksTest(unittest.TestCase):
    def test_profile_routes_public_discovery_through_hayatepy_dev(self) -> None:
        for relative_path in ("profile/README.md.in", "profile/README.md"):
            text = (ROOT / relative_path).read_text(encoding="utf-8")

            self.assertIn(CANONICAL_HOME, text)
            self.assertIn(CANONICAL_FIRST_APP, text)
            self.assertIn(CANONICAL_COMPATIBILITY, text)
            self.assertIn(CANONICAL_DESIGN_PARTNERS, text)
            self.assertNotIn(SUPERSEDED_DOCS_PREFIX, text)

    def test_llms_routes_human_documentation_through_hayatepy_dev(self) -> None:
        text = (ROOT / "llms.txt").read_text(encoding="utf-8")

        self.assertIn(CANONICAL_HOME, text)
        self.assertIn(CANONICAL_FIRST_APP, text)
        self.assertIn(CANONICAL_COMPATIBILITY, text)
        self.assertNotIn(SUPERSEDED_DOCS_PREFIX, text)

    def test_start_uses_the_current_scaffold_release(self) -> None:
        text = (ROOT / "docs" / "START.md").read_text(encoding="utf-8")

        self.assertIn("create-hayate==0.14.0", text)
        self.assertNotIn("create-hayate==0.13.2", text)

    def test_design_partner_form_uses_the_public_program_page(self) -> None:
        text = (
            ROOT / ".github" / "ISSUE_TEMPLATE" / "design_partner.yml"
        ).read_text(encoding="utf-8")

        self.assertIn(CANONICAL_DESIGN_PARTNERS, text)
