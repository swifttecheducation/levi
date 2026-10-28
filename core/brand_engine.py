#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/brand_engine.py — Parser và quản lý Bộ Nhận Diện Thương Hiệu Toàn Diện (Brand Kit Engine).
Phân tích 7 trụ cột từ brand-kit.md:
  1. Định vị thương hiệu & Kênh mạng xã hội
  2. Giọng điệu (Voice & Tone) & Gut Check cảm xúc
  3. Quy tắc câu từ cấm kỵ (Hard Rules)
  4. Câu từ đặc trưng (Voice DNA: Mở bài, Kết bài)
  5. Phong cách thị giác, Font chữ Việt hóa & Bảng màu
  6. Sản phẩm chính & Kịch bản chuyển đổi ManyChat
  7. Bảng sửa lỗi phiên âm giọng nói (Phonetic Auto-Corrections)
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple


DEFAULT_BRAND_KIT = {
    "name": "Levi Studio",
    "target_audience": "Nhà sáng tạo nội dung, Marketer và Chuyên gia số",
    "voice_tone": "Điềm tĩnh, sâu sắc, thực chiến và truyền cảm hứng",
    "gut_check": "Người xem cảm thấy được khai sáng, nhận được giá trị thực tế áp dụng được ngay.",
    "hard_rules": [
        "Không giật tít rẻ tiền",
        "Không cam kết 100%",
        "Không nói quá",
        "Không tạo áp lực FOMO tiêu cực"
    ],
    "voice_dna": {
        "intro_hook": "Nhiều người nghĩ..., nhưng thực ra...",
        "outro_cta": "Cùng kiên trì mỗi ngày nhé. Follow để giỏi lên cùng mình!"
    },
    "style_pack": "Editorial Luxe",
    "style_codes": ["H1", "C1", "L1", "X5", "M1", "G1"],
    "fonts": {
        "headline": "Playfair Display",
        "caption": "Be Vietnam Pro",
        "accent": "Caveat"
    },
    "colors": {
        "primary": "#F2EDE4",      # Kem Yến Mạch
        "secondary": "#212C1B",    # Xanh Thông Đậm
        "accent": "#FFADBF",       # Hồng Phấn
        "highlight": "#720000"     # Đỏ Rượu
    },
    "offers": {
        "main_product": "Khóa Học Dựng Phim AI Triệu View",
        "freebie": "Bản Đồ Kịch Bản Video 1 Triệu View"
    },
    "manychat_keywords": ["LEVI", "STUDIO", "VIP", "INBOX"],
    "phonetic_corrections": {
        "lê vi": "Levi",
        "s u per": "Super",
        "r e e l s": "Reels"
    },
    "audio": {
        "target_lufs": -14.0,       # -14 LUFS cho Reels/TikTok, -16 cho YouTube
        "true_peak": -1.5,
        "bgm_volume_db": -18.0
    }
}


