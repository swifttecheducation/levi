#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_brand_wizard.py — Kiểm thử đơn vị cho Brand Wizard & 7 Trụ Cột Nhận Diện Thương Hiệu.
"""

import os
import unittest
import tempfile
from unittest.mock import patch

from core.brand_engine import BrandEngine
from workflows.brand_wizard import BrandWizard


class TestBrandWizard(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.brand_file = os.path.join(self.temp_dir, "test_brand_kit.md")

    def tearDown(self):
        if os.path.exists(self.brand_file):
            os.remove(self.brand_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_brand_wizard_deep_interview(self):
        """Kiểm thử mô phỏng toàn bộ luồng phỏng vấn 7 trụ cột."""
        mock_inputs = [
            "Tech Master Pro",                   # 1. Tên thương hiệu
            "Các lập trình viên muốn làm video", # 1. Giúp ai
            "@techmaster",                       # 1. Instagram
            "@techmaster_ai",                    # 1. TikTok
            "Điềm tĩnh, khoa học, thực chiến",   # 2. Giọng điệu
            "Người xem thấy tin cậy và hiểu ngay",# 2. Gut check
            "Không clickbait, Không hứa hẹn 100%", # 3. Hard rules
            "Bạn có biết rằng...",               # 4. Intro hook
            "Hẹn gặp lại ở video tiếp theo!",    # 4. Outro CTA
            "2",                                 # 5. Modern Minimal (style choice)
            "Khóa Học Python Video Master",      # 6. Sản phẩm chính
            "Ebook 50 Prompt Video",             # 6. Quà tặng
            "PYTHON, AI, VIDEO",                 # 6. Từ khóa ManyChat
            "pai thon -> Python, quy p -> Quick" # 7. Sửa lỗi phiên âm
        ]

        wizard = BrandWizard(brand_kit_path=self.brand_file)
        with patch("builtins.input", side_effect=mock_inputs):
            wizard.run_deep_interview()

        self.assertTrue(os.path.exists(self.brand_file))

        # Đọc lại bằng BrandEngine để kiểm tra tính toàn vẹn của 7 trụ cột
        engine = BrandEngine(self.brand_file)
        self.assertEqual(engine.brand["name"], "Tech Master Pro")
        self.assertEqual(engine.brand["target_audience"], "Các lập trình viên muốn làm video")
        self.assertIn("Không clickbait", engine.get_hard_rules())
        self.assertEqual(engine.get_voice_dna()["intro_hook"], "Bạn có biết rằng...")
        self.assertEqual(engine.get_fonts()["headline"], "Inter")
        self.assertEqual(engine.get_offers()["main_product"], "Khóa Học Python Video Master")
        self.assertIn("PYTHON", engine.get_manychat_keywords())

        # Kiểm tra sửa lỗi phiên âm tự động
        raw_text = "học pai thon cực nhanh với quy p guide"
        corrected = engine.apply_phonetic_corrections(raw_text)
        self.assertIn("Python", corrected)
        self.assertIn("Quick", corrected)


if __name__ == "__main__":
    unittest.main()
