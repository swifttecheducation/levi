#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engines/capcut/draft_builder.py — Cỗ máy sinh dự án CapCut Desktop trực tiếp (Native Multi-Track).
Tạo folder dự án tại %LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft/
Bao gồm:
  - Video Track 1: Talking-head footage dựng đúng theo danh sách cut (đã gọt khoảng lặng)
  - Text Track 1: Hook Headline + Eyebrow
  - Text Track 2: Subtitles né cằm (vị trí lấy từ AI Chin-lock, mặc định Y ~ -0.36)

Hành vi lỗi (đã sửa): thiếu engine vectcut hoặc ghi draft thất bại sẽ ném CapCutUnavailable / RuntimeError
với thông báo rõ ràng, thay vì im lặng trả về một thư mục rỗng như đã thành công.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

HERE = Path(__file__).resolve().parent
VECTCUT_DIR = HERE / "vectcut"
if str(VECTCUT_DIR) not in sys.path:
    sys.path.insert(0, str(VECTCUT_DIR))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

VECTCUT_ERROR: Optional[str] = None
try:
    from create_draft import get_or_create_draft
    from add_video_track import add_video_track
    from add_text_impl import add_text_impl
    import draft_safety
    VECTCUT_AVAILABLE = True
except Exception as e:  # noqa: BLE001 - ghi lại nguyên nhân để báo lỗi rõ ràng ở bước dùng
    VECTCUT_AVAILABLE = False
    VECTCUT_ERROR = f"{type(e).__name__}: {e}"


class CapCutUnavailable(RuntimeError):
    """Engine vectcut không nạp được (thường do thiếu thư viện trong engines/capcut/vectcut/requirements.txt)."""


def default_drafts_root() -> Path:
    """Thư mục draft mặc định của CapCut Desktop trên máy hiện tại."""
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        return Path(local_app_data) / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"
    return Path.home() / "Movies" / "CapCut" / "User Data" / "Projects" / "com.lveditor.draft"


class CapCutDraftBuilder:
    def __init__(self, project_name: str, drafts_dir: Optional[str] = None):
        if not VECTCUT_AVAILABLE:
            raise CapCutUnavailable(
                f"Không nạp được engine CapCut ({VECTCUT_ERROR}). "
                "Hãy chạy: pip install -r requirements.txt"
            )

        self.project_name = project_name
        self.width = 1080
        self.height = 1920
        self.drafts_root = Path(drafts_dir) if drafts_dir else default_drafts_root()

        # Không tạo sẵn thư mục rỗng mang tên dự án: engine ghi draft vào <drafts_root>/<draft_id>.
        self.draft_id, self.script = get_or_create_draft(width=self.width, height=self.height)
        self._folder = str(self.drafts_root).replace("\\", "/")

    @property
    def project_dir(self) -> Path:
        """Thư mục draft thật sự (tên do engine đặt theo draft_id)."""
        return self.drafts_root / self.draft_id

    def add_main_video(
        self,
        video_path: str,
        duration_sec: Optional[float] = None,
        cuts: Optional[List[Dict[str, Any]]] = None
    ):
        """
        Thêm video chính vào track 'main_video'.
        - Có `cuts`: mỗi cut thành một clip, nối liền nhau trên timeline (đúng với khoảng lặng đã gọt).
        - Không có `cuts`: một clip duy nhất từ 0 đến duration_sec.
        """
        abs_path = os.path.abspath(video_path).replace("\\", "/")

        if cuts:
            cursor = 0.0
            for c in cuts:
                src_in = float(c.get("source_in", c.get("video_in", 0.0)))
                src_out = float(c.get("source_out", c.get("video_out", src_in + c.get("duration", 0.0))))
                if src_out <= src_in:
                    continue
                add_video_track(
                    video_url=abs_path,
                    draft_folder=self._folder,
                    draft_id=self.draft_id,
                    start=src_in,
                    end=src_out,
                    target_start=cursor,
                    track_name="main_video",
                    relative_index=0
                )
                cursor += (src_out - src_in)
            return

        add_video_track(
            video_url=abs_path,
            draft_folder=self._folder,
            draft_id=self.draft_id,
            start=0,
            end=duration_sec,
            track_name="main_video",
            relative_index=0
        )

    def add_hook(
        self,
        headline: str,
        eyebrow: Optional[str] = None,
        duration_sec: float = 5.0,
        font_name: str = "Playfair Display",
        font_color: str = "#F2EDE4"
    ):
        """Thêm cụm chữ Hook mở đầu ở 1/3 trên màn hình."""
        add_text_impl(
            text=headline,
            start=0,
            end=duration_sec,
            draft_id=self.draft_id,
            transform_y=0.62,
            font_size=18.0,
            font_color=font_color,
            font=font_name,
            track_name="hook_headline"
        )
        if eyebrow:
            add_text_impl(
                text=eyebrow.upper(),
                start=0,
                end=duration_sec,
                draft_id=self.draft_id,
                transform_y=0.72,
                font_size=10.0,
                font_color="#720000",
                font=font_name,
                track_name="hook_eyebrow"
            )

    def add_subtitles(
        self,
        subtitles: List[Dict[str, Any]],
        font_name: str = "Be Vietnam Pro",
        font_color: str = "#FFFFFF",
        transform_y: float = -0.36
    ):
        """
        Thêm phụ đề né cằm. Mỗi phụ đề có thể mang `transform_y` riêng (do ChinLock gắn vào);
        nếu không có thì dùng giá trị mặc định.
        """
        for s in subtitles:
            text = s.get("text", "").strip()
            if not text:
                continue
            add_text_impl(
                text=text,
                start=s["start"],
                end=s["end"],
                draft_id=self.draft_id,
                transform_y=s.get("transform_y", transform_y),
                font_size=10.5,
                font_color=font_color,
                font=font_name,
                track_name="subtitles_track"
            )

    def finalize(self) -> str:
        """
        Ghi draft ra đĩa và trả về đường dẫn thư mục draft thật.
        Từ chối ghi khi CapCut đang mở (CapCut sẽ lặng lẽ ghi đè), và ném lỗi nếu engine báo thất bại.
        """
        draft_safety.require_capcut_quit("tạo dự án CapCut mới")

        result = None
        try:
            from save_draft_impl import save_draft_impl, query_task_status
            result = save_draft_impl(draft_id=self.draft_id, draft_folder=self._folder)
            # save_draft_impl nuốt ngoại lệ và trả về chuỗi rỗng cho CẢ trường hợp thành công lẫn thất bại,
            # nên phải đọc trạng thái tác vụ mới biết kết quả thật.
            status = query_task_status(self.draft_id)
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Ghi dự án CapCut thất bại: {type(e).__name__}: {e}") from e

        if not isinstance(result, dict) or not result.get("success"):
            reason = result.get("error") if isinstance(result, dict) else result
            raise RuntimeError(f"Engine CapCut báo lỗi khi ghi dự án: {reason}")

        if status.get("status") != "completed":
            raise RuntimeError(
                f"Engine CapCut không hoàn tất việc ghi dự án (trạng thái: {status.get('status')}): "
                f"{status.get('message')}"
            )

        if not self.project_dir.is_dir():
            raise RuntimeError(f"Engine báo thành công nhưng không thấy thư mục dự án: {self.project_dir}")

        return str(self.project_dir)
