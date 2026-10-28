#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_workflows.py — Unit tests cho các workflows (Beat Sheet, Trial Reels, Carousel).
"""

import os
import sys
import unittest
from PIL import Image

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from workflows.beat_sheet import BeatSheetGenerator
from workflows.trial_reels import TrialReelsGenerator
from workflows.carousel_story.carousel import CarouselStoryGenerator


class TestWorkflowModules(unittest.TestCase):
    def test_trial_reels(self):
        gen = TrialReelsGenerator()
        variants = gen.generate_three_variants("Học AI Làm Phim", [])
        self.assertEqual(len(variants), 3)
        self.assertEqual(variants[0]["variant_id"], "A")
        self.assertEqual(variants[1]["variant_id"], "B")
        self.assertEqual(variants[2]["variant_id"], "C")

    def test_beat_sheet_image_generation(self):
        gen = BeatSheetGenerator(output_width=600)
        out_jpg = os.path.join(REPO_ROOT, "outbox", "test_beats.jpg")
        mock_frames = [
            Image.new("RGB", (180, 320), color="#111111"),
            Image.new("RGB", (180, 320), color="#222222")
        ]
        labels = ["0.0s", "2.5s"]
        gen.generate_contact_sheet(mock_frames, labels, out_jpg)
        self.assertTrue(os.path.exists(out_jpg))

        if os.path.exists(out_jpg):
            os.remove(out_jpg)

    def test_carousel_generation(self):
        gen = CarouselStoryGenerator()
        out_dir = os.path.join(REPO_ROOT, "outbox", "test_carousel")
        slides_data = [
            {"title": "Slide 1", "body": "Nội dung slide 1"},
            {"title": "Slide 2", "body": "Nội dung slide 2"}
        ]
        paths = gen.generate_carousel_slides(slides_data, output_dir=out_dir)
        self.assertEqual(len(paths), 2)
        for p in paths:
            self.assertTrue(os.path.exists(p))
            os.remove(p)
        if os.path.exists(out_dir):
            os.rmdir(out_dir)


if __name__ == "__main__":
    unittest.main()
