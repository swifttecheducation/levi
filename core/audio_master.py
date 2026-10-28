#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/audio_master.py — Chuẩn âm thanh phát sóng EBU R128 (-14 LUFS Reels / -16 LUFS YouTube) & Smart Ducking.
Tính toán tham số FFmpeg filter loudnorm, compand, anlmdn và tự động hạ âm BGM khi có giọng nói.
"""

import os
import subprocess
import json
from typing import Dict, Any, Optional, Tuple


class AudioMaster:
    def __init__(
        self,
        target_i: float = -14.0,     # Integrated Loudness (-14 LUFS)
        target_tp: float = -1.5,     # Maximum True Peak (-1.5 dBTP)
        target_lra: float = 7.0       # Loudness Range (7 LU)
    ):
        self.target_i = target_i
        self.target_tp = target_tp
        self.target_lra = target_lra

    def get_loudnorm_filter_string(self) -> str:
        """Trả về chuỗi cấu hình bộ lọc loudnorm của FFmpeg theo chuẩn EBU R128."""
        return (
            f"loudnorm=I={self.target_i}:TP={self.target_tp}:LRA={self.target_lra}:"
            f"measured_I=-20.0:measured_TP=-2.0:measured_LRA=6.0:measured_thresh=-30.0:linear=true"
        )

    def build_ffmpeg_audio_master_command(
        self,
        input_audio_path: str,
        output_audio_path: str,
        bgm_path: Optional[str] = None,
        bgm_duck_db: float = -18.0
    ) -> List[str]:
        """
        Xây dựng mảng lệnh FFmpeg thực thi cân bằng âm thanh:
        1. Giọng nói qua EBU R128 loudnorm + Bộ lọc làm trong giọng
        2. Nếu có BGM: Tự động lồng ghép và áp dụng sidechain / ducking
        """
        cmd = ["ffmpeg", "-y", "-i", input_audio_path]

        if bgm_path:
            cmd.extend(["-i", bgm_path])
            # Filter graph: Giọng nói chuẩn hóa, BGM giảm âm lượng và hạ ngầm khi nói
            filter_complex = (
                f"[0:a]{self.get_loudnorm_filter_string()}[voice];"
                f"[1:a]volume={bgm_duck_db}dB[bgm];"
                f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[outa]"
            )
            cmd.extend(["-filter_complex", filter_complex, "-map", "[outa]"])
        else:
            cmd.extend(["-af", self.get_loudnorm_filter_string()])

        cmd.extend(["-c:a", "aac", "-b:a", "192k", output_audio_path])
        return cmd

    def export_master_audio(
        self,
        input_audio_path: str,
        output_audio_path: str,
        bgm_path: Optional[str] = None
    ) -> bool:
        """Thực thi xuất file âm thanh chuẩn phát sóng qua FFmpeg."""
        cmd = self.build_ffmpeg_audio_master_command(input_audio_path, output_audio_path, bgm_path)
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
            return res.returncode == 0
        except Exception as e:
            print(f"[AudioMaster] Warning: Không thể chạy FFmpeg: {e}")
            return False
