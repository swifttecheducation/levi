#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_font_manager.py — Kiểm thử đơn vị cho Font Manager Engine & Kho 32 Font Việt Hóa.
"""

import unittest
from core.font_manager import FontManager, FONT_FAMILIES, CURATED_FONT_PACKS


class TestFontManager(unittest.TestCase):
    def setUp(self):
        self.fm = FontManager()

    def test_total_families(self):
        """Kiểm tra tổng số họ font được hỗ trợ."""
        self.assertEqual(self.fm.total_families, 14)
        families = [f["name"] for f in self.fm.list_families()]
        self.assertIn("Instrument Serif", families)
        self.assertIn("Be Vietnam Pro", families)
        self.assertIn("Inter", families)
        self.assertIn("Playfair Display", families)
        self.assertIn("Poppins", families)
        self.assertIn("Coolvetica", families)
        self.assertIn("Caveat", families)
        self.assertIn("SVN-Chicken Noodle Soup", families)

    def test_resolve_font_file(self):
        """Kiểm tra tìm file tệp font thực tế trong thư mục assets/fonts."""
        file_instrument = self.fm.resolve_font_file("Instrument Serif", "regular")
        self.assertIsNotNone(file_instrument)
        self.assertTrue(file_instrument.endswith("InstrumentSerif-Regular.ttf"))

        file_instrument_italic = self.fm.resolve_font_file("Instrument Serif", italic=True)
        self.assertIsNotNone(file_instrument_italic)
        self.assertTrue(file_instrument_italic.endswith("InstrumentSerif-Italic.ttf"))

        file_bevietnam = self.fm.resolve_font_file("Be Vietnam Pro", "bold")
        self.assertIsNotNone(file_bevietnam)
        self.assertTrue(file_bevietnam.endswith("BeVietnamPro-Bold.ttf"))

    def test_curated_font_packs(self):
        """Kiểm tra 6 bộ phối font chữ chuẩn thương hiệu."""
        packs = self.fm.list_packs()
        self.assertEqual(len(packs), 6)
        self.assertIn("1", packs)
        self.assertEqual(packs["1"]["headline"], "Instrument Serif")
        self.assertEqual(packs["1"]["caption"], "Be Vietnam Pro")

        self.assertIn("2", packs)
        self.assertEqual(packs["2"]["headline"], "Inter")


if __name__ == "__main__":
    unittest.main()
