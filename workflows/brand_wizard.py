#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflows/brand_wizard.py — Trình Phỏng Vấn & Thiết Lập Nhận Diện Thương Hiệu Chuyên Sâu (Brand Kit Wizard).
Hỗ trợ 2 chế độ phỏng vấn:
  1. Quick Setup (2 phút): 4 câu hỏi cốt lõi để bắt đầu dựng ngay.
  2. Deep Brand Blueprint (5 phút): Toàn diện 7 trụ cột (Định vị, Voice DNA, Từ cấm kỵ,
     Bảng màu, Sản phẩm/Phễu quà tặng, Sửa lỗi phiên âm Whisper).
Tự động lưu và cập nhật trực tiếp vào file brand-kit.md.
"""

import os
import sys
from typing import Dict, Any, Optional, List

from core.brand_engine import BrandEngine


class BrandWizard:
    def __init__(self, brand_kit_path: Optional[str] = None):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.brand_kit_path = brand_kit_path or os.path.join(self.root_dir, "brand-kit.md")
        self.brand_engine = BrandEngine(self.brand_kit_path)

    def _ask(self, question: str, default: str = "") -> str:
        """Hỏi ý kiến tương tác tại console."""
        suffix = f" [{default}]" if default else ""
        try:
            val = input(f"👉 {question}{suffix}: ").strip()
            return val if val else default
        except (KeyboardInterrupt, EOFError):
            print("\nĐã hủy thao tác.")
            sys.exit(0)

    def run_deep_interview(self):
        """Phỏng vấn chuyên sâu đầy đủ 7 trụ cột thương hiệu."""
        print("\n" + "=" * 65)
        print("🏛️  LEVI SUPER STUDIO — THIẾT LẬP BỘ NHẬN DIỆN THƯƠNG HIỆU CHUYÊN SÂU")
        print("    (7 Trụ Cột ADN Thương Hiệu Cá Nhân & Doanh Nghiệp)")
        print("=" * 65)

        cur = self.brand_engine.brand

        # TRỤ CỘT 1: ĐỊNH VỊ & KÊNH
        print("\n📌 [TRỤ CỘT 1/7] ĐỊNH VỊ THƯƠNG HIỆU & KÊNH ĐĂNG TẢI")
        name = self._ask("Tên thương hiệu hoặc tên kênh của bạn là gì?", default=cur.get("name", "Levi Studio"))
        target = self._ask(
            "Bạn giúp đỡ ai, và giải pháp/giá trị bạn mang lại cho họ là gì?",
            default=cur.get("target_audience", "Nhà sáng tạo nội dung, Marketer và Chuyên gia số")
        )
        instagram = self._ask("Tài khoản Instagram của bạn", default=f"@{name.lower().replace(' ', '')}")
        tiktok = self._ask("Tài khoản TikTok của bạn", default=f"@{name.lower().replace(' ', '')}")

        # TRỤ CỘT 2: GIỌNG ĐIỆU (VOICE & TONE)
        print("\n📌 [TRỤ CỘT 2/7] GIỌNG ĐIỆU CỦA BẠN (VOICE & TONE)")
        voice_tone = self._ask(
            "Mô tả giọng điệu của bạn (ví dụ: điềm tĩnh, sâu sắc, thực chiến, truyền cảm hứng, hóm hỉnh...)",
            default=cur.get("voice_tone", "Điềm tĩnh, sâu sắc, thực chiến và truyền cảm hứng")
        )
        gut_check = self._ask(
            "Cảm xúc bạn muốn người xem cảm nhận sau khi xem video của bạn?",
            default="Người xem cảm thấy được khai sáng, nhận được giá trị thực tế áp dụng được ngay."
        )

        # TRỤ CỘT 3: QUY TẮC CÂU TỪ CẤM KỴ (HARD RULES)
        print("\n📌 [TRỤ CỘT 3/7] QUY TẮC CẤM KỴ BẤT BIẾN TRONG NỘI DUNG (HARD RULES)")
        hard_rules = self._ask(
            "Những từ ngữ hoặc cách diễn đạt cấm kỵ (ngăn cách bằng dấu phẩy)",
            default="Không giật tít rẻ tiền, Không cam kết 100%, Không nói quá, Không tạo áp lực FOMO tiêu cực"
        )
        rule_list = [r.strip() for r in hard_rules.split(",") if r.strip()]

        # TRỤ CỘT 4: CÂU TỪ ĐẶC TRƯNG (VOICE DNA)
        print("\n📌 [TRỤ CỘT 4/7] CÂU TỪ QUEN THUỘC ĐẶC TRƯNG CỦA BẠN (VOICE DNA)")
        intro_hook = self._ask(
            "Cấu trúc câu mở đầu quen thuộc của bạn",
            default="Nhiều người nghĩ..., nhưng thực ra..."
        )
        outro_cta = self._ask(
            "Câu chào hoặc lời kết đặc trưng của bạn",
            default="Cùng kiên trì mỗi ngày nhé. Follow để giỏi lên cùng mình!"
        )

        # TRỤ CỘT 5: THỊ GIÁC, FONT CHỮ & BẢNG MÀU
        print("\n📌 [TRỤ CỘT 5/7] PHONG CÁCH THỊ GIÁC, FONT CHỮ & BẢNG MÀU")
        print("  [1] Editorial Luxe (Tạp chí Sang trọng: Playfair Display + Caveat + Be Vietnam Pro)")
        print("  [2] Modern Minimal (Tối giản Hiện đại: Inter Black + Space Grotesk + Be Vietnam Pro)")
        print("  [3] Gen Z Pop (Năng động Phá cách: Poppins Black + Caveat + Be Vietnam Pro)")
        style_choice = self._ask("Chọn bộ phong cách [1/2/3]", default="1")

        if style_choice == "2":
            style_name = "Modern Minimal"
            head_font = "Inter"
            accent_font = "Space Grotesk"
            p_color, s_color = "#FFFFFF", "#121212"
        elif style_choice == "3":
            style_name = "Gen Z Pop"
            head_font = "Poppins"
            accent_font = "Caveat"
            p_color, s_color = "#FFE600", "#1E1E24"
        else:
            style_name = "Editorial Luxe"
            head_font = "Playfair Display"
            accent_font = "Caveat"
            p_color, s_color = "#F2EDE4", "#212C1B"

        # TRỤ CỘT 6: SẢN PHẨM & PHỄU QUÀ TẶNG (MANYCHAT AUTOMATION)
        print("\n📌 [TRỤ CỘT 6/7] SẢN PHẨM & PHỄU QUÀ TẶNG TỰ ĐỘNG (MANYCHAT)")
        product_name = self._ask("Sản phẩm, khóa học hoặc dịch vụ chính bạn cung cấp", default="Khóa Học Dựng Phim AI Triệu View")
        freebie = self._ask("Quà tặng miễn phí để hút khách hàng (Lead Magnet)", default="Bản Đồ Kịch Bản Video 1 Triệu View")
        manychat_keys = self._ask("Từ khóa kích hoạt chatbot ManyChat (ngăn cách bằng dấu phẩy)", default="LEVI, STUDIO, VIP")
        mc_list = [k.strip().upper() for k in manychat_keys.split(",") if k.strip()]

        # TRỤ CỘT 7: SỬA LỖI PHIÊN ÂM WHISPER (PHONETIC CORRECTIONS)
        print("\n📌 [TRỤ CỘT 7/7] SỬA LỖI PHIÊN ÂM GIỌNG NÓI ĐẶC THÙ (PHONETIC CORRECTIONS)")
        print("  Ghi theo định dạng: nghe_nhầm -> từ_đúng (ngăn cách bằng dấu phẩy)")
        corrections_input = self._ask(
            "Cặp từ Whisper hay nghe nhầm của bạn",
            default="lê vi -> Levi, s u per -> Super, r e e l s -> Reels"
        )
        corr_pairs = [c.strip() for c in corrections_input.split(",") if "->" in c]

        # Ghi trực tiếp vào brand-kit.md
        rules_md = "\n".join([f"- {r}" for r in rule_list])
        corr_md = "\n".join([f"- {c}" for c in corr_pairs])

        brand_content = f"""# 🏡 Brand Kit — Bộ Nhận Diện Thương Hiệu {name}

