# 🎬 LEVI SUPER STUDIO v4.0 (Omni-Pipeline Edition)

> **Commercial-Grade Autonomous Video & Multi-Channel Content Production Engine**  
> Hợp nhất tinh hoa giữa **CapCut Desktop Native Draft** + **Adobe Premiere Pro & After Effects Suite** + **Remotion 60fps GPU Graphics** + **Computer-Vision 3D Chin-Lock** + **Instagram Carousel & Story Kit**.

[![GitHub](https://img.shields.io/badge/GitHub-swifttecheducation%2Flevi-blue?logo=github)](https://github.com/swifttecheducation/levi)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?logo=python)]()
[![Adobe](https://img.shields.io/badge/Adobe-Premiere%20%26%20AE-red?logo=adobe)]()
[![CapCut](https://img.shields.io/badge/CapCut-Desktop%20Native-00C4CC)]()
[![Remotion](https://img.shields.io/badge/Remotion-4.0%20GPU-red)]()

---

## 🌟 Đột Phá Kiến Trúc (Architecture Innovations)

1. **Dual-Lane Output (Làn Kép Song Song):**
   - **Fast-Lane:** Sinh file dự án CapCut Desktop đa track rời lớp (`draft_content.json`) để chỉnh sửa nhanh trên laptop hoặc mobile.
   - **Pro-Lane (Cinema Studio):** Tự động tạo timeline **Adobe Premiere Pro XML** (`.xml` / FCPXML) liên kết động với kịch bản **After Effects ExtendScript** (`.jsx`) áp dụng biểu thức chuyển động nảy đàn hồi (*Inertial Bounce*) và rung lắc tự nhiên (*Organic Wiggle*), hỗ trợ render ngầm GPU bằng `aerender.exe`.
2. **AI Chin-Lock 3D & Dynamic Safe-Zone:** Sử dụng mạng nơ-ron **OpenCV YuNet** (`assets/models/face_detection_yunet_2023mar.onnx`) để theo dõi cằm và góc nghiêng đầu từng frame, tự động neo phụ đề và thẻ hook bên dưới xương quai xanh, tuyệt đối không che mắt hay miệng người nói.
3. **Remotion Motion Farm (60fps Alpha):** Xuất các lớp đồ họa chuyển động phức tạp (Code viewer, bảng đếm số, terminal) thành video trong suốt kênh Alpha (ProRes 4444 / WebM VP9) để phủ trực tiếp vào Premiere hoặc CapCut.
4. **Broadcast Audio Standards (EBU R128 -14 LUFS):** Tự động cân bằng âm lượng giọng nói chuẩn phát sóng, giới hạn True Peak dưới -1.5 dBTP và tự động giảm âm nhạc nền (Audio Ducking -18dB) khi có tiếng nói.
5. **Trọn Bộ Đa Kênh Chuẩn Brand Kit:** Tự động trích xuất nội dung từ video Reel để tạo bộ slide vuốt ngang **Instagram Carousel (1080x1350)** và chuỗi tin ngắn **Story Kit (9:16)** chừa sẵn vị trí dán Sticker tương tác.
6. **Bảng Phân Cảnh Beat Sheet:** Xuất storyboard ảnh tĩnh đánh số các phân đoạn then chốt (`beat_sheet.jpg`) để người sáng tạo duyệt bố cục chữ và hình trong 10 giây trước khi bấm render.
7. **Trial Reels (A/B Testing):** Tự động tạo 3 biến thể nội dung từ 1 video gốc (đổi câu Hook mở đầu, nhịp cắt và năng lượng âm nhạc) để test thuật toán Instagram.

---

## 🚀 Hướng Dẫn Bắt Đầu Nhanh (Quick Start)

### 1. Cài đặt môi trường
Yêu cầu: Python 3.10+, FFmpeg trên PATH hệ thống.
```bash
pip install -r requirements.txt
```

### 2. Kiểm tra trạng thái hệ thống & Brand Kit
```bash
python studio.py status
```

### 3. Chạy Dựng Tự Động 1-Chạm (Autopilot)
Chỉ cần thả video thô vào thư mục `inbox/` và chạy:
```bash
python studio.py autopilot
```
Hệ thống sẽ tự động quét video, cắt gọt khoảng lặng, cân bằng âm thanh -14 LUFS, quét cằm né mặt và xuất đầy đủ:
- Bảng duyệt `outbox/<tên_dự_án>_beat_sheet.jpg`
- Dự án CapCut Desktop hoàn chỉnh
- Timeline Adobe Premiere Pro XML (`outbox/<tên_dự_án>_Premiere.xml`)
- Kịch bản After Effects JSX (`outbox/<tên_dự_án>_AfterEffects.jsx`)
- Bộ slide Instagram Carousel (`outbox/carousel/`)

---

## 🛠️ Danh Sách Lệnh CLI

| Lệnh | Mô tả |
| :--- | :--- |
| `python studio.py autopilot` | Dựng tự động 1-chạm toàn bộ quy trình từ video trong inbox/ |
| `python studio.py premiere -v <video>` | Xuất file Timeline FCPXML mở trực tiếp trong Adobe Premiere Pro |
| `python studio.py ae -t "<câu_hook>"` | Xuất kịch bản After Effects ExtendScript JSX |
| `python studio.py beat-sheet -v <video>` | Xuất bảng ảnh Storyboard duyệt nhanh |
| `python studio.py carousel -H "<tiêu_đề>"` | Tạo bộ ảnh vuốt ngang Instagram Carousel (1080x1350) |

---

## 📂 Cấu Trúc Dự Án

```text
levi/
├── inbox/                        # Thư mục thả video thô
├── outbox/                       # Nơi xuất sản phẩm hoàn thiện
├── brand-kit.md                  # Nhận diện thương hiệu (Màu sắc, Font, Voice DNA)
├── AGENTS.md                     # Hướng dẫn vận hành cho Trợ lý AI (Tiếng Việt)
├── studio.py                     # CLI điều hành trung tâm
│
├── core/                         # Bộ não AI & Media Analysis
│   ├── whisper_transcriber.py    # Bóc tách giọng nói Whisper & nhịp chữ
│   ├── chin_lock.py              # Tracking cằm & né mặt YuNet
│   ├── audio_master.py           # EBU R128 (-14 LUFS) & Smart Ducking
│   ├── rough_cutter.py           # Dead-air trimmer & Micro-zoom
│   └── brand_engine.py           # Phân tích Brand Kit
│
├── engines/                      # Bộ điều khiển xuất Timeline
│   ├── adobe/                    # Adobe Creative Suite (Premiere XML + AE JSX + aerender)
│   ├── capcut/                   # CapCut Desktop Native Draft (VectCut)
│   └── remotion/                 # Remotion 60fps GPU Graphics Studio
│
├── workflows/                    # Quy trình sản xuất tự động
│   ├── autopilot.py              # Dựng 1-chạm
│   ├── beat_sheet.py             # Bảng phân cảnh storyboard
│   ├── trial_reels.py            # 3 bản dựng A/B Testing
│   └── carousel_story/           # Instagram Carousel & Story Kit
│
├── assets/                       # Tài nguyên chuẩn hóa (Fonts Việt hóa, YuNet model, SFX)
└── tests/                        # Bộ kiểm thử tự động (AST Syntax & Unit Tests)
```

---

## 📜 Bản Quyền
Phát triển bởi [SwiftTech Education](https://github.com/swifttecheducation). Giấy phép MIT.
