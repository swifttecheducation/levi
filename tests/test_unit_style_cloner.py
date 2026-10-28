#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_style_cloner.py — Kiểm thử đơn vị cho cỗ máy sao chép phong cách video (Style Cloner Engine).
"""

import os
import unittest
import tempfile
import subprocess

from core.style_cloner import StyleClonerEngine, ReferenceVideoAnalyzer


class TestStyleCloner(unittest.TestCase):
    def setUp(self):
        self.analyzer = ReferenceVideoAnalyzer()
        self.cloner = StyleClonerEngine()
        self.temp_dir = tempfile.mkdtemp()
        self.dummy_video = os.path.join(self.temp_dir, "test_ref.mp4")

        # Tạo file video MP4 1s hợp lệ để test ffprobe
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x240:d=2:r=25",
             "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", self.dummy_video,
             "-loglevel", "quiet"],
            check=False
        )

    def tearDown(self):
        if os.path.exists(self.dummy_video):
            os.remove(self.dummy_video)
        if os.path.exists(self.temp_dir):
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_editing_fingerprint(self):
        """Kiểm tra trích xuất dấu vân tay nhịp độ biên tập."""
        fp = self.analyzer.extract_editing_fingerprint(self.dummy_video)
        self.assertIn("source_video", fp)
        self.assertIn("pacing_energy", fp)
        self.assertIn("motion_dynamics", fp)
        self.assertIn("cloned_style_codes", fp)
        self.assertTrue(len(fp["cloned_style_codes"]) > 0)

    def test_generate_style_recipe_markdown(self):
        """Kiểm tra sinh bản kịch bản sao chép định dạng Markdown."""
        fp = self.analyzer.extract_editing_fingerprint(self.dummy_video)
        md = self.analyzer.generate_style_recipe_markdown(fp)
        self.assertIn("BẢN CÔNG THỨC SAO CHÉP PHONG CÁCH BIÊN TẬP", md)
        self.assertIn("MotionClone", md)
        self.assertIn("HyperFrames", md)

    def test_clone_style_from_reference(self):
        """Kiểm tra toàn bộ luồng sao chép từ video mẫu."""
        recipe_out = os.path.join(self.temp_dir, "recipe.md")
        res = self.cloner.clone_style_from_reference(self.dummy_video, output_recipe_path=recipe_out)
        self.assertIn("fingerprint", res)
        self.assertIn("suggested_mix_codes", res)
        self.assertTrue(os.path.exists(recipe_out))


if __name__ == "__main__":
    unittest.main()
