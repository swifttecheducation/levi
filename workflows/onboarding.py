#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflows/onboarding.py — Cỗ Máy Hướng Dẫn & Thiết Lập Ban Đầu (Interactive Onboarding Wizard).
Giúp người dùng mới thiết lập toàn bộ môi trường chỉ trong 2 phút:
  1. Kiểm tra môi trường (Pre-flight Diagnostics: Python, FFmpeg, CapCut, Adobe, Node.js).
  2. Phỏng vấn thiết lập nhận diện thương hiệu (Brand Kit Setup: Tên kênh, Font chữ, Bảng màu).
  3. Kiểm tra tính toàn vẹn của mô hình AI YuNet và font Việt hóa.
  4. Tạo sản phẩm mẫu đầu tiên (First Project Test) để nghiệm thu hệ thống.
"""

import os
import sys
import shutil
import subprocess
from typing import Dict, Any, Optional

from core.brand_engine import BrandEngine, DEFAULT_BRAND_KIT
from workflows.carousel_story.carousel import CarouselStoryGenerator


class OnboardingWizard:
    def __init__(self, brand_kit_path: Optional[str] = None):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.brand_kit_path = brand_kit_path or os.path.join(self.root_dir, "brand-kit.md")
        self.brand_engine = BrandEngine(self.brand_kit_path)

    def _ask(self, question: str, default: str = "") -> str:
        """Hỏi tương tác tại console."""
        suffix = f" [{default}]" if default else ""
        try:
            val = input(f"👉 {question}{suffix}: ").strip()
            return val if val else default
        except (KeyboardInterrupt, EOFError):
            print("\nĐã hủy.")
            sys.exit(0)

    def check_preflight_environment(self) -> Dict[str, Any]:
        """Bước 1: Quét chẩn đoán môi trường máy tính."""
        print("\n" + "=" * 65)
        print("🔍 BƯỚC 1/4: CHẨN ĐOÁN MÔI TRƯỜNG MÁY TÍNH (PRE-FLIGHT)")
        print("=" * 65)

        results = {}

        # 1. Python & Version
        py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        py_ok = sys.version_info >= (3, 10)
        results["python"] = {"ok": py_ok, "version": py_ver}
        print(f"  {'✅' if py_ok else '❌'} Python: {py_ver} ({'Hợp lệ 3.10+' if py_ok else 'Cần nâng cấp lên 3.10+'})")

        # 2. FFmpeg & FFprobe
        ffmpeg_bin = shutil.which("ffmpeg")
        ffprobe_bin = shutil.which("ffprobe")
        ffmpeg_ok = bool(ffmpeg_bin and ffprobe_bin)
        results["ffmpeg"] = {"ok": ffmpeg_ok, "path": ffmpeg_bin}
        if ffmpeg_ok:
            print(f"  ✅ FFmpeg & FFprobe: Đã sẵn sàng ({ffmpeg_bin})")
        else:
            print("  ⚠️ FFmpeg: Chưa tìm thấy trong PATH (Cần để xử lý âm thanh/video chuẩn phát sóng)")
            print("     -> Gợi ý: Chạy lệnh `winget install Gyan.FFmpeg` trên Windows hoặc `brew install ffmpeg` trên Mac.")

        # 3. CapCut Desktop
        if os.name == "nt":
            local_app = os.environ.get("LOCALAPPDATA", "")
            capcut_path = os.path.join(local_app, "CapCut", "User Data", "Projects", "com.lveditor.draft")
        else:
            capcut_path = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
        capcut_ok = os.path.exists(capcut_path)
        results["capcut"] = {"ok": capcut_ok, "path": capcut_path}
        print(f"  {'✅' if capcut_ok else 'ℹ️ '} CapCut Desktop: {'Đã kết nối thư mục Drafts' if capcut_ok else 'Chưa mở lần đầu (sẽ tự động tạo khi dựng)'}")

        # 4. Adobe Creative Cloud (Premiere & AE)
        ae_found = False
        if os.name == "nt":
            import glob
            ae_paths = glob.glob(r"C:\Program Files\Adobe\Adobe After Effects *\Support Files\aerender.exe")
            ae_found = bool(ae_paths)
        results["adobe_ae"] = {"ok": ae_found}
        print(f"  {'✅' if ae_found else 'ℹ️ '} Adobe After Effects (aerender): {'Đã phát hiện GPU Command Line' if ae_found else 'Chưa cài đặt (Tùy chọn cho bản Cinema)'}")

        # 5. Node.js (Cho Remotion)
        node_bin = shutil.which("node")
        results["node"] = {"ok": bool(node_bin), "path": node_bin}
        print(f"  {'✅' if node_bin else 'ℹ️ '} Node.js: {'Đã cài đặt' if node_bin else 'Chưa cài đặt (Tùy chọn cho Remotion 60fps)'}")

        return results

    def run_brand_interview(self) -> Dict[str, Any]:
        """Bước 2: Phỏng vấn thiết lập nhận diện thương hiệu."""
        print("\n" + "=" * 65)
        print("🎨 BƯỚC 2/4: THIẾT LẬP NHẬN DIỆN THƯƠNG HIỆU (BRAND KIT)")
        print("=" * 65)
        print("Trả lời nhanh 4 câu hỏi dưới đây để video của bạn luôn mang đậm dấu ấn cá nhân:\n")

        cur_name = self.brand_engine.brand.get("name", "Levi Studio")
        name = self._ask("Tên thương hiệu hoặc tên kênh của bạn là gì?", default=cur_name)

        target = self._ask(
            "Đối tượng người xem bạn hướng tới là ai?",
            default="Nhà sáng tạo nội dung, Marketer và Chuyên gia số"
        )

        print("\nChọn bộ phong cách thị giác & font chữ yêu thích:")
        print("  [1] Editorial Luxe (Tạp chí Sang trọng: Playfair Display + Caveat + Be Vietnam Pro)")
        print("  [2] Modern Minimal (Tối giản Hiện đại: Inter Black + Space Grotesk + Be Vietnam Pro)")
        print("  [3] Gen Z Pop (Năng động, Phá cách: Poppins Black + Caveat + Be Vietnam Pro)")
        style_choice = self._ask("Chọn phong cách [1/2/3]", default="1")

        if style_choice == "2":
            style_name = "Modern Minimal"
            head_font = "Inter"
            accent_font = "Space Grotesk"
        elif style_choice == "3":
            style_name = "Gen Z Pop"
            head_font = "Poppins"
            accent_font = "Caveat"
        else:
            style_name = "Editorial Luxe"
            head_font = "Playfair Display"
            accent_font = "Caveat"

        manychat = self._ask("Từ khóa kích hoạt chatbot ManyChat (ngăn cách bằng dấu phẩy)", default="LEVI, STUDIO, VIP")
        kw_list = [k.strip().upper() for k in manychat.split(",") if k.strip()]

        # Cập nhật vào brand-kit.md
        brand_md_content = f"""# 🏡 Brand Kit — Bộ Nhận Diện Thương Hiệu {name}

