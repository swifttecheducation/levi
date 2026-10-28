# 🎞️ LUỒNG ADOBE PRO STUDIO (PREMIERE PRO & AFTER EFFECTS)

> Dành cho các dự án đòi hỏi chất lượng điện ảnh (Cinema Grade), chỉnh màu Lumetri sâu, Dynamic Link và hiệu ứng đồ họa chuyển động đỉnh cao.

---

## 1. Cầu Nối Adobe Premiere Pro (`engines/adobe/pr_xml_builder.py`)
- **Định dạng chuẩn:** Sinh file Final Cut Pro 7 XML (`<xmeml version="4">`) chuẩn ngành trao đổi dự án.
- **Cách sử dụng trong Premiere:**
  1. Mở Adobe Premiere Pro.
  2. Chọn `File` -> `Import...` (hoặc kéo thả file `.xml` từ thư mục `outbox/` vào cửa sổ Project).
  3. Premiere sẽ tự động tạo Sequence dọc 9:16 (1080x1920) với đầy đủ các track đã được cắt gọt:
     - **Video Track 1:** Các đoạn video người nói đã cắt sạch dead-air.
     - **Video Track 2:** Cảnh chèn B-Roll cutaways.
     - **Video Track 3:** Lớp đồ họa Remotion hoặc AE MOGRT trong suốt.
     - **Audio Track 1:** Giọng nói đã cân bằng âm lượng -14 LUFS.
     - **Audio Track 2:** Hiệu ứng âm thanh (SFX).
     - **Audio Track 3:** Nhạc nền (BGM) đã hạ âm ngầm.

---

## 2. Kịch Bản Tự Động Hóa After Effects (`engines/adobe/ae_script_generator.py`)
- **Định dạng:** File ExtendScript JavaScript (`.jsx`).
- **Tính năng nổi bật:**
  - Tự động tạo Composition 1080x1920, 30fps.
  - Tự động nạp font tiêu đề chuẩn từ Brand Kit (Playfair Display, Be Vietnam Pro).
  - Tự động gán **Biểu thức đàn hồi lò xo (Inertial Bounce Expression)** vào thuộc tính Scale của câu Hook: Tiêu đề sẽ nảy bật mượt mà từ 0% lên 100% trong 0.4s đầu mà không cần đặt keyframe thủ công.
  - Tự động rải toàn bộ các phân đoạn Subtitle theo đúng mốc thời gian (inPoint / outPoint) bám sát bên dưới cằm.
- **Cách kích hoạt trong After Effects:**
  - Mở After Effects -> Chọn `File` -> `Scripts` -> `Run Script File...` -> Chọn file `.jsx` trong thư mục `outbox/`.

---

## 3. Render Ngầm GPU Bằng Dòng Lệnh (`engines/adobe/aerender_service.py`)
- Tự động quét tìm `aerender.exe` trên hệ thống.
- Cho phép xuất file video trực tiếp từ file dự án `.aep` mà không cần bật giao diện nặng nề của After Effects:
  ```python
  from engines.adobe.aerender_service import AERenderService
  service = AERenderService()
  service.render_project("project.aep", "Levi_Motion_Comp", "output.mov")
  ```
