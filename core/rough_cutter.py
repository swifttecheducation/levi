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

        # 1. Nới mép (lead-in / lead-out) rồi gộp các đoạn chồng lấn để không bị lặp hình/tiếng ở chỗ nối.
        padded: List[Dict[str, Any]] = []
        for seg in sorted(speech_segments, key=lambda s: s["start"]):
            start = max(0.0, seg["start"] - lead_in)
            end = seg["end"] + lead_out
            text = seg.get("text", "")
            if padded and start <= padded[-1]["end"]:
                padded[-1]["end"] = max(padded[-1]["end"], end)
                if text:
                    padded[-1]["text"] = f"{padded[-1]['text']} {text}".strip()
            else:
                padded.append({"start": start, "end": end, "text": text})

        # 2. Sinh danh sách cut.
        cuts = []
        for idx, seg in enumerate(padded):
            duration = seg["end"] - seg["start"]

            # Xen kẽ micro zoom: Cứ mỗi đoạn cắt mới đổi cỡ cảnh (1.0 vs 1.08)
            scale = self.punch_in_scale if (idx % 2 == 1) else 1.0

            cuts.append({
                "clip_index": idx,
                "source_in": round(seg["start"], 3),
                "source_out": round(seg["end"], 3),
                "duration": round(duration, 3),
                "scale": scale,
                "text": seg["text"]
            })

        return cuts

    def get_timeline_duration(self, cuts: List[Dict[str, Any]]) -> float:
        """Tổng thời lượng của video sau khi đã cắt sạch khoảng lặng."""
        return round(sum(c["duration"] for c in cuts), 3)

    @staticmethod
    def clamp_cuts(cuts: List[Dict[str, Any]], max_duration: float) -> List[Dict[str, Any]]:
        """
        Kẹp các mốc cắt vào độ dài thật của video (mép lead-out có thể vượt quá cuối file).
        Cut nào còn lại dưới 1 frame sau khi kẹp thì bị bỏ. Không sửa danh sách gốc.
        """
        if not max_duration or max_duration <= 0:
            return [dict(c) for c in cuts]

        out = []
        for c in cuts:
            new = dict(c)
            for key in ("source_out", "video_out", "audio_out"):
                if key in new:
                    new[key] = round(min(new[key], max_duration), 3)
            s_in = new.get("source_in", new.get("video_in", 0.0))
            s_out = new.get("source_out", new.get("video_out", s_in + new.get("duration", 0.0)))
            if s_out - s_in < 1.0 / 30.0:
                continue
            new["duration"] = round(s_out - s_in, 3)
            out.append(new)
        for idx, c in enumerate(out):
            c["clip_index"] = idx
        return out

    @staticmethod
    def remap_to_timeline(
        items: List[Dict[str, Any]],
        cuts: List[Dict[str, Any]],
        min_duration: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Đổi mốc thời gian của phụ đề (tính theo video GỐC) sang mốc thời gian của TIMELINE SAU KHI CẮT.

        Nếu không đổi, phụ đề sẽ lệch dần vì các khoảng lặng đã bị cắt bỏ. Mốc rơi vào đoạn đã bị cắt
        được kéo về đầu cut kế tiếp. Trả về bản sao, không sửa danh sách gốc; các khóa khác được giữ nguyên.
        """
        if not cuts:
            return [dict(i) for i in items]

        # (đầu nguồn, cuối nguồn, thời điểm bắt đầu trên timeline)
        spans = []
        cursor = 0.0
        for c in cuts:
            # Bám theo mốc của HÌNH (source_in/out), vì `duration` của cut và track video ở CapCut/Premiere
            # đều tính theo hình; với J-Cut thì audio_in lệch so với hình nên không dùng để dựng timeline.
            c_in = c.get("source_in", c.get("video_in", 0.0))
            c_out = c.get("source_out", c.get("video_out", c_in + c.get("duration", 0.0)))
            spans.append((c_in, c_out, cursor))
            cursor += max(0.0, c_out - c_in)
        total = cursor

        def map_time(t: float) -> float:
            for c_in, c_out, tl_start in spans:
                if t < c_in:
                    return tl_start            # rơi vào đoạn đã bị cắt -> dính vào đầu cut kế tiếp
                if t <= c_out:
                    return tl_start + (t - c_in)
            return total                       # sau cut cuối cùng

        remapped = []
        for item in items:
            # Phụ đề nằm hoàn toàn trong đoạn đã bị cắt thì bỏ, tránh nháy chữ 0.05s vô nghĩa.
            if not any(c_in < item["end"] and item["start"] < c_out for c_in, c_out, _ in spans):
                continue
            new = dict(item)
            start = map_time(item["start"])
            end = map_time(item["end"])
            if end - start < min_duration:
                end = min(total, start + min_duration)
                if end - start < min_duration:   # nằm sát cuối timeline
                    start = max(0.0, end - min_duration)
            new["start"] = round(start, 3)
            new["end"] = round(end, 3)
            new["duration"] = round(new["end"] - new["start"], 3)
            remapped.append(new)
        return remapped
