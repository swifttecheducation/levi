#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/rough_cutter.py — Tự động cắt gọt khoảng lặng (Dead-Air Trimmer) và tính toán Micro-Zoom.
Loại bỏ các đoạn im lặng > 0.3s, tự động áp dụng hiệu ứng phóng to nhảy cảnh (Punch-In Zoom 1.0 -> 1.08)
tại các điểm nối câu để giữ nhịp độ và năng lượng của video dọc 9:16.
"""

from typing import List, Dict, Any, Tuple


class RoughCutter:
    def __init__(
        self,
        min_silence_duration: float = 0.35,  # Đoạn im lặng trên 0.35s sẽ bị cắt
        silence_threshold_db: float = -32.0,
        punch_in_scale: float = 1.08        # Zoom 8% tại các nhịp nhấn
    ):
        self.min_silence_duration = min_silence_duration
        self.silence_threshold_db = silence_threshold_db
        self.punch_in_scale = punch_in_scale

    def compute_cuts_from_speech_segments(
        self,
        speech_segments: List[Dict[str, Any]],
        lead_in: float = 0.05,
        lead_out: float = 0.08
    ) -> List[Dict[str, Any]]:
        """
        Nhận danh sách phân đoạn nói từ Whisper và tính toán các khoảng giữ lại (Kept Clips).
        Tự động nối nhẹ mép đầu (lead-in) và mép cuối (lead-out) để âm thanh tự nhiên không bị cụt hơi.
        """
        if not speech_segments:
            return []

        cuts = []
        for idx, seg in enumerate(speech_segments):
            start = max(0.0, seg["start"] - lead_in)
            end = seg["end"] + lead_out
            duration = end - start

            # Xen kẽ micro zoom: Cứ mỗi đoạn cắt mới đổi cỡ cảnh (1.0 vs 1.08)
            scale = self.punch_in_scale if (idx % 2 == 1) else 1.0

            cuts.append({
                "clip_index": idx,
                "source_in": round(start, 3),
                "source_out": round(end, 3),
                "duration": round(duration, 3),
                "scale": scale,
                "text": seg.get("text", "")
            })

        return cuts

    def get_timeline_duration(self, cuts: List[Dict[str, Any]]) -> float:
        """Tổng thời lượng của video sau khi đã cắt sạch khoảng lặng."""
        return round(sum(c["duration"] for c in cuts), 3)
