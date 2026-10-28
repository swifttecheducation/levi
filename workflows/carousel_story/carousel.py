#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflows/carousel_story/carousel.py — Bộ sinh nội dung Carousel (1080x1350) và Story (9:16).
Tạo bộ slide vuốt ngang Instagram Carousel chuẩn tỉ lệ 4:5 và chuỗi Story tương tác dọc 9:16.
Chừa sẵn vị trí dán Sticker thăm dò (Poll), câu hỏi (AMA), và từ khóa ManyChat.
"""

import os
from typing import List, Dict, Any, Optional
from PIL import Image, ImageDraw, ImageFont


class CarouselStoryGenerator:
    def __init__(
        self,
        brand_colors: Optional[Dict[str, str]] = None,
        brand_fonts: Optional[Dict[str, str]] = None
    ):
        self.colors = brand_colors or {
            "primary": "#F2EDE4",
            "secondary": "#212C1B",
            "accent": "#FFADBF",
            "highlight": "#720000"
        }

    def generate_carousel_slides(
        self,
        slides_data: List[Dict[str, str]],
        output_dir: str = "outbox/carousel"
    ) -> List[str]:
        """Tạo chuỗi ảnh 1080x1350 (4:5) cho bài đăng vuốt ngang Instagram."""
        os.makedirs(output_dir, exist_ok=True)
        width, height = 1080, 1350
        saved_paths = []

        for idx, slide in enumerate(slides_data):
            img = Image.new("RGB", (width, height), color=self.colors.get("secondary", "#212C1B"))
            draw = ImageDraw.Draw(img)

            title = slide.get("title", f"Slide {idx + 1}")
            body = slide.get("body", "")

            # Header / Page Number
            draw.text((80, 80), f"{idx + 1} / {len(slides_data)}", fill=self.colors.get("accent", "#FFADBF"))

            # Title
            draw.text((80, 240), title, fill=self.colors.get("primary", "#F2EDE4"))

            # Body text
            draw.text((80, 420), body, fill=self.colors.get("primary", "#F2EDE4"))

            # Swipe Indicator
            if idx < len(slides_data) - 1:
                draw.text((width - 240, height - 100), "VUỐT TIẾP 👉", fill=self.colors.get("accent", "#FFADBF"))
            else:
                draw.text((width - 320, height - 100), "COMMENT ĐỂ NHẬN QUÀ 🎁", fill=self.colors.get("accent", "#FFADBF"))

            slide_path = os.path.join(output_dir, f"slide_{idx + 1:02d}.jpg")
            img.save(slide_path, quality=95)
            saved_paths.append(slide_path)

        return saved_paths

    def generate_story_slide(
        self,
        headline: str,
        sticker_type: str = "poll",  # 'poll', 'question', 'link'
        output_path: str = "outbox/story.jpg"
    ) -> str:
        """Tạo 1 frame Story 9:16 (1080x1920) chừa vùng an toàn cho Instagram Sticker."""
        width, height = 1080, 1920
        img = Image.new("RGB", (width, height), color=self.colors.get("secondary", "#212C1B"))
        draw = ImageDraw.Draw(img)

        # Tiêu đề trên Story
        draw.text((100, 320), headline, fill=self.colors.get("primary", "#F2EDE4"))

        # Vùng chừa cho Instagram Sticker (Khung đứt nét)
        sticker_box = [160, 900, width - 160, 1250]
        draw.rectangle(sticker_box, outline=self.colors.get("accent", "#FFADBF"), width=3)
        draw.text((200, 1050), f"[ VÙNG DÁN STICKER INSTAGRAM ({sticker_type.upper()}) ]", fill=self.colors.get("accent", "#FFADBF"))

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        img.save(output_path, quality=95)
        return output_path
