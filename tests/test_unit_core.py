#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_core.py — Unit tests cho các module cốt lõi (Brand, Audio, Transcriber, ChinLock, RoughCutter).
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.brand_engine import BrandEngine
from core.audio_master import AudioMaster
from core.whisper_transcriber import WhisperTranscriber
from core.chin_lock import ChinLock
from core.rough_cutter import RoughCutter


class TestCoreModules(unittest.TestCase):
    def test_brand_engine(self):
        engine = BrandEngine()
        fonts = engine.get_fonts()
        colors = engine.get_colors()
        audio = engine.get_audio_standards()
        self.assertIn("headline", fonts)
        self.assertIn("caption", fonts)
        self.assertIn("primary", colors)
        self.assertEqual(audio["target_lufs"], -14.0)

    def test_audio_master_filter_generation(self):
        master = AudioMaster(target_i=-14.0, target_tp=-1.5)
        f_str = master.get_loudnorm_filter_string()
        self.assertIn("I=-14.0", f_str)
        self.assertIn("TP=-1.5", f_str)

        cmd = master.build_ffmpeg_audio_master_command("input.wav", "output.aac", "bgm.mp3")
        self.assertIn("-filter_complex", cmd)
        self.assertIn("loudnorm", "".join(cmd))

    def test_whisper_transcriber_mock(self):
        trans = WhisperTranscriber()
        text = "Một hai ba bốn năm sáu bảy tám"
        chunks = trans.create_mock_transcript_from_text(text, total_duration=8.0)
        self.assertTrue(len(chunks) >= 2)
        self.assertEqual(chunks[0]["start"], 0.0)
        self.assertTrue(chunks[-1]["end"] <= 8.0)

    def test_chin_lock_anchor(self):
        lock = ChinLock()
        default_y = lock.calculate_default_anchor_y()
        self.assertGreater(default_y, 1000.0)  # Nằm ở nửa dưới màn hình 1920px

    def test_rough_cutter(self):
        cutter = RoughCutter(punch_in_scale=1.1)
        mock_segs = [
            {"start": 0.5, "end": 2.0, "text": "Đoạn một"},
            {"start": 3.0, "end": 5.0, "text": "Đoạn hai"}
        ]
        cuts = cutter.compute_cuts_from_speech_segments(mock_segs)
        self.assertEqual(len(cuts), 2)
        self.assertEqual(cuts[0]["scale"], 1.0)
        self.assertEqual(cuts[1]["scale"], 1.1)  # Micro-zoom xen kẽ
        total_dur = cutter.get_timeline_duration(cuts)
        self.assertGreater(total_dur, 0.0)


if __name__ == "__main__":
    unittest.main()
