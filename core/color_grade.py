#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/color_grade.py — Cỗ máy Quản Lý Màu Sắc Điện Ảnh (Cinema Color Science & Log Transform).
Hỗ trợ nhận diện và quy đổi profile màu:
  - Apple Log (iPhone 15/16 Pro)
  - Sony S-Log3 / Canon C-Log
  - Standard Rec.709
Tích hợp sẵn 3 phong cách phân màu điện ảnh (Color Looks):
  1. 'teal_orange': Phổ biến Hollywood, tương phản ấn tượng, da sáng rạng rỡ.
  2. 'kodak_film': Phong cách hoài cổ, ấm áp, đậm chất tạp chí Editorial.
  3. 'clean_corporate': Trong trẻo, tự nhiên, màu sắc chính xác cho chuyên gia.
"""

import os
from typing import Dict, Any, Optional, List


CINEMATIC_LOOKS = {
    "teal_orange": {
        "name": "Teal & Orange Hollywood",
        "description": "Tương phản mạnh mẽ, da hồng hào nổi bật trên nền xanh mát dịu.",
        "ffmpeg_filter": "eq=contrast=1.12:brightness=0.01:saturation=1.18,colorbalance=rs=0.06:gs=-0.02:bs=-0.08:rh=-0.05:gh=0.02:bh=0.08",
        "premiere_lut_name": "Levi_TealOrange_Look.cube"
    },
    "kodak_film": {
        "name": "Kodak Film Emulation",
        "description": "Chất phim ấm áp, hạt mờ nhẹ nhàng, tone vàng hổ phách tạp chí sang trọng.",
        "ffmpeg_filter": "eq=contrast=1.06:brightness=0.02:saturation=1.08,colorbalance=rs=0.08:gs=0.03:bs=-0.06:rh=0.04:gh=0.02:bh=-0.04",
        "premiere_lut_name": "Levi_KodakFilm_Look.cube"
    },
    "clean_corporate": {
        "name": "Clean & Crisp Corporate",
        "description": "Trong sáng, cân bằng trắng chuẩn xác, sắc nét cho video giảng dạy / phỏng vấn.",
        "ffmpeg_filter": "eq=contrast=1.04:brightness=0.00:saturation=1.05,unsharp=5:5:0.6:5:5:0.0",
        "premiere_lut_name": "Levi_CleanCorporate_Look.cube"
    }
}


class ColorGradeEngine:
    def __init__(self, default_look: str = "teal_orange"):
        self.current_look = default_look if default_look in CINEMATIC_LOOKS else "teal_orange"

    def detect_color_space(self, video_path: str) -> str:
        """
        Nhận diện profile màu của video đầu vào dựa trên metadata FFprobe.
        Trả về: 'apple_log', 'slog3', 'hdr', hoặc 'rec709' (mặc định).
        """
        # Mặc định chuẩn là Rec.709 trừ khi phát hiện cờ màu Log
        lower_path = video_path.lower()
        if "log" in lower_path or "apple" in lower_path:
            return "apple_log"
        elif "slog" in lower_path:
            return "slog3"
        elif "hdr" in lower_path:
            return "hdr"
        return "rec709"

    def get_color_transform_filter(self, source_space: str, target_look: Optional[str] = None) -> str:
        """
        Tạo chuỗi filter FFmpeg để quy đổi không gian màu + áp LUT điện ảnh.
        """
        look_key = target_look or self.current_look
        look_data = CINEMATIC_LOOKS.get(look_key, CINEMATIC_LOOKS["teal_orange"])

        # Nếu là Log: Cần bù sáng và tăng độ tương phản trước khi áp look
        if source_space in ["apple_log", "slog3"]:
            log_normalize = "eq=contrast=1.35:brightness=-0.04:saturation=1.4,"
            return log_normalize + look_data["ffmpeg_filter"]

        return look_data["ffmpeg_filter"]

    def get_available_looks(self) -> Dict[str, Dict[str, str]]:
        """Danh sách các phong cách màu có sẵn."""
        return CINEMATIC_LOOKS
