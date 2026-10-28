# 🏆 CẨM NANG BÀN GIAO & HƯỚNG DẪN DÀNH CHO KHÁCH HÀNG (VIP EDITION)

> **Chào mừng bạn đến với LEVI SUPER STUDIO v4.0** — Hệ thống sản xuất video ngắn (Reels, TikTok, Shorts) tự động hóa chuẩn điện ảnh và nhận diện thương hiệu cá nhân.

---

## ⚡ BẮT ĐẦU NHANH TRONG 3 BƯỚC (DÀNH CHO NGƯỜI MỚI)

Bạn không cần biết lập trình hay gõ lệnh phức tạp, mọi thao tác đã được đóng gói thành các tệp chạy tự động 1-click:

```
📁 Thư mục LEVI/
├── 1_KHOI_DONG_CAI_DAT.bat            <-- [BƯỚC 1]: Chạy file này lần đầu để thiết lập hệ thống
├── inbox/                             <-- [BƯỚC 2]: Thả video thô vừa quay vào đây
├── 2_DUNG_VIDEO_TU_DONG_1_CHAM.bat    <-- [BƯỚC 3]: Chạy file này để AI tự động dựng từ A-Z
└── outbox/                            <-- Nhận video, timeline Premiere & kịch bản After Effects
```

---

## 🛠️ CHI TIẾT CÁC FILE CHẠY NHANH TRÊN WINDOWS

| Tên File | Chức Năng | Khi Nào Sử Dụng? |
| :--- | :--- | :--- |
| **`1_KHOI_DONG_CAI_DAT.bat`** | Kiểm tra môi trường, cài đặt thư viện và dẫn dắt bạn thiết lập Brand Kit ban đầu. | Chạy 1 lần duy nhất khi vừa giải nén công cụ. |
| **`2_DUNG_VIDEO_TU_DONG_1_CHAM.bat`** | Tự động quét video trong `inbox/`, cắt khoảng lặng, cân âm thanh -14 LUFS, khóa cằm né mặt và xuất song song CapCut + Premiere XML. | Dùng hàng ngày khi muốn dựng nhanh video chất lượng cao mà không cần can thiệp. |
| **`3_CHEDO_DAO_DIEN_HOI_TUNG_BUOC.bat`** | Chế độ Đạo Diễn Khoa Học: Hệ thống dừng lại hỏi ý kiến bạn tại 5 bước (Bật J-Cut, Chọn phong cách màu, Khóa cằm, Thêm SFX, Chọn phần mềm xuất). | Dùng khi bạn muốn kiểm soát chi tiết từng phân cảnh theo ý đồ đạo diễn riêng. |
| **`4_THIET_LAP_THUONG_HIEU.bat`** | Phỏng vấn chuyên sâu 7 Trụ Cột ADN Thương Hiệu (Định vị, Voice DNA, Bảng màu, Font chữ, Kịch bản ManyChat, Sửa lỗi phát âm Whisper). | Dùng khi bạn muốn đổi tên kênh, đổi phong cách nhận diện hoặc cập nhật sản phẩm mới. |
| **`5_XEM_THU_VIEN_105_PHONG_CACH.bat`** | Mở thư viện 105 phong cách dựng video (Hooks, Bố cục, Bằng chứng, Chuyển động, Bìa tạp chí...). | Dùng khi bạn muốn tìm cảm hứng và chọn các mã phong cách mới cho video. |
| **`6_KIEM_TRA_TRANG_THAI.bat`** | Báo cáo nhanh tình trạng Brand Kit, font chữ và kiểm tra xem có video nào trong `inbox/` chưa. | Dùng để kiểm tra trước khi bấm nút dựng. |

*(Người dùng macOS / Linux có thể click chạy các file tương ứng: `run_cai_dat.sh`, `run_dung_video.sh`).*

---

## 📥 HƯỚNG DẪN THẢ NGUYÊN LIỆU VÀO THƯ MỤC `inbox/`

