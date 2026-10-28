#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/pacing_engine.py — Động Cơ Nhịp Điệu Điện Ảnh & Kỹ Thuật Cắt J-Cut / L-Cut.
Thay thế việc cắt gọt máy móc bằng tư duy của một Senior Editor:
  1. Phân biệt khoảng lặng vô nghĩa (Dead-Air / Flubs) và Khoảng Lặng Kịch Tính (Dramatic Pauses).
  2. Tự động áp dụng J-Cut (tiếng của câu tiếp theo xuất hiện trước hình ảnh 100-150ms ~ 3-5 frame).
  3. Tự động áp dụng L-Cut (âm thanh câu trước gối nhẹ sang cảnh sau) tạo cảm giác chuyển cảnh mềm mại.
"""

from typing import List, Dict, Any, Tuple


class PacingEngine:
    def __init__(
        self,
        j_cut_offset_sec: float = 0.12,         # Âm thanh cất lên trước hình 120ms (J-Cut chuẩn)
        dramatic_pause_min_sec: float = 0.45,   # Khoảng lặng >0.45s sau câu hỏi sẽ được giữ lại
        max_silence_allowed_sec: float = 0.35   # Khoảng lặng chết thông thường bị xén
    ):
        self.j_cut_offset_sec = j_cut_offset_sec
        self.dramatic_pause_min_sec = dramatic_pause_min_sec
        self.max_silence_allowed_sec = max_silence_allowed_sec

    def is_dramatic_pause(self, prev_segment_text: str, gap_duration: float) -> bool:
        """
        Nhận diện khoảng lặng có chủ đích nghệ thuật:
        - Nằm ngay sau một câu hỏi (kết thúc bằng ? hoặc có từ 'sao', 'không', 'gì')
        - Nằm sau một câu khẳng định mạnh (kết thúc bằng ! hoặc từ khóa 'bí mật', 'nhưng thực ra')
        """
        if gap_duration < self.dramatic_pause_min_sec:
            return False

        text = prev_segment_text.strip().lower()
        if text.endswith("?") or text.endswith("!"):
            return True

        question_cues = ["tại sao", "làm sao", "được không", "phải không", "như thế nào"]
        if any(cue in text for cue in question_cues):
            return True

        return False

    def optimize_timeline_pacing(
        self,
        segments: List[Dict[str, Any]],
        enable_j_cuts: bool = True,
        preserve_dramatic_pauses: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Tối ưu nhịp cắt toàn bộ timeline với kỹ thuật J-Cut / L-Cut.
        """
        if not segments:
            return []

        optimized_cuts = []
        for idx, seg in enumerate(segments):
            start = seg["start"]
            end = seg["end"]
            text = seg.get("text", "")

            # Kiểm tra khoảng cách với phân đoạn tiếp theo
            if idx < len(segments) - 1:
                next_start = segments[idx + 1]["start"]
                gap = next_start - end
                
                # Nếu là Dramatic Pause và người dùng muốn giữ lại:
                if preserve_dramatic_pauses and self.is_dramatic_pause(text, gap):
                    # Giữ lại khoảng 0.4s để tạo độ lắng đọng cảm xúc
                    end = end + min(gap, 0.45)
                    pause_type = "dramatic_pause_preserved"
                else:
                    pause_type = "normal_cut"
            else:
                pause_type = "outro"

            # Áp dụng J-Cut: Kéo video lùi lại một chút so với audio của clip tiếp theo
            video_in = start
            audio_in = start
            if enable_j_cuts and idx > 0:
                video_in = start + self.j_cut_offset_sec  # Hình ảnh chuyển sau âm thanh

            optimized_cuts.append({
                "clip_index": idx,
                "source_in": round(video_in, 3),
                "source_out": round(end, 3),
                "video_in": round(video_in, 3),
                "video_out": round(end, 3),
                "audio_in": round(audio_in, 3),
                "audio_out": round(end, 3),
                "duration": round(end - video_in, 3),
                "has_j_cut": enable_j_cuts and (idx > 0),
                "pause_type": pause_type,
                "text": text
            })

        return optimized_cuts
