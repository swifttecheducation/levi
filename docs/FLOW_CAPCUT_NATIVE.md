# 📱 LUỒNG CAPCUT DESKTOP NATIVE DRAFT

> Giúp nhà sáng tạo có ngay một dự án CapCut hoàn chỉnh để xem và tinh chỉnh lại bằng tay nếu cần, thay vì xuất ra file MP4 dính chết (flattened) không thể sửa chữ.

---

## 1. Cơ Chế Hoạt Động (`engines/capcut/draft_builder.py`)
- Sử dụng cầu nối **VectCut / pyJianYingDraft** để ghi trực tiếp dữ liệu vào thư mục dự án cục bộ của CapCut Desktop:
  - **Trên Windows:** `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\<tên_dự_án>\`
  - **Trên macOS:** `~/Movies/CapCut/User Data/Projects/com.lveditor.draft/<tên_dự_án>/`
- Sinh ra các file dữ liệu chuẩn:
  - `draft_content.json`: Chứa cấu trúc toàn bộ các track, clip, text, keyframe và effect.
  - `draft_meta_info.json`: Chứa tên dự án, ảnh thumbnail, kích thước 1080x1920.

---

## 2. Các Lớp (Tracks) Trong Dự Án CapCut
1. **Video Track 0 (Main Track):** Video người nói quay thô, đã được tính toán thời lượng cắt.
2. **Video Track 1 (Overlay):** B-Roll hoặc các cảnh quay bổ trợ chèn đè lên trên.
3. **Text Track 1 (Hook Title):** Câu tiêu đề lớn ở 1/3 trên màn hình (y ~ 0.62) kèm Eyebrow phụ (y ~ 0.72).
4. **Text Track 2 (Subtitles):** Phụ đề chạy chữ từng câu ngắn (2-4 từ/nhịp), tự động neo ở vị trí an toàn né mặt (transform_y = -0.36).
5. **Audio Tracks:** Giọng đọc chính, âm thanh hiệu ứng (SFX) và nhạc nền.

---

## 3. Cách Sử Dụng
Sau khi chạy lệnh `python studio.py autopilot`, bạn chỉ cần:
1. Mở phần mềm **CapCut Desktop**.
2. Dự án mới sẽ lập tức xuất hiện ngay trên trang chủ.
3. Bấm vào dự án để xem trước hoặc đổi lại từng chữ, đổi màu, thay nhạc theo ý thích!