1. **Video chính của bạn:**
   - Thả trực tiếp file video thô vừa quay bằng điện thoại/máy ảnh vào thư mục `inbox/` (hoặc `inbox/video_chinh/`).
   - Định dạng: `.mp4`, `.mov`, `.m4v`.
   - Độ phân giải khuyến nghị: 1080x1920 (9:16) hoặc 4K quay dọc.
2. **Nguyên liệu bổ trợ (Tùy chọn):**
   - `inbox/broll/`: Thả các đoạn clip phụ, cảnh minh họa (AI sẽ tự động chèn xen kẽ).
   - `inbox/nhac_nen/`: Thả file nhạc nền (.mp3, .wav) nếu muốn dùng bài nhạc yêu thích (AI tự động giảm -18dB khi bạn nói).
   - `inbox/logo_watermark/`: Thả file logo thương hiệu của bạn dạng PNG nền trong suốt.

---

## 📤 XEM KẾT QUẢ THÀNH PHẨM Ở ĐÂU?

Sau khi hệ thống báo dựng hoàn tất:
1. **Trên CapCut Desktop:**
   - Mở ứng dụng CapCut Desktop trên máy tính.
   - Bạn sẽ thấy một dự án mới xuất hiện ngay đầu danh sách với đầy đủ các track video, phụ đề tự động cắt 2-4 từ/cụm, hiệu ứng nảy và nhạc nền đã được cân bằng âm lượng.
2. **Trên Adobe Premiere Pro:**
   - Mở Premiere Pro -> Nhấn `File` -> `Import` -> Chọn file `.xml` trong thư mục `outbox/`.
   - Toàn bộ Sequence timeline đa lớp với các điểm cắt chuẩn xác sẽ hiện ra ngay lập tức.
3. **Trên Adobe After Effects:**
   - Mở After Effects -> Nhấn `File` -> `Scripts` -> `Run Script File...` -> Chọn file `.jsx` trong thư mục `outbox/`.
   - AE sẽ tự động dựng toàn bộ hoạt họa Typography nảy lò xo (Inertial Bounce).
4. **Ảnh duyệt trước (Beat Sheet) & Slide Carousel:**
   - File ảnh Storyboard tóm tắt 10 khung hình: `outbox/<tên_dự_án>_beat_sheet.jpg`.
   - Bộ ảnh vuốt ngang Instagram Carousel (1080x1350): nằm trong thư mục `outbox/carousel/`.

---

## ❓ CÂU HỎI THƯỜNG GẶP & KHẮC PHỤC SỰ CỐ (FAQ)

### 1. Máy tính báo chưa cài Python?
- Tải Python 3.10 hoặc mới hơn tại: [python.org/downloads](https://www.python.org/downloads/).
- **RẤT QUAN TRỌNG:** Ở màn hình cài đặt đầu tiên, nhớ tích vào ô vuông **"Add Python to PATH"** trước khi bấm Install.

### 2. Máy tính báo thiếu FFmpeg?
- Mở PowerShell (hoặc Terminal) và gõ lệnh:
  ```powershell
  winget install Gyan.FFmpeg
  ```
- Hoặc tải bản giải nén từ [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/) và thêm thư mục `bin` vào PATH.

### 3. Mở CapCut không thấy dự án?
- Hãy đảm bảo bạn đã từng mở phần mềm CapCut Desktop ít nhất một lần trên máy để CapCut tự tạo thư mục cấu hình mặc định.

### 4. Font chữ có bị lỗi tiếng Việt không?
- Hoàn toàn **KHÔNG**. Levi Super Studio đã tích hợp sẵn 5 bộ font chữ Việt hóa 100% chuẩn điện ảnh (`Playfair Display`, `Be Vietnam Pro`, `Caveat`, `Inter`, `Poppins`), đảm bảo không bao giờ bị lỗi ô vuông hay nhảy dấu.

---

**Hỗ trợ kỹ thuật & Cộng đồng:** Tham gia nhóm học viên / khách hàng VIP để nhận cập nhật các preset phong cách mới nhất!
