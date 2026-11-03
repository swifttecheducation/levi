#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_pipeline_fixes.py — Kiểm thử cho các lỗi pipeline đã sửa:
  - Gộp cut chồng lấn, kẹp cut vào độ dài video, đổi phụ đề sang mốc timeline đã cắt
  - Vị trí phụ đề né cằm (px -> transform_y của CapCut)
  - BrandEngine không còn dùng chung state giữa các instance
  - Premiere XML: file URL được mã hóa, chỉ định nghĩa file đầy đủ một lần
  - find_inbox_video ổn định & không phân biệt hoa/thường
  - Transcript: JSON, lỗi rõ ràng, và transcript giả chỉ khi bật allow_mock
Các test ở đây không cần ffmpeg.
"""

import os
import sys
import json
import tempfile
import shutil
import unittest
import xml.etree.ElementTree as ET
from unittest import mock

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from core.rough_cutter import RoughCutter
from core.brand_engine import BrandEngine, DEFAULT_BRAND_KIT
from core.chin_lock import ChinLock
from core.whisper_transcriber import WhisperTranscriber, TranscriberUnavailable
from engines.adobe.pr_xml_builder import PremiereXMLBuilder, _path_to_file_url
from studio import find_inbox_video


class TestRoughCutterFixes(unittest.TestCase):
    def setUp(self):
        self.cutter = RoughCutter()

    def test_overlapping_segments_are_merged(self):
        segs = [
            {"start": 0.0, "end": 1.0, "text": "a"},
            {"start": 1.05, "end": 2.0, "text": "b"},   # lead-in/out làm hai đoạn chồng nhau
        ]
        cuts = self.cutter.compute_cuts_from_speech_segments(segs)
        self.assertEqual(len(cuts), 1)
        self.assertEqual(cuts[0]["text"], "a b")
        self.assertAlmostEqual(cuts[0]["source_in"], 0.0, places=3)
        self.assertAlmostEqual(cuts[0]["source_out"], 2.08, places=3)

    def test_remap_subtitles_to_cut_timeline(self):
        segs = [
            {"start": 0.5, "end": 2.0, "text": "một"},
            {"start": 5.0, "end": 6.0, "text": "hai"},
        ]
        cuts = self.cutter.compute_cuts_from_speech_segments(segs)
        subs = [
            {"start": 5.0, "end": 5.5, "text": "hai"},
            {"start": 3.0, "end": 4.0, "text": "nằm trong đoạn đã cắt"},
        ]
        out = self.cutter.remap_to_timeline(subs, cuts)

        self.assertEqual(len(out), 1)                       # phụ đề trong đoạn bị cắt phải bị bỏ
        first_cut_len = cuts[0]["source_out"] - cuts[0]["source_in"]
        offset_in_cut = 5.0 - cuts[1]["source_in"]
        self.assertAlmostEqual(out[0]["start"], first_cut_len + offset_in_cut, places=2)
        self.assertAlmostEqual(out[0]["end"] - out[0]["start"], 0.5, places=2)
        self.assertEqual(subs[0]["start"], 5.0)             # danh sách gốc không bị sửa

    def test_remap_without_cuts_returns_copies(self):
        subs = [{"start": 1.0, "end": 2.0, "text": "x"}]
        out = self.cutter.remap_to_timeline(subs, [])
        self.assertEqual(out, subs)
        self.assertIsNot(out[0], subs[0])

    def test_clamp_cuts_to_media_duration(self):
        cuts = [
            {"clip_index": 0, "source_in": 0.0, "source_out": 1.08, "duration": 1.08},
            {"clip_index": 1, "source_in": 1.5, "source_out": 2.0, "duration": 0.5},  # nằm ngoài video
        ]
        out = self.cutter.clamp_cuts(cuts, 1.0)
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["source_out"], 1.0)
        self.assertEqual(out[0]["duration"], 1.0)
        self.assertEqual(cuts[0]["source_out"], 1.08)       # không sửa danh sách gốc

    def test_clamp_cuts_noop_when_duration_unknown(self):
        cuts = [{"clip_index": 0, "source_in": 0.0, "source_out": 3.0, "duration": 3.0}]
        self.assertEqual(self.cutter.clamp_cuts(cuts, 0.0), cuts)


class TestChinLockPositions(unittest.TestCase):
    def test_px_to_capcut_transform_y(self):
        self.assertAlmostEqual(ChinLock.px_to_capcut_transform_y(1320), -0.375, places=3)
        self.assertEqual(ChinLock.px_to_capcut_transform_y(0), 1.0)
        self.assertEqual(ChinLock.px_to_capcut_transform_y(1920), -0.9)   # kẹp ở mức thấp nhất

    def test_anchor_lookup_and_attach(self):
        anchors = [
            {"timestamp": 0.0, "sub_top_y": 1300.0, "roll_deg": 0.0},
            {"timestamp": 1.0, "sub_top_y": 1400.0, "roll_deg": 0.0},
        ]
        self.assertEqual(ChinLock.anchor_y_at(anchors, -1.0), 1300.0)
        self.assertEqual(ChinLock.anchor_y_at(anchors, 0.5), 1300.0)
        self.assertEqual(ChinLock.anchor_y_at(anchors, 1.5), 1400.0)

        subs = [{"start": 0.2, "end": 0.8, "text": "a"}, {"start": 1.2, "end": 1.8, "text": "b"}]
        out = ChinLock().attach_subtitle_positions(subs, anchors)
        self.assertLess(out[1]["transform_y"], out[0]["transform_y"])      # neo thấp hơn -> transform_y nhỏ hơn
        self.assertNotIn("transform_y", subs[0])                           # không sửa danh sách gốc


class TestBrandEngineIsolation(unittest.TestCase):
    def test_instances_do_not_share_nested_state(self):
        e1 = BrandEngine()
        e1.get_fonts()["headline"] = "Font Đã Bị Sửa"
        e1.get_colors()["primary"] = "#000000"

        e2 = BrandEngine()
        self.assertEqual(e2.get_fonts()["headline"], DEFAULT_BRAND_KIT["fonts"]["headline"])
        self.assertNotEqual(e2.get_colors()["primary"], "#000000")
        self.assertNotEqual(DEFAULT_BRAND_KIT["fonts"]["headline"], "Font Đã Bị Sửa")


class TestPremiereXMLFixes(unittest.TestCase):
    def test_file_url_is_percent_encoded(self):
        url = _path_to_file_url("/tmp/thư mục/video 1.mp4")
        self.assertTrue(url.startswith("file://localhost"))
        self.assertNotIn(" ", url)
        self.assertIn("%20", url)

    def test_main_file_defined_once(self):
        tmp = tempfile.mkdtemp()
        try:
            out_xml = os.path.join(tmp, "seq.xml")
            cuts = [
                {"source_in": 0.0, "source_out": 3.0, "duration": 3.0},
                {"source_in": 3.5, "source_out": 7.0, "duration": 3.5},
                {"source_in": 8.0, "source_out": 9.0, "duration": 1.0},
            ]
            PremiereXMLBuilder(sequence_name="T").generate_xml_timeline("clip một.mp4", cuts, out_xml)

            root = ET.parse(out_xml).getroot()
            video_files = root.findall(".//video//clipitem/file")
            self.assertEqual(len(video_files), 3)
            full_defs = [f for f in video_files if f.find("pathurl") is not None]
            self.assertEqual(len(full_defs), 1)
            self.assertNotIn(" ", full_defs[0].find("pathurl").text)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class TestFindInboxVideo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _touch(self, *parts):
        path = os.path.join(self.tmp, *parts)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "wb").close()
        return path

    def test_sorted_and_case_insensitive(self):
        self._touch("notes.txt")
        self._touch("b.MP4")
        a = self._touch("a.mov")
        self.assertEqual(find_inbox_video(self.tmp), a)

    def test_skips_broll_and_music_folders(self):
        self._touch("broll", "x.mp4")
        raw = self._touch("raw", "y.mp4")
        self.assertEqual(find_inbox_video(self.tmp), raw)

    def test_empty_or_missing(self):
        self.assertIsNone(find_inbox_video(self.tmp))
        self.assertIsNone(find_inbox_video(os.path.join(self.tmp, "khong_ton_tai")))


class TestTranscriptSources(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.fake_video = os.path.join(self.tmp, "not_a_video.mp4")
        with open(self.fake_video, "w") as f:
            f.write("không phải video thật")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_json_transcript_is_used(self):
        tpath = os.path.join(self.tmp, "t.json")
        with open(tpath, "w", encoding="utf-8") as f:
            json.dump([{"start": 0.0, "end": 1.0, "text": "xin chào"}], f, ensure_ascii=False)
        res = WhisperTranscriber().load_or_transcribe(self.fake_video, transcript_json_path=tpath)
        self.assertEqual(res["mode"], "json")
        self.assertEqual(res["subtitles"][0]["text"], "xin chào")

    def test_missing_transcript_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            WhisperTranscriber().load_or_transcribe(self.fake_video, transcript_json_path="khong_co.json")

    def test_no_silent_mock_by_default(self):
        tr = WhisperTranscriber()
        with mock.patch.object(WhisperTranscriber, "transcribe", side_effect=TranscriberUnavailable("thiếu whisper")), \
             mock.patch.object(WhisperTranscriber, "detect_speech_segments", return_value=[]), \
             mock.patch.object(WhisperTranscriber, "get_media_duration", return_value=0.0):
            with self.assertRaises(RuntimeError):
                tr.load_or_transcribe(self.fake_video)

    def test_mock_only_when_allowed(self):
        tr = WhisperTranscriber()
        with mock.patch.object(WhisperTranscriber, "transcribe", side_effect=TranscriberUnavailable("thiếu whisper")), \
             mock.patch.object(WhisperTranscriber, "detect_speech_segments", return_value=[]), \
             mock.patch.object(WhisperTranscriber, "get_media_duration", return_value=0.0):
            res = tr.load_or_transcribe(self.fake_video, allow_mock=True,
                                        mock_text="một hai ba bốn năm sáu", mock_duration=6.0)
        self.assertEqual(res["mode"], "mock")
        self.assertTrue(res["subtitles"])

    def test_silence_mode_has_no_subtitles(self):
        tr = WhisperTranscriber()
        segs = [{"start": 0.0, "end": 2.0, "text": ""}]
        with mock.patch.object(WhisperTranscriber, "transcribe", side_effect=TranscriberUnavailable("thiếu whisper")), \
             mock.patch.object(WhisperTranscriber, "detect_speech_segments", return_value=segs):
            res = tr.load_or_transcribe(self.fake_video)
        self.assertEqual(res["mode"], "silence")
        self.assertEqual(res["segments"], segs)
        self.assertEqual(res["subtitles"], [])


if __name__ == "__main__":
    unittest.main()
