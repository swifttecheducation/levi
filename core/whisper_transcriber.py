#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/whisper_transcriber.py — Bộ nhận diện giọng nói và căn chỉnh nhịp chữ (Whisper Word-Level Timestamps).
Hỗ trợ nạp file phụ đề có sẵn (JSON/SRT), hoặc chạy Whisper/WhisperX trực tiếp.
Đảm bảo chuẩn hoá dấu tiếng Việt và ngắt cụm từ 2-4 từ/nhịp hiển thị.
"""

import os
import json
import re
import subprocess
from typing import List, Dict, Any, Optional


class TranscriberUnavailable(RuntimeError):
    """Không có engine Whisper nào được cài (faster-whisper hoặc openai-whisper)."""


class WhisperTranscriber:
    def __init__(self, model_name: str = "large-v3", device: str = "auto"):
        self.model_name = model_name
        self.device = device

    # ------------------------------------------------------------------
    # Phân tích âm thanh THẬT (không giả lập)
    # ------------------------------------------------------------------
    def transcribe(self, video_path: str, language: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Bóc tách giọng nói bằng Whisper thật (ưu tiên faster-whisper, sau đó openai-whisper).
        Trả về các cụm 2-4 từ có mốc thời gian theo từ. Ném TranscriberUnavailable nếu chưa cài engine nào.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Không tìm thấy video: {video_path}")

        words: List[Dict[str, Any]] = []
        try:
            from faster_whisper import WhisperModel  # type: ignore
            model = WhisperModel(self.model_name, device=self.device, compute_type="auto")
            segments, _info = model.transcribe(
                video_path, language=language, word_timestamps=True, vad_filter=True
            )
            for seg in segments:
                for w in (seg.words or []):
                    words.append({"word": w.word, "start": w.start, "end": w.end})
        except ImportError:
            try:
                import whisper  # type: ignore
            except ImportError:
                raise TranscriberUnavailable(
                    "Chưa cài engine Whisper. Chạy: pip install faster-whisper  (hoặc: pip install openai-whisper)"
                )
            model = whisper.load_model(
                self.model_name, device=None if self.device == "auto" else self.device
            )
            result = model.transcribe(video_path, language=language, word_timestamps=True)
            for seg in result.get("segments", []):
                for w in seg.get("words", []):
                    words.append({"word": w["word"], "start": w["start"], "end": w["end"]})

        return self._normalize_segments(self._chunk_words(words))

    @staticmethod
    def get_media_duration(video_path: str) -> float:
        """Tổng thời lượng (giây) bằng ffprobe. Trả về 0.0 nếu không đọc được."""
        try:
            out = subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", video_path],
                text=True, stderr=subprocess.DEVNULL, timeout=60
            ).strip()
            return float(out)
        except Exception:
            return 0.0

    def detect_speech_segments(
        self,
        video_path: str,
        noise_db: float = -30.0,
        min_silence: float = 0.35,
        min_segment: float = 0.30
    ) -> List[Dict[str, Any]]:
        """
        Tìm các đoạn CÓ TIẾNG bằng FFmpeg silencedetect trên âm thanh thật của video.
        Các đoạn trả về chưa có chữ (text rỗng). Rỗng nếu không phát hiện được khoảng lặng nào có nghĩa.
        """
        total = self.get_media_duration(video_path)
        if total <= 0.0:
            return []

        try:
            res = subprocess.run(
                ["ffmpeg", "-hide_banner", "-i", video_path,
                 "-af", f"silencedetect=noise={noise_db}dB:d={min_silence}", "-f", "null", "-"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=max(120, int(total * 2))
            )
        except Exception:
            return []

        silences: List[Dict[str, float]] = []
        for line in res.stderr.splitlines():
            m = re.search(r"silence_start:\s*(-?[0-9.]+)", line)
            if m:
                silences.append({"start": max(0.0, float(m.group(1)))})
                continue
            m = re.search(r"silence_end:\s*([0-9.]+)", line)
            if m and silences and "end" not in silences[-1]:
                silences[-1]["end"] = float(m.group(1))

        segments: List[Dict[str, Any]] = []
        cursor = 0.0
        for s in silences:
            if s["start"] - cursor >= min_segment:
                segments.append({"start": round(cursor, 3), "end": round(s["start"], 3), "text": ""})
            cursor = s.get("end", total)
        if total - cursor >= min_segment:
            segments.append({"start": round(cursor, 3), "end": round(total, 3), "text": ""})
        return segments

    def load_or_transcribe(
        self,
        video_path: str,
        transcript_json_path: Optional[str] = None,
        allow_mock: bool = False,
        mock_text: str = "",
        mock_duration: float = 15.0,
        language: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lấy dữ liệu giọng nói theo thứ tự ưu tiên:
          1. File transcript JSON do người dùng cung cấp.
          2. Whisper thật.
          3. Phát hiện khoảng lặng thật trên âm thanh (không có chữ -> không có phụ đề).
          4. Chỉ khi allow_mock=True mới dùng transcript giả (để demo/test).

        Trả về: {"segments": dùng để cắt, "subtitles": chỉ các cụm có chữ, "mode": json|whisper|silence|mock}
        """
        if transcript_json_path:
            if not os.path.exists(transcript_json_path):
                raise FileNotFoundError(f"Không tìm thấy file transcript: {transcript_json_path}")
            subs = self.load_transcript_json(transcript_json_path)
            return {"segments": subs, "subtitles": subs, "mode": "json"}

        try:
            subs = self.transcribe(video_path, language=language)
            if subs:
                return {"segments": subs, "subtitles": subs, "mode": "whisper"}
            print("       ⚠️ Whisper không nhận ra lời nói nào, chuyển sang cắt theo khoảng lặng.")
        except TranscriberUnavailable as e:
            print(f"       ⚠️ {e}")
            print("       ⚠️ Tạm cắt theo khoảng lặng thật; sẽ KHÔNG có phụ đề cho đến khi có Whisper hoặc --subtitles.")

        segs = self.detect_speech_segments(video_path)
        if segs:
            return {"segments": segs, "subtitles": [], "mode": "silence"}

        total = self.get_media_duration(video_path)
        if total > 0.0:
            # Không có khoảng lặng nào đáng cắt: giữ nguyên cả video.
            return {"segments": [{"start": 0.0, "end": round(total, 3), "text": ""}],
                    "subtitles": [], "mode": "silence"}

        if allow_mock:
            subs = self.create_mock_transcript_from_text(mock_text, total_duration=mock_duration)
            return {"segments": subs, "subtitles": subs, "mode": "mock"}

        raise RuntimeError(
            f"Không đọc được thời lượng/âm thanh của '{video_path}' (cần cài ffmpeg & ffprobe). "
            "Truyền --allow-mock nếu chỉ muốn chạy thử với dữ liệu giả."
        )

    def load_transcript_json(self, json_path: str) -> List[Dict[str, Any]]:
        """Nạp file transcript JSON (chuẩn Whisper hoặc Descript)."""
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Không tìm thấy file transcript: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        segments = []
        if isinstance(data, list):
            segments = data
        elif isinstance(data, dict):
            if "segments" in data:
                segments = data["segments"]
            elif "words" in data:
                segments = self._chunk_words(data["words"])
            elif "text" in data and "chunks" in data:
                segments = data["chunks"]

        return self._normalize_segments(segments)

    def _chunk_words(self, words: List[Dict[str, Any]], max_words: int = 4) -> List[Dict[str, Any]]:
        """Gom các từ đơn lẻ thành từng cụm 2-4 từ dễ đọc trên màn hình dọc 9:16."""
        chunks = []
        cur_words = []
        start_t = None

        for w in words:
            word_str = w.get("word", "").strip()
            if not word_str:
                continue

            if start_t is None:
                start_t = w.get("start", 0.0)

            cur_words.append(word_str)
            end_t = w.get("end", start_t + 0.3)

            # Ngắt cụm khi đủ số từ hoặc gặp dấu câu
            has_punct = bool(re.search(r"[,.?!;:]$", word_str))
            if len(cur_words) >= max_words or has_punct:
                chunks.append({
                    "start": round(start_t, 2),
                    "end": round(end_t, 2),
                    "text": " ".join(cur_words)
                })
                cur_words = []
                start_t = None

        if cur_words and start_t is not None:
            chunks.append({
                "start": round(start_t, 2),
                "end": round(end_t, 2),
                "text": " ".join(cur_words)
            })

        return chunks

    def _normalize_segments(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Làm sạch ký tự thừa và chuẩn hóa thời gian."""
        cleaned = []
        for s in segments:
            text = s.get("text", "").strip()
            if not text:
                continue
            start = float(s.get("start", 0.0))
            end = float(s.get("end", start + 0.5))
            cleaned.append({
                "start": round(start, 3),
                "end": round(end, 3),
                "text": text,
                "duration": round(end - start, 3)
            })
        return cleaned

    def create_mock_transcript_from_text(self, text: str, total_duration: float) -> List[Dict[str, Any]]:
        """Tạo transcript giả lập có chia nhịp đều từ chuỗi văn bản nếu chưa có audio phân tích."""
        words = text.split()
        if not words:
            return []
        
        chunks = []
        chunk_size = 4
        sub_lists = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        dt = total_duration / max(1, len(sub_lists))
        
        for idx, sub in enumerate(sub_lists):
            chunks.append({
                "start": round(idx * dt, 2),
                "end": round(min(total_duration, (idx + 1) * dt), 2),
                "text": " ".join(sub),
                "duration": round(dt, 2)
            })
        return chunks
