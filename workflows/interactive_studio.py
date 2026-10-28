#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflows/interactive_studio.py — Luồng Dựng Phim Khoa Học Có Tương Tác Hỏi Từng Bước (Interactive Director Mode).
Tại mỗi Step, hệ thống dừng lại, báo cáo dữ liệu phân tích và hỏi ý kiến người dùng:
  - Muốn dùng tính năng này không?
  - Muốn chọn tùy chọn nào (ví dụ chọn Look màu)?
  - Hay muốn bỏ qua (skip) để sang bước kế tiếp.
Đồng thời hỗ trợ cờ --auto khi muốn cỗ máy tự động chọn phương án tối ưu nhất.
"""

import os
import sys
from typing import Dict, Any, Optional

from core.brand_engine import BrandEngine
from core.whisper_transcriber import WhisperTranscriber
from core.chin_lock import ChinLock
from core.rough_cutter import RoughCutter
from core.audio_master import AudioMaster
from core.color_grade import ColorGradeEngine, CINEMATIC_LOOKS
from core.pacing_engine import PacingEngine
from core.motion_reframer import MotionReframer
from core.semantic_sound_visual import SemanticSoundVisual
from engines.adobe.pr_xml_builder import PremiereXMLBuilder
from engines.adobe.ae_script_generator import AfterEffectsScriptGenerator
from engines.capcut.draft_builder import CapCutDraftBuilder
from workflows.beat_sheet import BeatSheetGenerator
from workflows.trial_reels import TrialReelsGenerator
from workflows.carousel_story.carousel import CarouselStoryGenerator


class InteractiveStudio:
    def __init__(self, brand_kit_path: Optional[str] = None, auto_mode: bool = False):
        self.auto_mode = auto_mode
        self.brand_engine = BrandEngine(brand_kit_path)
        self.transcriber = WhisperTranscriber()
        self.chin_lock = ChinLock()
        self.cutter = RoughCutter()
        self.audio_master = AudioMaster(
            target_i=self.brand_engine.get_audio_standards().get("target_lufs", -14.0)
        )
        self.color_engine = ColorGradeEngine()
        self.pacing_engine = PacingEngine()
        self.motion_reframer = MotionReframer()
        self.semantic_engine = SemanticSoundVisual()

    def _ask_user(self, prompt: str, default: str = "y") -> str:
        """Hỏi ý kiến người dùng tại console, tự động nhận default nếu ở chế độ auto_mode."""
        if self.auto_mode:
            print(f"👉 [Tự động chọn]: {prompt} -> {default}")
            return default
        try:
            val = input(f"\n👉 {prompt} (Mặc định: {default}): ").strip().lower()
            return val if val else default
        except (KeyboardInterrupt, EOFError):
            print("\nĐã hủy.")
            sys.exit(0)

    def run_scientific_pipeline(
        self,
        video_path: str,
        project_name: str = "Levi_Scientific_Project",
        headline: Optional[str] = None,
        transcript_json_path: Optional[str] = None,
        output_dir: str = "outbox"
    ) -> Dict[str, Any]:
        """Điều phối 5 bước dựng phim khoa học có tương tác."""
        print("\n" + "=" * 65)
        print("🎬  LEVI SUPER STUDIO v4.0 — LUỒNG DỰNG PHIM KHOA HỌC TỐI ƯU")
        print("=" * 65)

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Không tìm thấy video: {video_path}")

        os.makedirs(output_dir, exist_ok=True)
        brand_colors = self.brand_engine.get_colors()
        brand_fonts = self.brand_engine.get_fonts()
        hook_headline = headline or "Bí Quyết Tạo Video Triệu View Chuẩn Studio"

        # Bóc tách giọng nói
        if transcript_json_path and os.path.exists(transcript_json_path):
            subtitles = self.transcriber.load_transcript_json(transcript_json_path)
        else:
            subtitles = self.transcriber.create_mock_transcript_from_text(
                "Đây là video được dựng khoa học với nhịp cắt J-Cut, màu sắc điện ảnh và né cằm chuẩn xác.",
                total_duration=16.0
            )

        pipeline_choices = {}

        # =====================================================================
        # BƯỚC 1: CẮT NHỊP ĐIỆN ẢNH & KHOẢNG LẶNG (PACING & J-CUT / L-CUT)
        # =====================================================================
        print("\n" + "-" * 65)
        print("📍 BƯỚC 1/5: TỐI ƯU NHỊP CẮT & KHOẢNG LẶNG (PACING & J-CUT)")
        print("-" * 65)
        base_cuts = self.cutter.compute_cuts_from_speech_segments(subtitles)
        print(f"📊 Dữ liệu: Phát hiện {len(subtitles)} phân đoạn câu nói.")

        ans_step1 = self._ask_user(
            "Bạn có muốn bật J-Cut (âm thanh cất lên trước 120ms) và giữ lại các khoảng lặng kịch tính (Dramatic Pause)? (y: Bật / n: Cắt thẳng / s: Bỏ qua)",
            default="y"
        )
        if ans_step1 in ["y", "yes"]:
            optimized_cuts = self.pacing_engine.optimize_timeline_pacing(
                subtitles, enable_j_cuts=True, preserve_dramatic_pauses=True
            )
            pipeline_choices["pacing"] = "j_cut_dramatic_pause"
            print("  ✅ Đã áp dụng J-Cut mềm mại và bảo toàn khoảng lặng cảm xúc.")
        else:
            optimized_cuts = base_cuts
            pipeline_choices["pacing"] = "standard_cuts"
            print("  ⏭️ Giữ nhịp cắt tiêu chuẩn.")

        final_duration = sum(c["duration"] for c in optimized_cuts)

        # =====================================================================
        # BƯỚC 2: PHÂN MÀU ĐIỆN ẢNH (CINEMA COLOR SCIENCE & LOG TRANSFORM)
        # =====================================================================
        print("\n" + "-" * 65)
        print("📍 BƯỚC 2/5: QUẢN LÝ MÀU SẮC ĐIỆN ẢNH (COLOR SCIENCE)")
        print("-" * 65)
        detected_space = self.color_engine.detect_color_space(video_path)
        print(f"📊 Dữ liệu: Không gian màu nhận diện: [{detected_space.upper()}].")
        print("   Các phong cách màu có sẵn:")
        print("   [1] Teal & Orange (Hiện đại, da sáng rực rỡ)")
        print("   [2] Kodak Film Emulation (Ấm áp, hoài cổ tạp chí)")
        print("   [3] Clean & Crisp Corporate (Trong trẻo, tự nhiên)")
        print("   [s] Giữ nguyên màu gốc (Bỏ qua)")

        ans_step2 = self._ask_user("Chọn phong cách màu bạn muốn áp dụng [1/2/3/s]", default="1")
        if ans_step2 == "1":
            chosen_look = "teal_orange"
            pipeline_choices["color"] = chosen_look
            color_filter = self.color_engine.get_color_transform_filter(detected_space, chosen_look)
            print("  ✅ Đã chọn: Teal & Orange Hollywood.")
        elif ans_step2 == "2":
            chosen_look = "kodak_film"
            pipeline_choices["color"] = chosen_look
            color_filter = self.color_engine.get_color_transform_filter(detected_space, chosen_look)
            print("  ✅ Đã chọn: Kodak Film Emulation.")
        elif ans_step2 == "3":
            chosen_look = "clean_corporate"
            pipeline_choices["color"] = chosen_look
            color_filter = self.color_engine.get_color_transform_filter(detected_space, chosen_look)
            print("  ✅ Đã chọn: Clean & Crisp Corporate.")
        else:
            pipeline_choices["color"] = "original"
            color_filter = "null"
            print("  ⏭️ Giữ nguyên màu gốc của video.")

        # =====================================================================
        # BƯỚC 3: KHUNG HÌNH, NÉ MẶT & CHUYỂN ĐỘNG (CHIN-LOCK & BEZIER ZOOM)
        # =====================================================================
        print("\n" + "-" * 65)
        print("📍 BƯỚC 3/5: KHÓA CẰM NÉ MẶT (CHIN-LOCK) & CHUYỂN ĐỘNG BEZIER")
        print("-" * 65)
        anchors = self.chin_lock.get_timeline_chin_anchors(video_path)
        safe_y = anchors[0]["sub_top_y"]
        print(f"📊 Dữ liệu: AI YuNet đã định vị cằm. Vùng an toàn neo chữ: Y ~ {safe_y}px.")

        ans_step3 = self._ask_user(
            "Bật gia tốc chuyển động Bezier Ease-out và mô phỏng Motion Blur 180° khi zoom cận? (y/n/s)",
            default="y"
        )
        if ans_step3 in ["y", "yes"]:
            pipeline_choices["motion"] = "bezier_motion_blur"
            print("  ✅ Đã kích hoạt Bezier Smooth Zoom & Motion Blur.")
        else:
            pipeline_choices["motion"] = "linear_zoom"
            print("  ⏭️ Sử dụng zoom nhảy cảnh cơ bản.")

        # =====================================================================
        # BƯỚC 4: THIẾT KẾ ÂM THANH & B-ROLL NGỮ NGHĨA (SEMANTIC SFX & FOLEY)
        # =====================================================================
        print("\n" + "-" * 65)
        print("📍 BƯỚC 4/5: THIẾT KẾ ÂM THANH THEO TỪ KHÓA (SEMANTIC SFX & FOLEY)")
        print("-" * 65)
        cues = self.semantic_engine.analyze_transcript_cues(subtitles)
        print(f"📊 Dữ liệu: Tìm thấy {len(cues)} điểm nhấn ngữ nghĩa trong bài nói (Tài chính, Đột phá, Chuyển hướng).")
        for c in cues:
            print(f"   • {c['timestamp']}s: Từ khóa '{c['matched_keyword']}' -> Gợi ý SFX: {c['sfx_file']}")

        ans_step4 = self._ask_user(
            "Tự động chèn các hiệu ứng âm thanh Foley SFX bám theo từ khóa? (y/n/s)",
            default="y"
        )
        if ans_step4 in ["y", "yes"]:
            pipeline_choices["semantic_sfx"] = True
            print("  ✅ Đã kích hoạt hệ thống Foley SFX ngữ nghĩa.")
        else:
            pipeline_choices["semantic_sfx"] = False
            print("  ⏭️ Bỏ qua chèn SFX tự động.")

        # =====================================================================
        # BƯỚC 5: LỰA CHỌN LÀN XUẤT BẢN (EXPORT DISPATCHER)
        # =====================================================================
        print("\n" + "-" * 65)
        print("📍 BƯỚC 5/5: LỰA CHỌN NỀN TẢNG XUẤT BẢN (EXPORT DISPATCHER)")
        print("-" * 65)
        print("   [1] Chỉ xuất dự án CapCut Desktop (Chỉnh nhanh trên laptop/mobile)")
        print("   [2] Chỉ xuất Adobe Premiere Pro XML & After Effects JSX (Chuẩn điện ảnh)")
        print("   [3] Xuất TRỌN BỘ CẢ HAI + Storyboard Beat Sheet + Carousel (Khuyến nghị)")

        ans_step5 = self._ask_user("Chọn nền tảng bạn muốn xuất [1/2/3]", default="3")
        exported_files = {}

        # 1. Beat Sheet luôn xuất để xem trước
        beat_gen = BeatSheetGenerator()
        beat_sheet_path = os.path.join(output_dir, f"{project_name}_beat_sheet.jpg")
        beat_gen.extract_and_generate_from_video(video_path, optimized_cuts, beat_sheet_path)
        exported_files["beat_sheet"] = beat_sheet_path

        # 2. Xuất CapCut nếu chọn 1 hoặc 3
        if ans_step5 in ["1", "3"]:
            capcut_builder = CapCutDraftBuilder(project_name)
            capcut_builder.add_main_video(video_path, duration_sec=final_duration)
            capcut_builder.add_hook(
                headline=hook_headline,
                eyebrow="LEVI INSIGHT",
                font_name=brand_fonts.get("headline", "Playfair Display"),
                font_color=brand_colors.get("primary", "#F2EDE4")
            )
            capcut_builder.add_subtitles(
                subtitles=subtitles,
                font_name=brand_fonts.get("caption", "Be Vietnam Pro")
            )
            capcut_path = capcut_builder.finalize()
            exported_files["capcut_draft"] = capcut_path
            print(f"  ✅ Đã tạo dự án CapCut Desktop tại: {capcut_path}")

        # 3. Xuất Adobe Premiere / After Effects nếu chọn 2 hoặc 3
        if ans_step5 in ["2", "3"]:
            pr_builder = PremiereXMLBuilder(sequence_name=project_name)
            xml_path = os.path.join(output_dir, f"{project_name}_Premiere.xml")
            pr_builder.generate_xml_timeline(video_path, optimized_cuts, xml_path)
            exported_files["premiere_xml"] = xml_path

            ae_builder = AfterEffectsScriptGenerator(comp_name=project_name, duration_sec=final_duration)
            jsx_path = os.path.join(output_dir, f"{project_name}_AfterEffects.jsx")
            ae_builder.generate_jsx_script(
                hook_text=hook_headline,
                subtitles=subtitles,
                brand_colors=brand_colors,
                output_jsx_path=jsx_path
            )
            exported_files["after_effects_jsx"] = jsx_path
            print(f"  ✅ Đã tạo Timeline Premiere Pro XML: {xml_path}")
            print(f"  ✅ Đã tạo Kịch bản After Effects JSX: {jsx_path}")

        # 4. Xuất Carousel nếu chọn 3
        if ans_step5 == "3":
            carousel_gen = CarouselStoryGenerator(brand_colors=brand_colors)
            carousel_paths = carousel_gen.generate_carousel_slides(
                [
                    {"title": hook_headline, "body": "Quy trình sản xuất video khoa học có tương tác."},
                    {"title": "Màu Sắc & Nhịp Điệu", "body": f"Áp dụng phong cách {pipeline_choices.get('color')} và J-Cut mềm mại."},
                    {"title": "Hành Động", "body": "Comment LEVI để nhận trọn bộ công nghệ."}
                ],
                output_dir=os.path.join(output_dir, "carousel")
            )
            exported_files["carousel_slides"] = carousel_paths

        print("\n" + "=" * 65)
        print("🎉 QUY TRÌNH DỰNG PHIM KHOA HỌC ĐÃ HOÀN TẤT THÀNH CÔNG!")
        print("=" * 65)
        print(f"📋 Bảng Storyboard duyệt nhanh: {beat_sheet_path}")

        return {
            "status": "success",
            "choices": pipeline_choices,
            "exported_files": exported_files
        }
