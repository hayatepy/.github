from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import export_compatibility


class ExportCompatibilityTests(unittest.TestCase):
    def test_private_evidence_is_plain_text_with_a_commit(self) -> None:
        sources = {
            "private": {
                "label": "Private production gate",
                "commit": "0123456789abcdef",
                "visibility": "private",
            }
        }

        rendered = export_compatibility._evidence_links(["private"], sources)

        self.assertEqual(rendered, "Private production gate at `0123456789ab`")
        self.assertNotIn("](", rendered)


if __name__ == "__main__":
    unittest.main()
