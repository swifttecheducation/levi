#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_styles_library.py — Kiểm thử đơn vị cho Thư viện 105 Phong cách Dựng Video (Styles Library).
"""

import unittest
from core.styles_library import StylesLibrary, CURATED_PRESETS
from core.brand_engine import BrandEngine


class TestStylesLibrary(unittest.TestCase):
    def setUp(self):
        self.lib = StylesLibrary()

    def test_total_count_and_categories(self):
        """Kiểm tra tổng số lượng phong cách và danh mục."""
        self.assertEqual(self.lib.total_count, 105)
        cats = self.lib.list_categories()
        self.assertEqual(len(cats), 10)
        cat_ids = [c["id"] for c in cats]
        for expected in ["H", "C", "L", "P", "V", "B", "X", "M", "S", "G"]:
            self.assertIn(expected, cat_ids)

    def test_get_style_by_code(self):
        """Kiểm tra tra cứu từng phong cách cụ thể."""
        h1 = self.lib.get_style("H1")
        self.assertIsNotNone(h1)
        self.assertEqual(h1["code"], "H1")
        self.assertIn("Tiêu đề lớn sau nhân vật", h1["name"])

        g1 = self.lib.get_style("g1")  # test case insensitivity
        self.assertIsNotNone(g1)
        self.assertEqual(g1["code"], "G1")

    def test_search_styles(self):
        """Kiểm tra tìm kiếm phong cách theo từ khóa."""
        results = self.lib.search_styles("Apple")
        self.assertTrue(len(results) > 0)
        codes = [r["code"] for r in results]
        self.assertIn("G4", codes)

        mag_results = self.lib.search_styles("tạp chí")
        self.assertTrue(len(mag_results) > 0)

    def test_compose_mix_prompt(self):
        """Kiểm tra tạo bản tóm tắt yêu cầu dựng (Mix Prompt)."""
        prompt = self.lib.compose_mix_prompt(["H1", "C1", "L1", "X5", "M1", "G1"])
        self.assertIn("Dựng video của tôi theo các phong cách sau:", prompt)
        self.assertIn("- H1 Tiêu đề lớn sau nhân vật", prompt)
        self.assertIn("- C1 Cụm chữ và từ khóa vàng", prompt)
        self.assertIn("vùng an toàn TikTok và Reels", prompt)

    def test_curated_presets(self):
        """Kiểm tra các bộ phối mẫu gợi ý."""
        presets = self.lib.list_presets()
        self.assertIn("editorial_luxe", presets)
        self.assertIn("apple_minimal", presets)
        self.assertIn("hands_off_reels", presets)
        self.assertIn("viral_storyteller", presets)
        self.assertIn("gen_z_pop", presets)

        hands_off = self.lib.get_preset("hands_off_reels")
        self.assertIn("H1", hands_off["codes"])

    def test_brand_engine_integration(self):
        """Kiểm tra tích hợp style_codes với BrandEngine."""
        engine = BrandEngine()
        codes = engine.get_style_codes()
        self.assertTrue(len(codes) > 0)
        self.assertIn("H1", codes)


if __name__ == "__main__":
    unittest.main()
