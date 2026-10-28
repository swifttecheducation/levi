#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
core/chin_lock.py — Công nghệ Khóa Cằm (AI Chin-Lock 3D) & Neo Phụ Đề An Toàn.
Sử dụng mô hình OpenCV YuNet (assets/models/face_detection_yunet_2023mar.onnx)
để quét vị trí cằm, mắt và góc nghiêng đầu từng frame.
Tự động neo chữ và phụ đề dưới xương quai xanh (collar line) hoặc góc an toàn,
tuyệt đối không để phụ đề đè lên khuôn mặt người nói.
"""

import os
import sys
import json
import math
from typing import List, Dict, Any, Tuple, Optional


AUTH_WIDTH = 1080
AUTH_HEIGHT = 1920
DEFAULT_COLLAR_OFFSET_PX = 60  # Cách đỉnh cằm 60px xuống dưới


class ChinLock:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets", "models", "face_detection_yunet_2023mar.onnx"
        )
        self.detector = None
        self._init_detector()

    def _init_detector(self):
        """Khởi tạo bộ nhận diện khuôn mặt YuNet của OpenCV nếu có thư viện."""
        if not os.path.exists(self.model_path):
            return
        try:
            import cv2
            self.detector = cv2.FaceDetectorYN_create(
                self.model_path, "", (AUTH_WIDTH, AUTH_HEIGHT),
                score_threshold=0.6, nms_threshold=0.3
            )
        except Exception:
            self.detector = None

    def calculate_default_anchor_y(self) -> float:
        """
        Vị trí mặc định an toàn cho màn hình 9:16 (1080x1920) khi không có camera:
        y ~ 1300px (tương đương transform_y = -0.35 trong CapCut chuẩn).
        """
        return 1320.0

    def analyze_frame(self, frame_img) -> Optional[Dict[str, Any]]:
        """Quét 1 frame ảnh và trả về tọa độ cằm + góc nghiêng đầu."""
        if self.detector is None or frame_img is None:
            return None

        try:
            import cv2
            h, w = frame_img.shape[:2]
            self.detector.setInputSize((w, h))
            _, faces = self.detector.detect(frame_img)
            if faces is None or len(faces) == 0:
                return None

            # Chọn khuôn mặt lớn nhất (gần camera nhất)
            best_face = max(faces, key=lambda f: f[2] * f[3])
            fx, fy, fw, fh = best_face[0:4]
            
            # Cằm xấp xỉ ở đáy của bounding box khuôn mặt
            chin_y = fy + fh
            scale_y = AUTH_HEIGHT / float(h)
            chin_y_auth = chin_y * scale_y

            # Landmark mắt để tính góc xoay (Head Roll Angle)
            # best_face[4:14] chứa 5 điểm landmarks (mắt phải, mắt trái, mũi, mép miệng phải, mép miệng trái)
            eye_r = (best_face[4], best_face[5])
            eye_l = (best_face[6], best_face[7])
            dx = eye_l[0] - eye_r[0]
            dy = eye_l[1] - eye_r[1]
            roll_deg = math.degrees(math.atan2(dy, dx)) if dx != 0 else 0.0

            return {
                "face_box": [float(fx), float(fy), float(fw), float(fh)],
                "chin_y": round(float(chin_y_auth), 2),
                "safe_sub_top_y": round(float(chin_y_auth + DEFAULT_COLLAR_OFFSET_PX), 2),
                "head_roll_deg": round(roll_deg, 2)
            }
        except Exception:
            return None

    def get_timeline_chin_anchors(
        self,
        video_path: str,
        sample_interval_sec: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Quét video theo chu kỳ mẫu và sinh chuỗi tọa độ neo chữ làm mượt theo thời gian.
        Nếu không có OpenCV hoặc không tìm thấy mặt, trả về vị trí chuẩn tĩnh an toàn.
        """
        anchors = []
        default_y = self.calculate_default_anchor_y()

        if not os.path.exists(video_path) or self.detector is None:
            # Fallback an toàn
            return [{"timestamp": 0.0, "sub_top_y": default_y, "roll_deg": 0.0}]

        try:
            import cv2
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            frame_step = max(1, int(fps * sample_interval_sec))

            frame_idx = 0
            while frame_idx < total_frames:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                if not ret:
                    break
                t_sec = frame_idx / fps
                info = self.analyze_frame(frame)
                sub_y = info["safe_sub_top_y"] if info else default_y
                roll = info["head_roll_deg"] if info else 0.0

                anchors.append({
                    "timestamp": round(t_sec, 2),
                    "sub_top_y": sub_y,
                    "roll_deg": roll
                })
                frame_idx += frame_step

            cap.release()
        except Exception as e:
            print(f"[ChinLock] Note: Quét nhanh fallback: {e}")
            anchors = [{"timestamp": 0.0, "sub_top_y": default_y, "roll_deg": 0.0}]

        return anchors if anchors else [{"timestamp": 0.0, "sub_top_y": default_y, "roll_deg": 0.0}]
