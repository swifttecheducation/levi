#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
engines/remotion/render_alpha.py — Xuất Motion Graphics trong suốt (Alpha Channel 60fps) qua Remotion.
Sử dụng Remotion CLI để render các Composition React thành video ProRes 4444 hoặc WebM (kênh Alpha),
sẵn sàng thả vào Premiere Pro hoặc CapCut.
"""

import os
import subprocess
from typing import Optional, List


class RemotionAlphaRenderer:
    def __init__(self, remotion_root: Optional[str] = None):
        self.remotion_root = remotion_root or os.path.dirname(os.path.abspath(__file__))

    def build_render_command(
        self,
        composition_id: str,
        output_path: str,
        props_json_path: Optional[str] = None,
        codec: str = "prores"  # 'prores' cho ProRes 4444 hoặc 'vp9' cho WebM
    ) -> List[str]:
        """Tạo câu lệnh render Remotion Alpha."""
        cmd = [
            "npx", "remotion", "render",
            composition_id,
            output_path,
            f"--codec={codec}"
        ]
        if codec == "prores":
            cmd.append("--pixel-format=yuva444p10le")
        elif codec == "vp9":
            cmd.append("--pixel-format=yuva420p")

        if props_json_path and os.path.exists(props_json_path):
            cmd.append(f"--props={props_json_path}")

        return cmd

    def render_alpha_overlay(
        self,
        composition_id: str,
        output_path: str,
        props_json_path: Optional[str] = None
    ) -> bool:
        """Thực thi render Remotion Alpha."""
        cmd = self.build_render_command(composition_id, output_path, props_json_path)
        try:
            print(f"[Remotion] Rendering 60fps Alpha: {composition_id}...")
            res = subprocess.run(
                cmd,
                cwd=self.remotion_root,
                shell=(os.name == "nt"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=180
            )
            return res.returncode == 0
        except Exception as e:
            print(f"[Remotion] Warning: Không thể chạy Remotion render: {e}")
            return False
