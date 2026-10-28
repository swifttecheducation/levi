#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
workflows/trial_reels.py — Tạo 3 bản dựng Video Thử Nghiệm (Instagram Trial Reels A/B Testing).
Từ 1 video gốc, tự động biến tấu 3 phiên bản khác nhau:
  - Bản A: Hook Trực diện (Direct / High Urgency), nhịp cắt nhanh, âm thanh punchy.
  - Bản B: Hook Đặt câu hỏi (Question / Curiosity), nhịp kể chuyện điềm tĩnh, zoom nhẹ.
  - Bản C: Hook Ngược dòng (Contrarian / Hot Take), phong cách Editorial tối giản.
Giúp kiểm tra thuật toán Instagram mà không bị đánh gậy video trùng lặp (re-up).
"""

from typing import List, Dict, Any


class TrialReelsGenerator:
    def __init__(self):
        pass

    def generate_three_variants(
        self,
        base_headline: str,
        base_cuts: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Sinh cấu hình 3 biến thể A/B/C."""
        # Biến thể A: Trực diện, giật tít, phóng to ngay từ frame đầu
        var_a = {
            "variant_id": "A",
            "name": "High_Urgency_Punch",
            "hook_headline": f"ĐỪNG BỎ LỠ: {base_headline.upper()}",
            "eyebrow": "CẢNH BÁO QUAN TRỌNG",
            "initial_scale": 1.12,
            "music_energy": "high",
            "cuts": base_cuts
        }

        # Biến thể B: Tò mò, đặt câu hỏi
        var_b = {
            "variant_id": "B",
            "name": "Curiosity_Question",
            "hook_headline": f"Bạn Đã Biết Bí Mật Này Chưa? {base_headline}",
            "eyebrow": "GÓC NHÌN MỚI",
            "initial_scale": 1.0,
            "music_energy": "medium_calm",
            "cuts": base_cuts
        }

        # Biến thể C: Ngược dòng, phản biện
        var_c = {
            "variant_id": "C",
            "name": "Contrarian_Editorial",
            "hook_headline": f"Hầu hết mọi người đang hiểu sai về: {base_headline}",
            "eyebrow": "SỰ THẬT ĐẰNG SAU",
            "initial_scale": 1.05,
            "music_energy": "minimal_lofi",
            "cuts": base_cuts
        }

        return [var_a, var_b, var_c]