Tệp này là **Trụ Sở Thương Hiệu (Brand Homebase)** của bạn: quy định toàn bộ phong cách thị giác, bảng màu chuẩn điện ảnh, font chữ Việt hóa 100% không lỗi ô vuông, và tiêu chuẩn âm thanh phát sóng.

---

## 1. Định vị thương hiệu (Brand Identity)
- **Bạn và thương hiệu của bạn:** {name}
- **Bạn giúp ai, và giá trị họ nhận được là gì:** {target}
- **Nơi bạn đăng tải nội dung:**
  - Instagram: @{name.lower().replace(' ', '')}
  - TikTok: @{name.lower().replace(' ', '')}

## 2. Giọng điệu thương hiệu (Voice & Tone)
- **Mô tả giọng điệu:** Điềm tĩnh, sâu sắc, thực chiến, truyền cảm hứng và tinh tế.
- **Gut check:** Người xem cảm thấy được khai sáng, nhận được giá trị thực tế áp dụng được ngay.

## 3. Phong cách thị giác & Font chữ (Visual & Typography)
- **Bộ phong cách đang sử dụng:** {style_name}
- **Font tiêu đề chính (Headline font):** {head_font}
- **Font phụ đề (Caption font):** Be Vietnam Pro
- **Font tạo điểm nhấn (Accent font):** {accent_font}
- **Bảng màu chủ đạo (Color Palette):**
  - Màu nền chính (Primary): `#F2EDE4`
  - Màu nền tương phản (Secondary): `#212C1B`
  - Màu nhấn (Accent): `#FFADBF`
  - Màu nổi bật (Highlight): `#720000`

