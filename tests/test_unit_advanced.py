#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_advanced.py — Unit tests cho các module nâng cấp điện ảnh:
  - ColorGradeEngine (Log transform, Cinematic looks)
  - PacingEngine (J-Cut / L-Cut, Dramatic Pause)
  - MotionReframer (Cubic-Bezier zoom, Motion blur)
  - SemanticSoundVisual (Keyword to SFX matching)
  - InteractiveStudio (5-step scientific pipeline)
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.color_grade import ColorGradeEngine
from core.pacing_engine import PacingEngine
from core.motion_reframer import MotionReframer
from core.semantic_sound_visual import SemanticSoundVisual
from workflows.interactive_studio import InteractiveStudio


class TestAdvancedCinemaModules(unittest.TestCase):
    def test_color_grade_engine(self):
        engine = ColorGradeEngine()
        space = engine.detect_color_space("my_apple_log_video.mp4")
        self.assertEqual(space, "apple_log")

        flt = engine.get_color_transform_filter("apple_log", "teal_orange")
        self.assertIn("contrast=", flt)
        self.assertIn("colorbalance=", flt)

        looks = engine.get_available_looks()
        self.assertIn("teal_orange", looks)
        self.assertIn("kodak_film", looks)
        self.assertIn("clean_corporate", looks)

    def test_pacing_engine(self):
        pacing = PacingEngine(j_cut_offset_sec=0.12)
        # Kiểm tra dramatic pause
        is_pause = pacing.is_dramatic_pause("Tại sao bạn chưa giàu?", gap_duration=0.6)
        self.assertTrue(is_pause)

        is_not_pause = pacing.is_dramatic_pause("và tôi đi ăn cơm", gap_duration=0.2)
        self.assertFalse(is_not_pause)

        # Kiểm tra J-Cut
        segs = [
            {"start": 0.0, "end": 2.0, "text": "Câu một"},
            {"start": 2.5, "end": 5.0, "text": "Tại sao lại thế?"}
        ]
        optimized = pacing.optimize_timeline_pacing(segs, enable_j_cuts=True)
        self.assertEqual(len(optimized), 2)
        self.assertTrue(optimized[1]["has_j_cut"])
        self.assertGreater(optimized[1]["video_in"], optimized[1]["audio_in"])

    def test_motion_reframer(self):
        reframer = MotionReframer()
        val_0 = reframer.cubic_bezier_ease_out(0.0)
        val_1 = reframer.cubic_bezier_ease_out(1.0)
        val_half = reframer.cubic_bezier_ease_out(0.5)
        self.assertEqual(val_0, 0.0)
        self.assertEqual(val_1, 1.0)
        self.assertGreater(val_half, 0.5)  # Ease-out nhanh hơn ở đầu

        kfs = reframer.compute_zoom_keyframes(clip_start=1.0, target_scale=1.08)
        self.assertTrue(len(kfs) > 1)
        self.assertEqual(kfs[-1]["scale"], 1.08)

    def test_semantic_sound_visual(self):
        semantic = SemanticSoundVisual()
        subs = [
            {"start": 1.0, "text": "Kiếm được một triệu view và nhiều tiền"},
            {"start": 20.0, "text": "Bí mật đằng sau ý tưởng này là gì"}
        ]
        cues = semantic.analyze_transcript_cues(subs)
        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0]["category"], "finance")
        self.assertEqual(cues[1]["category"], "insight")

    def test_interactive_studio_auto(self):
        # Chạy pipeline ở chế độ auto_mode
        studio = InteractiveStudio(auto_mode=True)
        # Tạo file video giả lập để test
        dummy_video = os.path.join(REPO_ROOT, "outbox", "dummy_test_video.mp4")
        with open(dummy_video, "w") as f:
            f.write("dummy")

        res = studio.run_scientific_pipeline(
            video_path=dummy_video,
            project_name="Test_Interactive",
            output_dir=os.path.join(REPO_ROOT, "outbox", "test_interactive_out")
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("pacing", res["choices"])
        self.assertIn("color", res["choices"])

        # Dọn dẹp
        if os.path.exists(dummy_video):
            os.remove(dummy_video)
        out_test_dir = os.path.join(REPO_ROOT, "outbox", "test_interactive_out")
        if os.path.exists(out_test_dir):
            import shutil
            shutil.rmtree(out_test_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