Tệp này là **Trụ Sở Thương Hiệu (Brand Homebase)** toàn diện của bạn: quy định định vị, giọng điệu, từ cấm kỵ, bảng màu chuẩn điện ảnh, font chữ Việt hóa 100% không lỗi ô vuông, kịch bản chuyển đổi ManyChat và bộ sửa lỗi phiên âm.

---

## 1. Định vị thương hiệu (Brand Identity)
- **Bạn và thương hiệu của bạn:** {name}
- **Bạn giúp ai, và giá trị họ nhận được là gì:** {target}
- **Nơi bạn đăng tải nội dung:**
  - Instagram: {instagram}
  - TikTok: {tiktok}

## 2. Giọng điệu thương hiệu (Voice & Tone)
- **Mô tả giọng điệu:** {voice_tone}
- **Gut check (Tiêu chuẩn cảm xúc):** {gut_check}

## 3. Các quy tắc câu từ cấm kỵ (Hard Rules)
> Danh sách những điều cấm kỵ mà AI không bao giờ được phép vi phạm khi viết tiêu đề hay kịch bản cho bạn:
{rules_md}

## 4. Những câu từ đặc trưng của bạn (Voice DNA)
- **Cấu trúc câu mở đầu quen thuộc:** {intro_hook}
- **Câu chào hoặc lời kết đặc trưng:** {outro_cta}

