#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/brand_engine.py — Parser và quản lý Bộ Nhận Diện Thương Hiệu (Brand Kit).
Đọc trực tiếp từ brand-kit.md, cung cấp bảng màu, font chữ tiếng Việt,
giọng điệu (Voice & Tone) và các từ khóa kích hoạt Chatbot ManyChat.
"""

import os
import re
from typing import Dict, Any, List, Optional


DEFAULT_BRAND_KIT = {
    "name": "Levi Studio",
    "target_audience": "Nhà sáng tạo nội dung, Marketer và Chuyên gia số",
    "voice_tone": "Điềm tĩnh, sâu sắc, thực chiến và truyền cảm hứng",
    "style_pack": "Editorial Luxe",
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
    "audio": {
        "target_lufs": -14.0,       # -14 LUFS cho Reels/TikTok, -16 cho YouTube
        "true_peak": -1.5,
        "bgm_volume_db": -18.0
    },
    "manychat_keywords": ["LEVI", "STUDIO", "VIP", "INBOX"]
}


class BrandEngine:
    def __init__(self, brand_kit_path: Optional[str] = None):
        self.brand_kit_path = brand_kit_path
        self.brand = DEFAULT_BRAND_KIT.copy()
        if brand_kit_path and os.path.exists(brand_kit_path):
            self.load_from_markdown(brand_kit_path)

    def load_from_markdown(self, path: str) -> Dict[str, Any]:
        """Phân tích nội dung file brand-kit.md."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            # Phân tích các trường chính bằng Regex
            name_m = re.search(r"-\s+\*\*Bạn và thương hiệu của bạn:\*\*\s*(.+)", content)
            if name_m and "{{" not in name_m.group(1):
                self.brand["name"] = name_m.group(1).strip()

            style_m = re.search(r"-\s+\*\*Bộ phong cách đang sử dụng:\*\*\s*(.+)", content)
            if style_m and "{{" not in style_m.group(1):
                self.brand["style_pack"] = style_m.group(1).strip()

            head_font_m = re.search(r"-\s+\*\*Font tiêu đề chính[^*]*:\*\*\s*(.+)", content)
            if head_font_m and "{{" not in head_font_m.group(1):
                self.brand["fonts"]["headline"] = head_font_m.group(1).strip()

            cap_font_m = re.search(r"-\s+\*\*Font phụ đề[^*]*:\*\*\s*(.+)", content)
            if cap_font_m and "{{" not in cap_font_m.group(1):
                self.brand["fonts"]["caption"] = cap_font_m.group(1).strip()

            accent_font_m = re.search(r"-\s+\*\*Font tạo điểm nhấn[^*]*:\*\*\s*(.+)", content)
            if accent_font_m and "{{" not in accent_font_m.group(1):
                self.brand["fonts"]["accent"] = accent_font_m.group(1).strip()

            # Colors
            colors_found = re.findall(r"#[0-9a-fA-F]{6}", content)
            if len(colors_found) >= 2:
                self.brand["colors"]["primary"] = colors_found[0]
                self.brand["colors"]["secondary"] = colors_found[1]
            if len(colors_found) >= 3:
                self.brand["colors"]["accent"] = colors_found[2]
            if len(colors_found) >= 4:
                self.brand["colors"]["highlight"] = colors_found[3]

        except Exception as e:
            print(f"[BrandEngine] Warning: Không thể đọc hoàn chỉnh {path}: {e}")

        return self.brand

    def get_fonts(self) -> Dict[str, str]:
        return self.brand["fonts"]

    def get_colors(self) -> Dict[str, str]:
        return self.brand["colors"]

    def get_audio_standards(self) -> Dict[str, float]:
        return self.brand["audio"]

    def get_manychat_keywords(self) -> List[str]:
        return self.brand.get("manychat_keywords", [])
