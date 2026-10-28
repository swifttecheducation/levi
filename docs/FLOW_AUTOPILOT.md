# ⚡ LUỒNG DỰNG TỰ ĐỘNG 1-CHẠM (AUTOPILOT OMNI-PIPELINE)

> Luồng Autopilot là trái tim của hệ thống: Biến một đoạn video quay thô bằng điện thoại thành trọn bộ sản phẩm đa kênh hoàn thiện mà không cần người dùng thao tác thủ công.

---

## 🏛️ Sơ Đồ 7 Bước Xử Lý Của Autopilot

```
[ Video Thô: inbox/raw.mp4 ]
            │
            ▼
[ Bước 1: Whisper Transcription & Word Chunking ]
  -> Bóc tách âm thanh, gom thành các cụm 2-4 từ/nhịp hiển thị
            │
            ▼
[ Bước 2: Dead-Air Trimmer & Micro-Zoom Calculator ]
  -> Cắt sạch khoảng lặng > 0.35s, xen kẽ zoom 1.0 vs 1.08 tại các vết cắt
            │
            ▼
[ Bước 3: AI Chin-Lock 3D Face Anchor (YuNet) ]
  -> Quét vị trí cằm từng frame, tính toán vùng an toàn dưới xương quai xanh (Y ~ 1320px)
            │
            ▼
[ Bước 4: Beat Sheet Storyboard Contact Sheet ]
  -> Trích xuất các keyframe quan trọng ghép thành ảnh beat_sheet.jpg để duyệt trong 10s
            │
            ▼
[ Bước 5: CapCut Desktop Draft Builder (VectCut) ]
  -> Sinh file draft_content.json đa track (Video + B-Roll + Hook + Subtitle + Audio)
            │
            ▼
[ Bước 6: Adobe Pro Suite Dispatcher ]
  -> Sinh file Timeline Premiere Pro XML (<xmeml>) + Kịch bản After Effects JSX
            │
            ▼
[ Bước 7: Multi-Format Packaging ]
  -> Xuất 3 biến thể Trial Reels A/B Test + Bộ slide Instagram Carousel (1080x1350)
```

---

## 💻 Cách Khởi Chạy

```bash
# 1. Tự động nhận diện video trong inbox/
python studio.py autopilot

# 2. Hoặc chỉ định video và đặt tên dự án cụ thể
python studio.py autopilot --video "duong/dan/video.mp4" --name "Bai_Hoc_1" --headline "Bí Quyết Thành Công"
```
