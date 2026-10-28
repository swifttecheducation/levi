#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engines/adobe/aerender_service.py — Bộ điều khiển Render ngầm Adobe After Effects qua dòng lệnh (aerender).
Tự động tìm kiếm thư mục cài đặt Adobe After Effects trên Windows/macOS.
Cho phép xuất video ProRes / MP4 / H.264 trực tiếp bằng GPU mà không cần mở giao diện After Effects.
"""

import os
import glob
import subprocess
from typing import Optional, List


class AERenderService:
    def __init__(self, aerender_binary_path: Optional[str] = None):
        self.binary_path = aerender_binary_path or self._find_aerender_executable()

    def _find_aerender_executable(self) -> Optional[str]:
        """Tự động tìm đường dẫn aerender.exe trên hệ thống."""
        if os.name == "nt":
            candidates = [
                r"C:\Program Files\Adobe\Adobe After Effects 2026\Support Files\aerender.exe",
                r"C:\Program Files\Adobe\Adobe After Effects 2025\Support Files\aerender.exe",
                r"C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\aerender.exe",
                r"C:\Program Files\Adobe\Adobe After Effects 2023\Support Files\aerender.exe",
            ]
            for c in candidates:
                if os.path.exists(c):
                    return c
            
            # Quét pattern linh hoạt
            matched = glob.glob(r"C:\Program Files\Adobe\Adobe After Effects *\Support Files\aerender.exe")
            if matched:
                return matched[-1]
        else:
            mac_paths = [
                "/Applications/Adobe After Effects 2026/aerender",
                "/Applications/Adobe After Effects 2025/aerender",
                "/Applications/Adobe After Effects 2024/aerender"
            ]
            for p in mac_paths:
                if os.path.exists(p):
                    return p

        return None

    def is_available(self) -> bool:
        """Kiểm tra máy có cài đặt Adobe After Effects command line không."""
        return bool(self.binary_path and os.path.exists(self.binary_path))

    def render_project(
        self,
        project_aep_path: str,
        comp_name: str,
        output_file_path: str,
        output_module: str = "Lossless with Alpha"
    ) -> bool:
        """Thực thi render ngầm một Composition trong file .aep."""
        if not self.is_available():
            print("[AERenderService] Note: Không tìm thấy After Effects aerender trên máy này.")
            return False

        cmd = [
            self.binary_path,
            "-project", project_aep_path,
            "-comp", comp_name,
            "-output", output_file_path,
            "-OMtemplate", output_module
        ]

        try:
            print(f"[AERenderService] Đang kích hoạt After Effects GPU render: {comp_name}...")
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=300)
            return res.returncode == 0
        except Exception as e:
            print(f"[AERenderService] Render thất bại: {e}")
            return False