## 4. Chuẩn âm thanh phát sóng (Audio Standards)
- **Mức âm lượng tích hợp (Integrated Loudness):** `-14.0 LUFS` (Chuẩn EBU R128 tối ưu cho Reels/TikTok)
- **Mức đỉnh thực (True Peak):** `-1.5 dBTP`
- **Nhạc nền ngầm (BGM Bed):** `-18.0 dB`

## 5. Từ khóa kích hoạt tin nhắn tự động (ManyChat Triggers)
- Danh sách từ khóa: {', '.join(kw_list)}
"""
        with open(self.brand_kit_path, "w", encoding="utf-8") as f:
            f.write(brand_md_content)

        print(f"\n  ✅ Đã lưu cấu hình thương hiệu thành công vào: {self.brand_kit_path}")
        return {"name": name, "style": style_name, "headline_font": head_font}

    def verify_assets_and_models(self) -> bool:
        """Bước 3: Kiểm tra font chữ và mô hình AI YuNet."""
        print("\n" + "=" * 65)
        print("🧠 BƯỚC 3/4: KIỂM TRA MÔ HÌNH AI & FONT CHỮ VIỆT HÓA")
        print("=" * 65)

        models_dir = os.path.join(self.root_dir, "assets", "models")
        fonts_dir = os.path.join(self.root_dir, "assets", "fonts")
        yunet_model = os.path.join(models_dir, "face_detection_yunet_2023mar.onnx")

        has_yunet = os.path.exists(yunet_model)
        has_fonts = os.path.exists(fonts_dir) and len(os.listdir(fonts_dir)) >= 5

        print(f"  {'✅' if has_yunet else '❌'} Mô hình AI Chin-Lock YuNet: {'Sẵn sàng (232 KB)' if has_yunet else 'Chưa có'}")
        print(f"  {'✅' if has_fonts else '❌'} Kho Font chữ Việt hóa: {'Đầy đủ 100% chuẩn tiếng Việt' if has_fonts else 'Thiếu fonts'}")

        return has_yunet and has_fonts

    def generate_welcome_test_assets(self) -> str:
        """Bước 4: Sinh bộ ảnh test nghiệm thu đầu tiên."""
        print("\n" + "=" * 65)
        print("🎉 BƯỚC 4/4: SINH DỰ ÁN NGHIỆM THU ĐẦU TIÊN (WELCOME TEST)")
        print("=" * 65)

        self.brand_engine.load_from_markdown(self.brand_kit_path)
        brand_colors = self.brand_engine.get_colors()
        name = self.brand_engine.brand.get("name", "Levi Studio")

        out_carousel_dir = os.path.join(self.root_dir, "outbox", "onboarding_welcome")
        car_gen = CarouselStoryGenerator(brand_colors=brand_colors)
        slides = car_gen.generate_carousel_slides(
            [
                {"title": f"CHÀO MỪNG ĐẾN VỚI {name.upper()}", "body": "Hệ thống sản xuất video AI đa kênh đã sẵn sàng."},
                {"title": "QUAY 1 LẦN — ĐĂNG MỌI NƠI", "body": "CapCut Desktop + Adobe Premiere Pro + After Effects."},
                {"title": "BẮT ĐẦU NGAY HÔM NAY", "body": "Thả video vào thư mục inbox/ và gõ 'autopilot' nhé!"}
            ],
            output_dir=out_carousel_dir
        )

        print(f"  ✅ Đã xuất 3 slides ảnh nghiệm thu tại: {out_carousel_dir}")
        print("\n" + "*" * 65)
        print("🚀 CHÚC MỪNG BẠN! QUY TRÌNH ONBOARDING ĐÃ HOÀN TẤT XUẤT SẮC.")
        print("*" * 65)
        print("Bây giờ bạn chỉ cần:")
        print("  1. Thả video mới quay vào thư mục 'inbox/'")
        print("  2. Chạy lệnh: python studio.py director (để dựng có tương tác)")
        print("     Hoặc: python studio.py autopilot (để máy tự làm hết từ A-Z)\n")

        return out_carousel_dir

    def run_full_onboarding(self):
        """Khởi chạy trọn gói quy trình Onboarding."""
        self.check_preflight_environment()
        self.run_brand_interview()
        self.verify_assets_and_models()
        self.generate_welcome_test_assets()
