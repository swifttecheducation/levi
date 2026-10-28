#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
studio.py — CLI ĐIỀU HÀNH TRUNG TÂM (LEVI SUPER STUDIO MASTER CLI v4.0).
Quản lý toàn bộ cỗ máy dựng phim đa kênh tự động và tương tác:
  - director: Chế độ Đạo Diễn Khoa Học Từng Bước (Hỏi người dùng từng tính năng)
  - autopilot: Dựng 1-chạm tự động từ video thô trong inbox/
  - premiere: Xuất Premiere Pro XML Timeline
  - ae: Xuất kịch bản After Effects JSX
  - beat-sheet: Xuất Storyboard Beat Sheet duyệt nhanh
  - carousel: Sinh bộ bài đăng Instagram Carousel
"""

import os
import sys
import argparse
import glob
from typing import Optional

# Bắt buộc UTF-8 trên Windows console
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        try:
            _s.reconfigure(encoding="utf-8")
        except Exception:
            pass

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from workflows.autopilot import AutopilotEngine
from workflows.interactive_studio import InteractiveStudio
from workflows.onboarding import OnboardingWizard
from workflows.brand_wizard import BrandWizard
from core.brand_engine import BrandEngine
from core.styles_library import StylesLibrary, CURATED_PRESETS
from core.font_manager import FontManager, FONT_FAMILIES, CURATED_FONT_PACKS
from engines.adobe.pr_xml_builder import PremiereXMLBuilder
from engines.adobe.ae_script_generator import AfterEffectsScriptGenerator
from workflows.beat_sheet import BeatSheetGenerator
from workflows.carousel_story.carousel import CarouselStoryGenerator


def find_inbox_video(inbox_dir: str = "inbox") -> Optional[str]:
    """
    Tự động tìm file video đầu tiên trong thư mục inbox/:
    Hỗ trợ cả thả trực tiếp vào inbox/ hoặc trong các thư mục con (vd: inbox/video_chinh/).
    """
    if not os.path.exists(inbox_dir):
        return None
    patterns = ["*.mp4", "*.mov", "*.m4v", "*.mkv"]
    # 1. Tìm trực tiếp ngay trong inbox/
    for p in patterns:
        files = glob.glob(os.path.join(inbox_dir, p))
        if files:
            return files[0]

    # 2. Tìm trong các thư mục con cấp 1 (vd: inbox/video_chinh/, inbox/raw/)
    for p in patterns:
        sub_files = glob.glob(os.path.join(inbox_dir, "*", p))
        for f in sub_files:
            folder_name = os.path.basename(os.path.dirname(f)).lower()
            # Bỏ qua thư mục broll hoặc nhạc
            if folder_name not in ["broll", "nhac_nen", "sfx", "logo_watermark"]:
                return f
    return None


def main():
    parser = argparse.ArgumentParser(
        description="🎬 Levi Super Studio v4.0 — Master Video & Multi-Channel Automation Engine"
    )
    subparsers = parser.add_subparsers(dest="command", help="Lệnh thực thi")

    # 1. Interactive Director Mode (HỎI TỪNG BƯỚC)
    dir_parser = subparsers.add_parser("director", help="Chế độ Đạo Diễn Khoa Học (Hỏi ý kiến bạn tại từng bước)")
    dir_parser.add_argument("--video", "-v", type=str, default=None, help="Đường dẫn file video thô (hoặc tự quét inbox/)")
    dir_parser.add_argument("--name", "-n", type=str, default="Levi_Director_Project", help="Tên dự án")
    dir_parser.add_argument("--headline", "-H", type=str, default=None, help="Tiêu đề câu Hook chính")
    dir_parser.add_argument("--mix", "-m", type=str, default=None, help="Mã phong cách từ Thư viện 105 phong cách (vd: H1,C1,L1,X5)")
    dir_parser.add_argument("--auto", action="store_true", help="Chạy tự động các lựa chọn khuyến nghị không cần hỏi")

    # 2. Autopilot Mode (TỰ ĐỘNG 1-CHẠM)
    ap_parser = subparsers.add_parser("autopilot", help="Chạy cỗ máy dựng 1-chạm tự động hoàn toàn từ A-Z")
    ap_parser.add_argument("--video", "-v", type=str, default=None, help="Đường dẫn file video thô (hoặc tự quét inbox/)")
    ap_parser.add_argument("--name", "-n", type=str, default="Levi_Project", help="Tên dự án")
    ap_parser.add_argument("--headline", "-H", type=str, default=None, help="Tiêu đề câu Hook chính")
    ap_parser.add_argument("--subtitles", "-s", type=str, default=None, help="File transcript JSON (nếu có sẵn)")
    ap_parser.add_argument("--mix", "-m", type=str, default=None, help="Mã phong cách từ Thư viện 105 phong cách (vd: H1,C1,L1,X5)")

    # 3. Premiere Pro XML Command
    pr_parser = subparsers.add_parser("premiere", help="Chỉ xuất Timeline chuẩn cho Adobe Premiere Pro (.xml)")
    pr_parser.add_argument("--video", "-v", type=str, required=True, help="Đường dẫn file video")
    pr_parser.add_argument("--name", "-n", type=str, default="Premiere_Sequence", help="Tên sequence")

    # 4. After Effects JSX Command
    ae_parser = subparsers.add_parser("ae", help="Chỉ xuất ExtendScript JSX cho After Effects")
    ae_parser.add_argument("--text", "-t", type=str, required=True, help="Câu Hook headline")
    ae_parser.add_argument("--name", "-n", type=str, default="AE_Comp", help="Tên composition")

    # 5. Beat Sheet Command
    bs_parser = subparsers.add_parser("beat-sheet", help="Xuất bảng ảnh Storyboard duyệt nhanh trước khi render")
    bs_parser.add_argument("--video", "-v", type=str, required=True, help="Đường dẫn video")

    # 6. Carousel Command
    car_parser = subparsers.add_parser("carousel", help="Sinh bộ bài đăng vuốt ngang Instagram Carousel")
    car_parser.add_argument("--headline", "-H", type=str, default="Insight Mới", help="Tiêu đề slide 1")

    # 7. Status Check
    subparsers.add_parser("status", help="Kiểm tra môi trường và Brand Kit")

    # 8. Onboarding / Setup Wizard
    subparsers.add_parser("onboard", help="Chạy quy trình Onboarding & Thiết lập ban đầu (4 bước)")
    subparsers.add_parser("setup", help="Bí danh của onboard")

    # 9. Brand Kit Deep Interview Wizard
    subparsers.add_parser("brand", help="Phỏng vấn chuyên sâu thiết lập Brand Kit 7 trụ cột")
    subparsers.add_parser("brand-kit", help="Bí danh của brand")

    # 10. Styles Library (105 Styles from Siatruong)
    styles_p = subparsers.add_parser("styles", help="Thư viện 105 phong cách dựng video rảnh tay")
    styles_p.add_argument("--list", "-l", action="store_true", help="Liệt kê 10 danh mục & 105 phong cách")
    styles_p.add_argument("--cat", "-c", type=str, help="Xem chi tiết phong cách trong danh mục (H, C, L, P, V, B, X, M, S, G)")
    styles_p.add_argument("--search", "-s", type=str, help="Tìm kiếm phong cách theo từ khóa")
    styles_p.add_argument("--mix", "-m", type=str, help="Tạo bản tóm tắt yêu cầu dựng từ danh sách mã phong cách (vd: H1,C1,L1,X5)")
    styles_p.add_argument("--presets", "-p", action="store_true", help="Xem các bộ phối mẫu gợi ý (Editorial, Apple, Hands-off Reels...)")

    # 11. Font Catalog Command
    fonts_p = subparsers.add_parser("fonts", help="Tra cứu toàn bộ kho 32 font chữ Việt hóa & 14 họ font")
    fonts_p.add_argument("--list", "-l", action="store_true", help="Liệt kê 14 họ font & các tệp font chi tiết")
    fonts_p.add_argument("--packs", "-p", action="store_true", help="Xem 6 bộ phối font chữ gợi ý")

    args = parser.parse_args()

    if not args.command or args.command == "status":
        print("\n" + "=" * 65)
        print("🎬  LEVI SUPER STUDIO v4.0 — TRẠNG THÁI HỆ THỐNG")
        print("=" * 65)
        brand_path = os.path.join(HERE, "brand-kit.md")
        brand = BrandEngine(brand_path)
        print(f"✅ Thương hiệu   : {brand.brand['name']}")
        print(f"🎨 Bộ phong cách : {brand.brand['style_pack']}")
        print(f"🏷️  Mã phong cách : {', '.join(brand.get_style_codes())}")
        print(f"🔤 Font chữ      : Headline: {brand.get_fonts()['headline']} | Body: {brand.get_fonts()['caption']}")
        print(f"🔊 Chuẩn âm thanh: EBU R128 ({brand.get_audio_standards()['target_lufs']} LUFS)")
        inbox_vid = find_inbox_video(os.path.join(HERE, "inbox"))
        print(f"📥 Video trong inbox/: {inbox_vid if inbox_vid else 'Chưa có (Hãy thả video vào inbox/)'}")
        print("=" * 65 + "\n")
        return

    brand_file = os.path.join(HERE, "brand-kit.md")

    if args.command in ["onboard", "setup"]:
        wizard = OnboardingWizard(brand_kit_path=brand_file)
        wizard.run_full_onboarding()
        return

    if args.command in ["brand", "brand-kit"]:
        wizard = BrandWizard(brand_kit_path=brand_file)
        wizard.run_deep_interview()
        return

    if args.command == "styles":
        sl = StylesLibrary()
        if args.cat:
            cat_id = args.cat.upper().strip()
            styles = sl.get_styles_in_category(cat_id)
            cat_name = sl.by_cat.get(cat_id, {}).get("name", cat_id)
            print(f"\n📂 DANH MỤC [{cat_id}]: {cat_name} ({len(styles)} phong cách)")
            print("=" * 65)
            for it in styles:
                print(f"👉 [{it['code']}] {it['name']}")
                print(f"   {it['what']}\n")
            return

        if args.search:
            res = sl.search_styles(args.search)
            print(f"\n🔍 KẾT QUẢ TÌM KIẾM CHO: '{args.search}' ({len(res)} phong cách)")
            print("=" * 65)
            for it in res:
                print(f"👉 [{it['code']}] {it['name']} ({it['cat_name']})")
                print(f"   {it['what']}\n")
            return

        if args.mix:
            codes = [c.strip().upper() for c in args.mix.split(",") if c.strip()]
            prompt = sl.compose_mix_prompt(codes)
            print("\n" + "=" * 65)
            print("✨ BẢN TÓM TẮT YÊU CẦU DỰNG (MIX PROMPT):")
            print("=" * 65)
            print(prompt)
            print("=" * 65 + "\n")
            return

        if args.presets:
            print("\n" + "=" * 65)
            print("🌟 BỘ PHỐI MẪU GỢI Ý (CURATED PRESETS):")
            print("=" * 65)
            for k, p in sl.list_presets().items():
                print(f"🔹 [{k}] {p['name']}")
                print(f"   Mã: {', '.join(p['codes'])}")
                print(f"   Mô tả: {p['description']}\n")
            return

        # Mặc định hoặc --list: hiển thị tổng quan 10 danh mục
        print("\n" + "=" * 65)
        print(f"🎨 THƯ VIỆN 105 PHONG CÁCH DỰNG VIDEO (SIATRUONG.COM INTEGRATION)")
        print(f"   Tổng cộng: {sl.total_count} phong cách phân chia thành 10 nhóm")
        print("=" * 65)
        for cat in sl.list_categories():
            print(f"📁 [{cat['id']}] {cat['name']:<30} : {cat['count']} phong cách")
            print(f"   ↳ {cat['blurb']}")
        print("\n💡 Gợi ý lệnh tra cứu:")
        print("   python studio.py styles -c H             (Xem chi tiết nhóm Hook)")
        print("   python studio.py styles -s \"apple\"       (Tìm phong cách kiểu Apple)")
        print("   python studio.py styles -m \"H1,C1,L1,X5\"  (Tạo yêu cầu dựng video)")
        print("   python studio.py styles -p               (Xem các bộ phối gợi ý)")
        print("=" * 65 + "\n")
        return

    if args.command == "fonts":
        fm = FontManager()
        if args.packs:
            print("\n" + "=" * 65)
            print("🔤 6 BỘ PHỐI FONT CHỮ GỢI Ý (CURATED FONT PACKS):")
            print("=" * 65)
            for k, p in fm.list_packs().items():
                print(f"🔹 [{k}] {p['name']}")
                print(f"   Headline: {p['headline']} | Caption: {p['caption']} | Accent: {p['accent']}")
                print(f"   Mô tả: {p['description']}\n")
            print("=" * 65 + "\n")
            return

        print("\n" + "=" * 65)
        print(f"🔤 KHO 32 TỆP FONT CHỮ VIỆT HÓA 100% ({fm.total_families} HỌ FONT)")
        print("=" * 65)
        for fam in fm.list_families():
            print(f"📌 {fam['name']} — [{fam['category']}]")
            print(f"   ↳ {fam['description']}")
            print(f"   ↳ Files: {', '.join(fam['files'].values())}")
            print(f"   ↳ Phù hợp nhất: {', '.join(fam['best_for'])}\n")
        print("💡 Gợi ý lệnh tra cứu:")
        print("   python studio.py fonts -p                (Xem 6 bộ phối font khuyên dùng)")
        print("=" * 65 + "\n")
        return

    if args.command == "director":
        target_video = args.video or find_inbox_video(os.path.join(HERE, "inbox"))
        if not target_video:
            print("❌ Lỗi: Không tìm thấy video trong inbox/ và bạn chưa chỉ định --video!")
            print("👉 Hãy thả video vào thư mục 'inbox/' hoặc chạy:")
            print("   python studio.py director --video duong/dan/video.mp4")
            sys.exit(1)

        studio = InteractiveStudio(brand_kit_path=brand_file, auto_mode=args.auto)
        studio.run_scientific_pipeline(
            video_path=target_video,
            project_name=args.name,
            headline=args.headline
        )

    elif args.command == "autopilot":
        target_video = args.video or find_inbox_video(os.path.join(HERE, "inbox"))
        if not target_video:
            print("❌ Lỗi: Không tìm thấy video trong inbox/ và bạn chưa chỉ định --video!")
            print("👉 Hãy thả video vào thư mục 'inbox/' hoặc chạy:")
            print("   python studio.py autopilot --video duong/dan/video.mp4")
            sys.exit(1)

        engine = AutopilotEngine(brand_kit_path=brand_file)
        engine.run_autopilot(
            video_path=target_video,
            project_name=args.name,
            headline=args.headline,
            transcript_json_path=args.subtitles
        )

    elif args.command == "premiere":
        pr = PremiereXMLBuilder(sequence_name=args.name)
        out_xml = os.path.join(HERE, "outbox", f"{args.name}.xml")
        pr.generate_xml_timeline(
            main_video_path=args.video,
            cuts=[{"source_in": 0.0, "source_out": 10.0, "duration": 10.0}],
            output_xml_path=out_xml
        )
        print(f"✅ Đã tạo Timeline Premiere Pro XML tại: {out_xml}")

    elif args.command == "ae":
        ae = AfterEffectsScriptGenerator(comp_name=args.name)
        out_jsx = os.path.join(HERE, "outbox", f"{args.name}.jsx")
        brand = BrandEngine(brand_file)
        ae.generate_jsx_script(
            hook_text=args.text,
            subtitles=[{"start": 0.0, "end": 3.0, "text": args.text}],
            brand_colors=brand.get_colors(),
            output_jsx_path=out_jsx
        )
        print(f"✅ Đã tạo kịch bản After Effects ExtendScript tại: {out_jsx}")

    elif args.command == "beat-sheet":
        bs = BeatSheetGenerator()
        out_jpg = os.path.join(HERE, "outbox", "beat_sheet.jpg")
        bs.extract_and_generate_from_video(
            video_path=args.video,
            cuts=[{"source_in": 0.0, "duration": 3.0}, {"source_in": 3.0, "duration": 3.0}],
            output_path=out_jpg
        )
        print(f"✅ Đã xuất Beat Sheet tại: {out_jpg}")

    elif args.command == "carousel":
        brand = BrandEngine(brand_file)
        car = CarouselStoryGenerator(brand_colors=brand.get_colors())
        slides = car.generate_carousel_slides(
            [
                {"title": args.headline, "body": "Bí quyết dựng video đa kênh chuẩn điện ảnh."},
                {"title": "Làn Kép Song Song", "body": "CapCut cho bản nhanh, Premiere & AE cho bản rạp."},
                {"title": "Hành Động Ngay", "body": "Inbox LEVI để nhận toàn bộ mã nguồn."}
            ],
            output_dir=os.path.join(HERE, "outbox", "carousel")
        )
        print(f"✅ Đã xuất {len(slides)} slides Carousel tại: outbox/carousel/")


if __name__ == "__main__":
    main()
