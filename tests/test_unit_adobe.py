#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_unit_adobe.py — Unit tests cho các module tích hợp Adobe Premiere Pro và After Effects.
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from engines.adobe.pr_xml_builder import PremiereXMLBuilder
from engines.adobe.ae_script_generator import AfterEffectsScriptGenerator


class TestAdobeModules(unittest.TestCase):
    def test_premiere_xml_generation(self):
        builder = PremiereXMLBuilder(sequence_name="Test_Sequence", width=1080, height=1920)
        output_xml = os.path.join(REPO_ROOT, "outbox", "test_premiere.xml")
        cuts = [
            {"source_in": 0.0, "source_out": 3.0, "duration": 3.0},
            {"source_in": 3.5, "source_out": 7.0, "duration": 3.5}
        ]
        builder.generate_xml_timeline("test_video.mp4", cuts, output_xml)
        self.assertTrue(os.path.exists(output_xml))

        # Kiểm tra tính hợp lệ của cú pháp XML
        tree = ET.parse(output_xml)
        root = tree.getroot()
        self.assertEqual(root.tag, "xmeml")
        self.assertEqual(root.attrib.get("version"), "4")

        # Dọn dẹp
        if os.path.exists(output_xml):
            os.remove(output_xml)

    def test_after_effects_jsx_generation(self):
        gen = AfterEffectsScriptGenerator(comp_name="Test_AE_Comp", duration_sec=15.0)
        output_jsx = os.path.join(REPO_ROOT, "outbox", "test_ae.jsx")
        brand_colors = {"primary": "#F2EDE4", "highlight": "#720000"}
        subtitles = [{"start": 0.0, "end": 2.5, "text": "Kiểm tra subtitle After Effects"}]

        gen.generate_jsx_script(
            hook_text="Hook Thử Nghiệm",
            subtitles=subtitles,
            brand_colors=brand_colors,
            output_jsx_path=output_jsx
        )
        self.assertTrue(os.path.exists(output_jsx))

        with open(output_jsx, "r", encoding="utf-8") as f:
            code = f.read()

        self.assertIn("Test_AE_Comp", code)
        self.assertIn("Inertial Bounce", code)
        self.assertIn("ParagraphJustification.CENTER_JUSTIFY", code)

        # Dọn dẹp
        if os.path.exists(output_jsx):
            os.remove(output_jsx)


if __name__ == "__main__":
    unittest.main()
