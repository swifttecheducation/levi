# 📖 CẨM NANG HƯỚNG DẪN SỬ DỤNG LEVI SUPER STUDIO v4.0

> Chào mừng bạn đến với **Levi Super Studio v4.0** — Hệ thống sản xuất video và nội dung mạng xã hội đa kênh tự động hóa chuẩn điện ảnh.

---

## 🚀 1. Chuẩn Bị & Cài Đặt Môi Trường (3 Phút)

### Yêu cầu cấu hình máy:
- **Hệ điều hành:** Windows 10/11 hoặc macOS 12+
- **Python:** Phiên bản 3.10 trở lên
- **FFmpeg:** Đã cài đặt và có trong PATH hệ thống (để xử lý âm thanh và video)
- **Công cụ tùy chọn (Khuyến nghị):**
  - CapCut Desktop (bản Quốc tế hoặc Jianying)
  - Adobe Premiere Pro / After Effects (nếu muốn làm bản Cinema Grade)
  - Node.js 18+ (nếu muốn render Remotion React 60fps)

### Cài đặt thư viện Python:
Mở Terminal tại thư mục `levi/` và chạy:
```bash
pip install -r requirements.txt
```

---

## 🎨 2. Cấu Hình Thương Hiệu Cá Nhân (`brand-kit.md`)

Trước khi bắt đầu, hãy mở file [`brand-kit.md`](../brand-kit.md) để cá nhân hóa:
1. **Tên thương hiệu:** Đổi thành tên kênh của bạn.
2. **Font chữ:** Lựa chọn bộ phong cách yêu thích (Editorial Luxe, Modern Minimal hoặc Gen Z Pop). Toàn bộ 100% phông chữ đã được tích hợp sẵn trong thư mục `assets/fonts/` và được Việt hóa hoàn hảo, không bị lỗi ô vuông (tofu).
3. **Bảng màu:** Cập nhật 4 mã màu chủ đạo (Primary, Secondary, Accent, Highlight).
4. **Từ khóa ManyChat:** Danh sách từ khóa để tự động gửi quà tặng khi người xem bình luận.

---

## ⚡ 3. Quy Trình Dựng Video Cơ Bản (3 Bước)

### Bước 1: Thả video thô vào `inbox/`
Quay video bằng điện thoại (khung dọc 9:16) và copy file vào thư mục `inbox/` (ví dụ: `inbox/raw_talk.mp4`).

### Bước 2: Kích hoạt dựng tự động
Chạy lệnh:
```bash
python studio.py autopilot
```
Hoặc trong cửa sổ chat với AI (Gemini, Claude, Cursor), bạn chỉ cần gõ:
> *"dựng video trong inbox cho mình"*

### Bước 3: Nhận thành phẩm trong `outbox/`
Chỉ sau khoảng 15-30 giây, hệ thống sẽ xuất toàn bộ:
1. **`outbox/<tên_dự_án>_beat_sheet.jpg`**: Mở xem ảnh này đầu tiên để duyệt nhanh khung hình, vị trí chữ và cằm.
2. **Dự án CapCut Desktop**: Tự động xuất hiện trong màn hình chính của CapCut Desktop, mở lên là có đầy đủ các track rời lớp để tinh chỉnh.
3. **Timeline Premiere Pro (`.xml`)**: Kéo thả thẳng vào Adobe Premiere Pro để chỉnh màu Lumetri hoặc hòa âm nâng cao.
4. **Kịch bản After Effects (`.jsx`)**: Mở After Effects -> File -> Scripts -> Run Script File để sinh animation nảy đàn hồi (*Inertial Bounce*).
5. **Bộ ảnh Carousel (`outbox/carousel/`)**: Toàn bộ slide 1080x1350 sẵn sàng đăng Instagram.
