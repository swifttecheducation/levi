#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/semantic_sound_visual.py — Thiết Kế Âm Thanh & Hình Ảnh Ngữ Nghĩa (Semantic Audio & Visual Matching).
Tự động phân tích câu từ trong bài nói để chèn hiệu ứng âm thanh (Foley SFX) và cảnh quay B-Roll ẩn dụ:
  - Tài chính / Tiền bạc: 'tiền', 'doanh thu', 'lợi nhuận', 'giá' -> SFX ka-ching / cash register
  - Ý tưởng / Đột phá: 'bí quyết', 'nhận ra', 'ý tưởng', 'chiến lược' -> SFX ding bell / lightbulb spark
  - Chuyển hướng / Nhấn mạnh: 'nhưng', 'tuy nhiên', 'thực ra', 'chú ý' -> SFX deep whoosh / sub hit
  - Công nghệ / Thực thi: 'lập trình', 'code', 'click', 'hệ thống' -> SFX mechanical click
"""

from typing import List, Dict, Any, Optional


SEMANTIC_SFX_RULES = [
    {
        "category": "finance",
        "keywords": ["tiền", "doanh thu", "lợi nhuận", "chi phí", "nghìn đô", "triệu view", "bán hàng"],
        "sfx_name": "sfx_cash_register.wav",
        "broll_tag": "finance_growth"
    },
    {
        "category": "insight",
        "keywords": ["bí mật", "nhận ra", "ý tưởng", "chiến lược", "bước ngoặt", "khám phá"],
        "sfx_name": "sfx_idea_spark.wav",
        "broll_tag": "creative_light"
    },
    {
        "category": "contrast",
        "keywords": ["nhưng thực ra", "tuy nhiên", "ngược lại", "sai lầm", "cảnh báo"],
        "sfx_name": "sfx_deep_whoosh.wav",
        "broll_tag": "glitch_impact"
    },
    {
        "category": "action",
        "keywords": ["bấm vào", "hệ thống", "công cụ", "tải về", "bắt đầu ngay"],
        "sfx_name": "sfx_mouse_click.wav",
        "broll_tag": "workspace_tech"
    }
]


class SemanticSoundVisual:
    def __init__(self, rules: Optional[List[Dict[str, Any]]] = None):
        self.rules = rules or SEMANTIC_SFX_RULES

    def analyze_transcript_cues(
        self,
        subtitles: List[Dict[str, Any]],
        max_sfx_per_minute: int = 4
    ) -> List[Dict[str, Any]]:
        """
        Quét danh sách phụ đề và sinh các điểm chèn âm thanh SFX và B-Roll phù hợp.
        Giới hạn số lượng SFX để video không bị quá tải âm thanh (bảo đảm tính tinh tế, chuyên nghiệp).
        """
        cues = []
        last_sfx_time = -999.0
        min_gap_sec = 60.0 / max_sfx_per_minute

        for sub in subtitles:
            text = sub.get("text", "").lower()
            start_t = sub.get("start", 0.0)

            # Nếu thời gian cách quá gần SFX trước đó thì bỏ qua
            if start_t - last_sfx_time < min_gap_sec:
                continue

            for rule in self.rules:
                matched_kw = next((kw for kw in rule["keywords"] if kw in text), None)
                if matched_kw:
                    cues.append({
                        "timestamp": round(start_t, 2),
                        "matched_keyword": matched_kw,
                        "category": rule["category"],
                        "sfx_file": rule["sfx_name"],
                        "broll_tag": rule["broll_tag"],
                        "text_snippet": sub.get("text", "")
                    })
                    last_sfx_time = start_t
                    break

        return cues
