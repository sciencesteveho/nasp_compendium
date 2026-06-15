"""Tests for display-name helpers."""

from __future__ import annotations

import unittest

from nasp_compendium.display import humanize_module_name


class HumanizeModuleNameTest(unittest.TestCase):
    def test_module_specific_display_names(self) -> None:
        expected_labels = {
            "CGAMP_TRANSPORT": "cGAMP transport",
            "ISR": "Integrated stress response",
            "NASP_DNA_SENSING": "DNA sensing",
            "NASP_RNA_SENSING": "RNA sensing",
            "SIGNALING_CONTEXT_IFN_JAK_STAT": (
                "Signaling context IFN JAK/STAT"
            ),
            "SIGNALING_CONTEXT_TBK1_IRF": "Signaling context TBK1-IRF",
            "SIGNALING_CONTEXT_TLR": "Signaling context TLR",
        }

        for module_id, expected_label in expected_labels.items():
            with self.subTest(module_id=module_id):
                self.assertEqual(
                    humanize_module_name(module_id),
                    expected_label,
                )

    def test_generic_module_name_fallback(self) -> None:
        self.assertEqual(
            humanize_module_name("SIGNALING_CONTEXT_NFKB"),
            "Signaling context NF-\u03baB",
        )


if __name__ == "__main__":
    unittest.main()
