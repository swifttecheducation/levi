#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
workflows/viral_creator.py — Cỗ Máy Tạo Video Viral Triệu View (Viral Reels Generator).
Thiết kế trọn bộ:
  1. Hook mở đầu giật gân (3s đầu): "CẦU TOÀN MÀ DÙNG AI - ĐỪNG ĐỂ BỊ ĐỐT TOKEN!"
  2. Phụ đề động (Dynamic Captions): Đồng bộ chính xác theo từng câu nói tiếng Việt của tác giả.
  3. Khóa cằm AI Chin-Lock: Neo phụ đề an toàn né mặt ở vùng Y = 1310px.
  4. Call To Action (CTA): "COMMENT [STUDIO]" ở cuối video.
  5. Đồng bộ dự án đa lớp vào CapCut Desktop (D:\CapCut Drafts\Levi_Project).
  6. Render video MP4 hoàn chỉnh có phụ đề động vào outbox/video_hoan_thien/.
"""

import os
import sys
import json
import time
import uuid
import shutil
import subprocess

VIRAL_SUBTITLES = [
    {"start": 0.5, "end": 3.8, "text": "Nếu bạn là người CẦU TOÀN..."},
    {"start": 3.8, "end": 7.2, "text": "...mà lại thích edit video bằng AI"},
    {"start": 7.2, "end": 10.5, "text": "thì phải xem ngay video này!"},
    {"start": 10.5, "end": 14.2, "text": "nếu không muốn TỐN TIỀN TOKEN liên tục!"},
    {"start": 14.2, "end": 18.0, "text": "Người cầu toàn có tật: lệch 1 PIXEL thôi cũng ngứa mắt!"},
    {"start": 18.0, "end": 22.5, "text": "Sai một chữ phụ đề hay đổi phông là lại gõ prompt bắt AI sửa"},
    {"start": 22.5, "end": 27.5, "text": "Mỗi lần bạn gõ sửa: AI lại ĐỐT CẢ ĐỐNG TOKEN để render lại!"},
    {"start": 27.5, "end": 33.0, "text": "Sửa xong video khéo TIỀN TOKEN đắt ngang tiền thuê thợ dựng!"},
    {"start": 33.0, "end": 38.5, "text": "Nhưng hệ thống XƯỞNG DỰNG RẢNH TAY thì khác nha!"},
    {"start": 38.5, "end": 44.0, "text": "AI làm đúng 80% việc nặng: tự cắt khoảng lặng, bắt nhịp..."},
    {"start": 44.0, "end": 50.5, "text": "Còn 20% tiểu tiết: MỞ THẲNG DRAFT CAPCUT CHO BẠN!"},
    {"start": 50.5, "end": 56.5, "text": "Tự tay kéo di, sửa chính tả, đổi màu phông trong ĐÚNG 5 GIÂY!"},
    {"start": 56.5, "end": 62.0, "text": "KHÔNG TỐN THÊM 1 GIỌT TOKEN NÀO NỮA!"},
    {"start": 62.0, "end": 68.0, "text": "Sau mỗi lần sửa, AI tự học lại để về sau không cần sửa nữa."},
    {"start": 68.0, "end": 73.0, "text": "Dùng AI là để RẢNH TAY chứ không phải đi nuôi Token!"},
    {"start": 73.0, "end": 79.0, "text": "Quay 1 lần: ra Reels + Bộ ảnh Carousel + 3 Story đi kèm!"},
    {"start": 79.0, "end": 84.0, "text": "👉 COMMENT [STUDIO] ĐỂ NHẬN QUY TRÌNH RẢNH TAY NÀY NHÉ!"}
]

def generate_srt_subtitles(subs, srt_path):
    """Tạo file SRT phụ đề chuẩn."""
    def fmt_time(t_sec):
        hrs = int(t_sec // 3600)
        mins = int((t_sec % 3600) // 60)
        secs = int(t_sec % 60)
        msecs = int((t_sec - int(t_sec)) * 1000)
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{msecs:03d}"

    lines = []
    for idx, s in enumerate(subs, 1):
        lines.append(str(idx))
        lines.append(f"{fmt_time(s['start'])} --> {fmt_time(s['end'])}")
        lines.append(s["text"])
        lines.append("")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ Đã tạo file SRT: {srt_path}")


def build_viral_capcut_draft(target_dir: str = r"D:\CapCut Drafts\Levi_Project"):
    """Cập nhật dự án CapCut với đầy đủ các track Hook, Eyebrow, Subtitles, CTA."""
    os.makedirs(target_dir, exist_ok=True)
    draft_content_path = os.path.join(target_dir, "draft_content.json")
    meta_path = os.path.join(target_dir, "draft_meta_info.json")

    # Đọc draft_content hiện tại hoặc tạo mới
    if os.path.exists(draft_content_path):
        with open(draft_content_path, "r", encoding="utf-8") as f:
            content = json.load(f)
    else:
        content = {"tracks": [], "materials": {"texts": [], "videos": [], "speeds": []}}

    # Đảm bảo materials
    if "materials" not in content:
        content["materials"] = {}
    if "texts" not in content["materials"]:
        content["materials"]["texts"] = []

    # Xóa các track text cũ để nạp track viral mới
    content["tracks"] = [t for t in content.get("tracks", []) if t.get("type") != "text"]

    # 1. Track Hook Headline (0 -> 4.5s)
    hook_id = str(uuid.uuid4()).upper()
    content["materials"]["texts"].append({
        "id": hook_id,
        "type": "text",
        "content": json.dumps({
            "text": "CẦU TOÀN MÀ DÙNG AI\nĐỪNG ĐỂ BỊ ĐỐT TOKEN!",
            "styles": [
                {"range": [0, 18], "size": 18.0, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [0.95, 0.93, 0.89], "alpha": 1.0}}}},
                {"range": [19, 40], "size": 16.0, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [1.0, 0.85, 0.2], "alpha": 1.0}}}}
            ]
        }, ensure_ascii=False)
    })

    hook_track = {
        "id": str(uuid.uuid4()).upper(),
        "type": "text",
        "segments": [{
            "id": str(uuid.uuid4()).upper(),
            "material_id": hook_id,
            "target_timerange": {"start": 0, "duration": 4500000},
            "source_timerange": {"start": 0, "duration": 4500000},
            "clip": {"transform": {"y": 0.62, "x": 0.0, "scale": {"x": 1.0, "y": 1.0}}}
        }]
    }

    # 2. Track Eyebrow (0 -> 4.5s)
    eyebrow_id = str(uuid.uuid4()).upper()
    content["materials"]["texts"].append({
        "id": eyebrow_id,
        "type": "text",
        "content": json.dumps({
            "text": "🚨 CẢNH BÁO TIỀN TOKEN",
            "styles": [{"range": [0, 22], "size": 10.0, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [0.8, 0.1, 0.1], "alpha": 1.0}}}}]
        }, ensure_ascii=False)
    })

    eyebrow_track = {
        "id": str(uuid.uuid4()).upper(),
        "type": "text",
        "segments": [{
            "id": str(uuid.uuid4()).upper(),
            "material_id": eyebrow_id,
            "target_timerange": {"start": 0, "duration": 4500000},
            "source_timerange": {"start": 0, "duration": 4500000},
            "clip": {"transform": {"y": 0.74, "x": 0.0, "scale": {"x": 1.0, "y": 1.0}}}
        }]
    }

    # 3. Track Subtitles theo từng câu (khóa cằm Chin-Lock Y ~ -0.38)
    sub_segments = []
    for s in VIRAL_SUBTITLES:
        mat_id = str(uuid.uuid4()).upper()
        # Highlight từ khoá quan trọng bằng màu vàng
        content["materials"]["texts"].append({
            "id": mat_id,
            "type": "text",
            "content": json.dumps({
                "text": s["text"],
                "styles": [{"range": [0, len(s["text"])], "size": 11.5, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [1.0, 1.0, 1.0], "alpha": 1.0}}}}]
            }, ensure_ascii=False)
        })

        st_us = int(s["start"] * 1000000)
        dur_us = int((s["end"] - s["start"]) * 1000000)
        sub_segments.append({
            "id": str(uuid.uuid4()).upper(),
            "material_id": mat_id,
            "target_timerange": {"start": st_us, "duration": dur_us},
            "source_timerange": {"start": 0, "duration": dur_us},
            "clip": {"transform": {"y": -0.38, "x": 0.0, "scale": {"x": 1.0, "y": 1.0}}}
        })

    sub_track = {
        "id": str(uuid.uuid4()).upper(),
        "type": "text",
        "segments": sub_segments
    }

    # 4. Track Call to Action cuối video
    cta_id = str(uuid.uuid4()).upper()
    content["materials"]["texts"].append({
        "id": cta_id,
        "type": "text",
        "content": json.dumps({
            "text": "COMMENT [STUDIO]\nNHẬN QUY TRÌNH RẢNH TAY",
            "styles": [
                {"range": [0, 16], "size": 19.0, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [1.0, 0.85, 0.1], "alpha": 1.0}}}},
                {"range": [17, 40], "size": 13.0, "bold": True, "fill": {"alpha": 1.0, "content": {"solid": {"color": [1.0, 1.0, 1.0], "alpha": 1.0}}}}
            ]
        }, ensure_ascii=False)
    })

    cta_track = {
        "id": str(uuid.uuid4()).upper(),
        "type": "text",
        "segments": [{
            "id": str(uuid.uuid4()).upper(),
            "material_id": cta_id,
            "target_timerange": {"start": 78000000, "duration": 6500000},
            "source_timerange": {"start": 0, "duration": 6500000},
            "clip": {"transform": {"y": 0.15, "x": 0.0, "scale": {"x": 1.0, "y": 1.0}}}
        }]
    }

    content["tracks"].extend([hook_track, eyebrow_track, sub_track, cta_track])

    with open(draft_content_path, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    # Cập nhật meta
    now_us = int(time.time() * 1000000)
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        meta["tm_draft_modified"] = now_us + 200000
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f)

    root_meta_path = r"C:\Users\Admin\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\root_meta_info.json"
    if os.path.exists(root_meta_path):
        with open(root_meta_path, "r", encoding="utf-8") as f:
            root_m = json.load(f)
        for d in root_m.get("all_draft_store", []):
            if d.get("draft_name") == "Levi_Project":
                d["tm_draft_modified"] = now_us + 200000
                break
        with open(root_meta_path, "w", encoding="utf-8") as f:
            json.dump(root_m, f, indent=2)

    print("🎉 Đã cập nhật trọn bộ Layer Viral vào CapCut Desktop thành công!")


def render_viral_video_with_captions(
    input_video: str,
    output_video: str,
    srt_path: str
):
    """Render file video MP4 hoàn chỉnh có sẵn Subtitle chữ nổi tiếng Việt."""
    font_file = r"assets\fonts\BeVietnamPro-Bold.ttf".replace("\\", "/")
    srt_clean = srt_path.replace("\\", "/").replace(":", "\\:")

    # Chuẩn bị subtitle filter với styling hiện đại: nền bo nhẹ hoặc viền đen dày
    sub_filter = (
        f"subtitles='{srt_clean}':force_style='"
        f"Fontname=Be Vietnam Pro,Fontsize=18,PrimaryColour=&H00FFFFFF&,OutlineColour=&H00000000&,"
        f"BorderStyle=1,Outline=3,Shadow=1,MarginV=120,Alignment=2'"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-vf", sub_filter,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
        "-pix_fmt", "yuv420p",
        "-c:a", "copy",
        "-movflags", "+faststart",
        output_video
    ]

    print(f"🎬 Đang render video MP4 hoàn thiện có phụ đề: {output_video}...")
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode == 0:
        print(f"🎉 Render video viral thành công: {output_video}")
        return True
    else:
        print(f"❌ Lỗi render: {res.stderr[-300:]}")
        return False


if __name__ == "__main__":
    srt_out = r"outbox\viral_subtitles.srt"
    generate_srt_subtitles(VIRAL_SUBTITLES, srt_out)
    build_viral_capcut_draft(r"D:\CapCut Drafts\Levi_Project")
    render_viral_video_with_captions(
        input_video=r"outbox\video_hoan_thien\Levi_SourceGoc_Final.mp4",
        output_video=r"outbox\video_hoan_thien\Levi_Video_Viral_TrieuView.mp4",
        srt_path=srt_out
    )