class BrandEngine:
    def __init__(self, brand_kit_path: Optional[str] = None):
        self.brand_kit_path = brand_kit_path
        self.brand = DEFAULT_BRAND_KIT.copy()
        if brand_kit_path and os.path.exists(brand_kit_path):
            self.load_from_markdown(brand_kit_path)

    def load_from_markdown(self, path: str) -> Dict[str, Any]:
        """Phân tích nội dung file brand-kit.md toàn diện."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # 1. Định vị
            name_m = re.search(r"-\s+\*\*Bạn và thương hiệu của bạn:\*\*\s*(.+)", content)
            if name_m and "{{" not in name_m.group(1):
                self.brand["name"] = name_m.group(1).strip()

            target_m = re.search(r"-\s+\*\*Bạn giúp ai[^*]*:\*\*\s*(.+)", content)
            if target_m and "{{" not in target_m.group(1):
                self.brand["target_audience"] = target_m.group(1).strip()

            # 2. Giọng điệu
            tone_m = re.search(r"-\s+\*\*Mô tả giọng điệu:\*\*\s*(.+)", content)
            if tone_m and "{{" not in tone_m.group(1):
                self.brand["voice_tone"] = tone_m.group(1).strip()

            gut_m = re.search(r"-\s+\*\*Gut check[^*]*:\*\*\s*(.+)", content)
            if gut_m and "{{" not in gut_m.group(1):
                self.brand["gut_check"] = gut_m.group(1).strip()

            # 3. Hard Rules
            rules_section = re.search(r"## 3\. Các quy tắc[^\n]*\n([\s\S]*?)(?=## 4|$)", content)
            if rules_section:
                rules = re.findall(r"-\s+([^\n]+)", rules_section.group(1))
                if rules:
                    self.brand["hard_rules"] = [r.strip() for r in rules if "{{" not in r]

            # 4. Voice DNA
            intro_m = re.search(r"-\s+\*\*Cấu trúc câu mở đầu[^*]*:\*\*\s*(.+)", content)
            if intro_m and "{{" not in intro_m.group(1):
                self.brand["voice_dna"]["intro_hook"] = intro_m.group(1).strip()

            outro_m = re.search(r"-\s+\*\*Câu chào hoặc lời kết[^*]*:\*\*\s*(.+)", content)
            if outro_m and "{{" not in outro_m.group(1):
                self.brand["voice_dna"]["outro_cta"] = outro_m.group(1).strip()

            # 5. Fonts & Style
            style_m = re.search(r"-\s+\*\*Bộ phong cách đang sử dụng:\*\*\s*(.+)", content)
            if style_m and "{{" not in style_m.group(1):
                self.brand["style_pack"] = style_m.group(1).strip()

            style_codes_m = re.search(r"-\s+\*\*Mã phong cách dựng video[^*]*:\*\*\s*(.+)", content)
            if style_codes_m and "{{" not in style_codes_m.group(1):
                self.brand["style_codes"] = [c.strip().upper() for c in style_codes_m.group(1).split(",") if c.strip()]

            head_font_m = re.search(r"-\s+\*\*Font tiêu đề chính[^*]*:\*\*\s*(.+)", content)
            if head_font_m and "{{" not in head_font_m.group(1):
                self.brand["fonts"]["headline"] = head_font_m.group(1).strip()

            cap_font_m = re.search(r"-\s+\*\*Font phụ đề[^*]*:\*\*\s*(.+)", content)
            if cap_font_m and "{{" not in cap_font_m.group(1):
                self.brand["fonts"]["caption"] = cap_font_m.group(1).strip()

            accent_font_m = re.search(r"-\s+\*\*Font tạo điểm nhấn[^*]*:\*\*\s*(.+)", content)
            if accent_font_m and "{{" not in accent_font_m.group(1):
                self.brand["fonts"]["accent"] = accent_font_m.group(1).strip()

            colors_found = re.findall(r"#[0-9a-fA-F]{6}", content)
            if len(colors_found) >= 2:
                self.brand["colors"]["primary"] = colors_found[0]
                self.brand["colors"]["secondary"] = colors_found[1]
            if len(colors_found) >= 3:
                self.brand["colors"]["accent"] = colors_found[2]
            if len(colors_found) >= 4:
                self.brand["colors"]["highlight"] = colors_found[3]

            # 6. Offers & ManyChat
            product_m = re.search(r"-\s+\*\*Sản phẩm chính:\*\*\s*(.+)", content)
            if product_m and "{{" not in product_m.group(1):
                self.brand["offers"]["main_product"] = product_m.group(1).strip()

            freebie_m = re.search(r"-\s+\*\*Quà tặng miễn phí[^*]*:\*\*\s*(.+)", content)
            if freebie_m and "{{" not in freebie_m.group(1):
                self.brand["offers"]["freebie"] = freebie_m.group(1).strip()

            mc_m = re.search(r"-\s+\*\*Từ khóa kích hoạt chatbot[^*]*:\*\*\s*(.+)", content)
            if mc_m and "{{" not in mc_m.group(1):
                self.brand["manychat_keywords"] = [k.strip().upper() for k in mc_m.group(1).split(",") if k.strip()]

            # 7. Sửa lỗi phiên âm Whisper
            corr_section = re.search(r"## 7\. Bảng sửa lỗi phiên âm[^\n]*\n([\s\S]*?)(?=## 8|$)", content)
            if corr_section:
                pairs = re.findall(r"-\s+([^->\n]+)\s*->\s*([^\n]+)", corr_section.group(1))
                if pairs:
                    for wrong, right in pairs:
                        self.brand["phonetic_corrections"][wrong.strip().lower()] = right.strip()

        except Exception as e:
            print(f"[BrandEngine] Warning: Không thể đọc hoàn chỉnh {path}: {e}")

        return self.brand

    def get_style_codes(self) -> List[str]:
        return self.brand.get("style_codes", ["H1", "C1", "L1", "X5", "M1", "G1"])

    def get_fonts(self) -> Dict[str, str]:
        return self.brand["fonts"]

    def get_colors(self) -> Dict[str, str]:
        return self.brand["colors"]

    def get_audio_standards(self) -> Dict[str, float]:
        return self.brand["audio"]

    def get_manychat_keywords(self) -> List[str]:
        return self.brand.get("manychat_keywords", [])

    def get_hard_rules(self) -> List[str]:
        return self.brand.get("hard_rules", [])

    def get_voice_dna(self) -> Dict[str, str]:
        return self.brand.get("voice_dna", {})

    def get_offers(self) -> Dict[str, str]:
        return self.brand.get("offers", {})

    def get_phonetic_corrections(self) -> Dict[str, str]:
        return self.brand.get("phonetic_corrections", {})

    def apply_phonetic_corrections(self, text: str) -> str:
        """Tự động thay thế các từ Whisper nghe nhầm thành từ đúng chuẩn thương hiệu."""
        corrected = text
        for wrong, right in self.get_phonetic_corrections().items():
            pattern = re.compile(re.escape(wrong), re.IGNORECASE)
            corrected = pattern.sub(right, corrected)
        return corrected