## 5. Phong cách thị giác & Font chữ (Visual & Typography)
- **Bộ phong cách đang sử dụng:** {style_name}
- **Font tiêu đề chính (Headline font):** {head_font}
- **Font phụ đề (Caption font):** Be Vietnam Pro
- **Font tạo điểm nhấn (Accent font):** {accent_font}
- **Bảng màu chủ đạo (Color Palette):**
  - Màu nền chính (Primary): `{p_color}`
  - Màu nền tương phản (Secondary): `{s_color}`
  - Màu nhấn (Accent): `#FFADBF`
  - Màu nổi bật (Highlight): `#720000`

## 6. Sản phẩm & Kịch bản gửi tin nhắn tự động (ManyChat Conversion)
- **Sản phẩm chính:** {product_name}
- **Quà tặng miễn phí (Freebie / Lead Magnet):** {freebie}
- **Từ khóa kích hoạt chatbot ManyChat:** {', '.join(mc_list)}

## 7. Bảng sửa lỗi phiên âm giọng nói (Phonetic Auto-Corrections)
> Hệ thống Whisper tự động tra cứu danh sách này để sửa đúng 100% tên riêng và thuật ngữ chuyên ngành:
{corr_md}

## 8. Chuẩn âm thanh phát sóng (Audio Standards)
- **Mức âm lượng tích hợp (Integrated Loudness):** `-14.0 LUFS` (Chuẩn EBU R128 tối ưu cho Reels/TikTok)
- **Mức đỉnh thực (True Peak):** `-1.5 dBTP`
- **Nhạc nền ngầm (BGM Bed):** `-18.0 dB`
"""
        with open(self.brand_kit_path, "w", encoding="utf-8") as f:
            f.write(brand_content)

        print("\n" + "*" * 65)
        print("🎉 CHÚC MỪNG! BỘ NHẬN DIỆN THƯƠNG HIỆU ĐÃ ĐƯỢC LƯU HOÀN THIỆN 100%.")
        print(f"📁 Tệp lưu trữ: {self.brand_kit_path}")
        print("*" * 65 + "\n")
