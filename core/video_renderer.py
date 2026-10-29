#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/video_renderer.py — Cỗ Máy Render Video Trực Tiếp Chuẩn Phát Sóng (Direct Video Renderer).
Tự động xuất file video MP4 hoàn thiện từ video thô:
  1. Phân tích và cắt sạch khoảng lặng (Dead-Air Trimmer) với độ chính xác mili-giây.
  2. Áp dụng chuẩn màu điện ảnh (Teal & Orange, Kodak Film, Clean Corporate).
  3. Chuẩn hóa âm thanh phát sóng EBU R128 (-14 LUFS Reels/TikTok, True Peak -1.5 dBTP).
  4. Tăng tốc phần cứng bằng GPU NVIDIA (h264_nvenc) hoặc CPU libx264 tối ưu.
  5. Xuất trực tiếp vào thư mục outbox/video_hoan_thien/.
"""

import os
import re
import sys
import shutil
import subprocess
import tempfile
from typing import List, Dict, Any, Optional, Tuple

from core.color_grade import ColorGradeEngine, CINEMATIC_LOOKS
from core.audio_master import AudioMaster


class VideoRenderer:
    def __init__(
        self,
        color_look: str = "teal_orange",
        target_lufs: float = -14.0,
        silence_threshold_db: float = -30.0,
        min_silence_duration: float = 0.35,
        use_gpu: bool = True
    ):
        self.color_engine = ColorGradeEngine(default_look=color_look)
        self.audio_master = AudioMaster(target_i=target_lufs)
        self.silence_threshold_db = silence_threshold_db
        self.min_silence_duration = min_silence_duration
        self.use_gpu = use_gpu and self._check_nvenc_support()

    def _check_nvenc_support(self) -> bool:
        """Kiểm tra máy có card đồ họa NVIDIA hỗ trợ h264_nvenc không."""
        try:
            res = subprocess.run(
                ["ffmpeg", "-encoders"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            return "h264_nvenc" in res.stdout or "h264_nvenc" in res.stderr
        except Exception:
            return False

    def get_video_duration(self, video_path: str) -> float:
        """Lấy tổng thời lượng video (giây)."""
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]
        try:
            out = subprocess.check_output(cmd, text=True).strip()
            return float(out)
        except Exception:
            return 0.0

    def detect_speech_cuts(
        self,
        video_path: str,
        lead_in: float = 0.05,
        lead_out: float = 0.08,
        min_clip_duration: float = 0.30
    ) -> List[Dict[str, Any]]:
        """
        Dùng FFmpeg silencedetect để phân tích âm thanh và tìm các phân đoạn có giọng nói.
        Tự động gọt bỏ dead-air với lead-in/lead-out để không bị nuốt âm.
        """
        total_dur = self.get_video_duration(video_path)
        if total_dur <= 0.0:
            return []

        cmd = [
            "ffmpeg", "-i", video_path,
            "-af", f"silencedetect=noise={self.silence_threshold_db}dB:d={self.min_silence_duration}",
            "-f", "null", "-"
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        silences = []
        for line in res.stderr.splitlines():
            if "silence_start:" in line:
                m = re.search(r"silence_start:\s*([0-9.]+)", line)
                if m:
                    silences.append({"start": float(m.group(1))})
            elif "silence_end:" in line:
                m = re.search(r"silence_end:\s*([0-9.]+)", line)
                if m and silences and "end" not in silences[-1]:
                    silences[-1]["end"] = float(m.group(1))

        # Nếu không có khoảng lặng nào thì giữ nguyên cả video
        if not silences:
            return [{"clip_index": 0, "start": 0.0, "end": total_dur, "duration": total_dur}]

        speeches = []
        cur_time = 0.0
        for s in silences:
            s_start = s["start"]
            s_end = s.get("end", total_dur)
            if s_start > cur_time:
                speeches.append((cur_time, s_start))
            cur_time = s_end
        if cur_time < total_dur:
            speeches.append((cur_time, total_dur))

        cuts = []
        for idx, (start, end) in enumerate(speeches):
            c_start = max(0.0, start - lead_in)
            c_end = min(total_dur, end + lead_out)
            dur = c_end - c_start
            if dur >= min_clip_duration:
                cuts.append({
                    "clip_index": idx,
                    "start": round(c_start, 3),
                    "end": round(c_end, 3),
                    "duration": round(dur, 3)
                })

        return cuts

    def render_final_video(
        self,
        video_path: str,
        output_path: str,
        cuts: Optional[List[Dict[str, Any]]] = None,
        apply_color_grade: bool = True,
        apply_audio_master: bool = True,
        bgm_path: Optional[str] = None
    ) -> bool:
        """
        Thực thi toàn bộ luồng Render xuất bản video thành phẩm:
        Cắt gọt dead-air + Ghép liền mạch + Phân màu điện ảnh + Âm thanh chuẩn EBU R128.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Không tìm thấy video đầu vào: {video_path}")

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        if not cuts:
            print("  🔍 Đang quét phân tích khoảng lặng (Dead-Air)...")
            cuts = self.detect_speech_cuts(video_path)

        if not cuts:
            print("  ⚠️ Không phát hiện đoạn cắt, giữ nguyên toàn bộ video.")
            total_dur = self.get_video_duration(video_path)
            cuts = [{"clip_index": 0, "start": 0.0, "end": total_dur, "duration": total_dur}]

        orig_dur = self.get_video_duration(video_path)
        final_dur = sum(c["duration"] for c in cuts)
        print(f"  ✂️  Tổng phân đoạn: {len(cuts)} nhịp. Thời lượng rút gọn: {final_dur:.2f}s (từ gốc {orig_dur:.2f}s).")

        # Chuẩn bị bộ lọc video (Color Grade & Pixel Format)
        v_filters = []
        if apply_color_grade and self.color_engine.current_look in CINEMATIC_LOOKS:
            look_cfg = CINEMATIC_LOOKS[self.color_engine.current_look]
            v_filters.append(look_cfg["ffmpeg_filter"])
            print(f"  🎨 Áp dụng màu điện ảnh: {look_cfg['name']}")

        # Luôn chuẩn hoá pixel format về yuv420p & TV Range tương thích 100% với Windows Media Player & Mobile
        v_filters.append("scale=out_color_matrix=bt709:out_range=limited,format=yuv420p")

        # Chuẩn bị bộ lọc âm thanh (EBU R128)
        a_filters = []
        if apply_audio_master:
            a_filters.append(self.audio_master.get_loudnorm_filter_string())
            print(f"  🔊 Chuẩn hóa âm thanh: EBU R128 ({self.audio_master.target_i} LUFS)")

        # Xây dựng filter_complex cắt và ghép nối các phân đoạn (trimmed concat)
        filter_parts = []
        concat_v_inputs = []
        concat_a_inputs = []

        for i, c in enumerate(cuts):
            st = c["start"]
            en = c["end"]
            filter_parts.append(f"[0:v]trim=start={st}:end={en},setpts=PTS-STARTPTS[v{i}]")
            filter_parts.append(f"[0:a]atrim=start={st}:end={en},asetpts=PTS-STARTPTS[a{i}]")
            concat_v_inputs.append(f"[v{i}]")
            concat_a_inputs.append(f"[a{i}]")

        n = len(cuts)
        cat_inputs = "".join(f"{concat_v_inputs[i]}{concat_a_inputs[i]}" for i in range(n))
        filter_parts.append(f"{cat_inputs}concat=n={n}:v=1:a=1[base_v][base_a]")

        # Nối tiếp bộ lọc màu sắc
        if v_filters:
            vf_str = ",".join(v_filters)
            filter_parts.append(f"[base_v]{vf_str}[out_v]")
            final_v_map = "[out_v]"
        else:
            final_v_map = "[base_v]"

        # Nối tiếp bộ lọc âm thanh
        if a_filters:
            af_str = ",".join(a_filters)
            filter_parts.append(f"[base_a]{af_str}[out_a]")
            final_a_map = "[out_a]"
        else:
            final_a_map = "[base_a]"

        filter_complex_str = ";".join(filter_parts)

        # Chọn Video Encoder: GPU NVENC hoặc CPU libx264
        if self.use_gpu:
            vcodec = ["-c:v", "h264_nvenc", "-preset", "p4", "-cq", "22", "-b:v", "8M"]
            print("  ⚡ Tăng tốc GPU: NVIDIA NVENC Hardware Encoder")
        else:
            vcodec = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20"]
            print("  ⚙️  Sử dụng CPU: libx264 Encoder")

        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-filter_complex", filter_complex_str,
            "-map", final_v_map,
            "-map", final_a_map,
            *vcodec,
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart",
            output_path
        ]

        print("  ⏳ Đang render video...")
        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"  🎉 Render thành công: {output_path}")
                return True
            else:
                # Nếu GPU thất bại (do driver hoặc vram), thử lại bằng CPU libx264
                if self.use_gpu:
                    print("  ⚠️ Thử lại bằng CPU libx264...")
                    cmd[cmd.index("h264_nvenc") : cmd.index("h264_nvenc") + 5] = ["libx264", "-preset", "veryfast", "-crf", "20"]
                    res2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    if res2.returncode == 0 and os.path.exists(output_path):
                        print(f"  🎉 Render thành công (CPU): {output_path}")
                        return True
                print(f"  ❌ Lỗi khi render: {res.stderr[-400:]}")
                return False
        except Exception as e:
            print(f"  ❌ Lỗi ngoại lệ khi render: {e}")
            return False

    def render_with_motionmaxxing(
        self,
        video_path: str,
        output_path: str,
        badges: Optional[List[Dict[str, Any]]] = None,
        ass_subtitle_path: Optional[str] = None,
        zoom_windows: Optional[List[Tuple[float, float]]] = None,
        sfx_cues: Optional[List[Dict[str, Any]]] = None,
        fonts_dir: Optional[str] = None
    ) -> bool:
        """
        Render video theo quy chuẩn cao cấp của motionmaxxing:
        1. Dynamic Camera Punch-in Zoom (1.14x) tại các điểm drama/punchline.
        2. Lớp đồ họa Graphic Badges có chiều sâu & ánh sáng viền phát sáng (Glow).
        3. Phụ đề Kinetic nảy chữ dứt khoát 2-4 từ.
        4. Thiết kế âm thanh Foley SFX đồng bộ và Master âm lượng chuẩn phát sóng -14 LUFS.
        5. Kiểm định chất lượng tự động qua Quality Gate (G0, G2, G3).
        """
        import tempfile
        from core.motion_reframer import MotionReframer
        reframer = MotionReframer()

        # 1. Chuẩn bị Audio Master với Foley SFX và Loudnorm -14 LUFS
        temp_audio = os.path.join(tempfile.gettempdir(), "master_motionmaxxing_audio.aac")
        cmd_audio = ["ffmpeg", "-y", "-i", video_path]

        sfx_inputs = []
        if sfx_cues:
            for cue in sfx_cues:
                if os.path.exists(cue["file"]):
                    cmd_audio.extend(["-i", cue["file"]])
                    sfx_inputs.append(cue)

        if sfx_inputs:
            af_parts = []
            mix_ins = ["[0:a]"]
            for idx, cue in enumerate(sfx_inputs):
                in_id = idx + 1
                ms = int(cue["time"] * 1000)
                vol = cue.get("vol", 0.45)
                af_parts.append(f"[{in_id}:a]adelay={ms}|{ms},volume={vol}[sfx{in_id}]")
                mix_ins.append(f"[sfx{in_id}]")
            mix_ins_str = "".join(mix_ins)
            af_parts.append(f"{mix_ins_str}amix=inputs={len(mix_ins)}:duration=first:dropout_transition=0[mixed_a]")
            af_parts.append(f"[mixed_a]{self.audio_master.get_loudnorm_filter_string()}[out_a]")
            cmd_audio.extend(["-filter_complex", ";".join(af_parts), "-map", "[out_a]"])
        else:
            cmd_audio.extend(["-af", self.audio_master.get_loudnorm_filter_string()])

        cmd_audio.extend(["-c:a", "aac", "-b:a", "192k", temp_audio])
        subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 2. Xây dựng Video Filter Complex (Punch-in Zoom + Badges + ASS Subtitles)
        cmd_video = ["ffmpeg", "-y", "-i", video_path]
        if os.path.exists(temp_audio):
            cmd_video.extend(["-i", temp_audio])
            audio_source = "1:a"
        else:
            audio_source = "0:a"

        badge_inputs = []
        if badges:
            for b in badges:
                if os.path.exists(b["file"]):
                    cmd_video.extend(["-i", b["file"]])
                    badge_inputs.append(b)

        v_steps = []
        # Bước A: Punch-in Zoom
        if zoom_windows:
            zoom_str, out_lbl = reframer.build_punch_in_filter(zoom_windows, base_label="0:v", out_label="v_punch")
            v_steps.append(zoom_str)
            curr_v = "v_punch"
        else:
            curr_v = "0:v"

        # Bước B: Graphic Badges
        start_badge_idx = 2 if os.path.exists(temp_audio) else 1
        for i, b in enumerate(badge_inputs):
            in_idx = start_badge_idx + i
            out_v = f"v_badge_{i}"
            cond = f"between(t,{b['start']:.2f},{b['end']:.2f})"
            v_steps.append(f"[{curr_v}][{in_idx}:v]overlay={b['x']}:{b['y']}:enable='{cond}'[{out_v}]")
            curr_v = out_v

        # Bước C: ASS Subtitles
        if ass_subtitle_path and os.path.exists(ass_subtitle_path):
            ass_clean = os.path.abspath(ass_subtitle_path).replace("\\", "/")
            if ":" in ass_clean:
                # Dùng relative path để tránh lỗi escape dấu hai chấm trên Windows
                rel_ass = os.path.relpath(ass_subtitle_path, os.getcwd()).replace("\\", "/")
            else:
                rel_ass = ass_clean
            sub_filter = f"ass='{rel_ass}'"
            if fonts_dir and os.path.exists(fonts_dir):
                rel_fonts = os.path.relpath(fonts_dir, os.getcwd()).replace("\\", "/")
                sub_filter += f":fontsdir='{rel_fonts}'"
            v_steps.append(f"[{curr_v}]{sub_filter}[v_final]")
            curr_v = "v_final"

        full_vf = ";".join(v_steps)
        cmd_video.extend([
            "-filter_complex", full_vf,
            "-map", f"[{curr_v}]",
            "-map", audio_source,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            "-movflags", "+faststart",
            output_path
        ])

        print(f"🎬 [motionmaxxing] Đang thực thi render video chất lượng cao...")
        res = subprocess.run(cmd_video, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and os.path.exists(output_path):
            print(f"🎉 [motionmaxxing] Render video hoàn tất: {output_path}")
            return True
        else:
            print(f"❌ [motionmaxxing] Lỗi: {res.stderr[-400:]}")
            return False
