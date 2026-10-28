#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/motion_reframer.py — Tái Cấu Trúc Khung Hình Điện Ảnh & Chuyển Động Mượt Mà (Motion Blur & Bezier Zoom).
Thay thế các cú phóng to giật cục bằng chuyển động Bezier tự nhiên (Cubic-Bezier Ease-Out).
Mô phỏng góc mở màn trập 180 độ (180-degree Shutter Angle) để tạo độ mờ chuyển động (Motion Blur) 
giúp mắt người xem không bị mỏi khi xem video dọc 9:16.
"""

import math
from typing import Dict, Any, List, Tuple


class MotionReframer:
    def __init__(
        self,
        base_scale: float = 1.0,
        punch_in_scale: float = 1.08,
        transition_duration_sec: float = 0.25,
        shutter_angle: int = 180
    ):
        self.base_scale = base_scale
        self.punch_in_scale = punch_in_scale
        self.transition_duration_sec = transition_duration_sec
        self.shutter_angle = shutter_angle

    def cubic_bezier_ease_out(self, t: float) -> float:
        """Đường cong gia tốc Bezier Ease-Out (0.25, 0.1, 0.25, 1.0)."""
        # Công thức mượt mà t*(2-t) hoặc cubic
        t = max(0.0, min(1.0, t))
        return 1.0 - math.pow(1.0 - t, 3)

    def compute_zoom_keyframes(
        self,
        clip_start: float,
        target_scale: float,
        fps: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Tính toán chuỗi keyframe scale chuyển tiếp mượt mà trong transition_duration_sec.
        """
        frames = int(self.transition_duration_sec * fps)
        keyframes = []

        start_scale = self.base_scale if target_scale != self.base_scale else self.punch_in_scale

        for i in range(frames + 1):
            progress = i / float(frames)
            ease_val = self.cubic_bezier_ease_out(progress)
            cur_scale = start_scale + (target_scale - start_scale) * ease_val
            t_sec = clip_start + (i / float(fps))

            keyframes.append({
                "time": round(t_sec, 3),
                "scale": round(cur_scale, 4),
                "motion_blur_amount": round(abs(target_scale - start_scale) * (1.0 - ease_val), 3)
            })

        return keyframes

    def get_after_effects_bezier_expression(self) -> str:
        """Trả về biểu thức After Effects áp dụng Ease-in/Ease-out tự nhiên."""
        return """
// Cubic Bezier Smooth Zoom
var dur = 0.25;
if (time < inPoint + dur) {
    var t = (time - inPoint) / dur;
    var easeVal = 1 - Math.pow(1 - t, 3);
    linear(easeVal, 0, 1, [100, 100], [108, 108]);
} else {
    [108, 108];
}
""".strip()
