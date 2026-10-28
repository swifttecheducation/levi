# 📋 LUỒNG STORYBOARD BEAT SHEET & TRIAL REELS A/B TEST

> Giúp nhà sáng tạo duyệt nhanh nội dung trong 10 giây và thử nghiệm các biến thể khác nhau để chinh phục thuật toán Instagram.

---

## 1. Bảng Phân Cảnh Beat Sheet (`workflows/beat_sheet.py`)
- **Vấn đề giải quyết:** Thay vì phải chờ đợi máy tính render một video dài 5-10 phút rồi mới phát hiện chữ bị che hoặc sai lỗi chính tả, Beat Sheet giúp bạn xem trước toàn bộ khung hình then chốt dưới dạng ảnh tĩnh.
- **Quy cách file `beat_sheet.jpg`:**
  - Trích xuất 6-12 khung hình tiêu biểu tại các điểm chuyển cảnh và nhịp nói.
  - Mỗi khung hình được đánh số thứ tự rõ ràng (`Beat #1 | 0.0s`, `Beat #2 | 3.5s`...).
  - Ghép thành 1 tấm ảnh lưới tổng thể lưu tại `outbox/<tên_dự_án>_beat_sheet.jpg`.
- **Cách sử dụng:**
  - Chạy lệnh: `python studio.py beat-sheet -v <video>`
  - Mở file ảnh `beat_sheet.jpg` để duyệt nhanh chữ, cằm, màu sắc trước khi render video hoàn thiện.

---

## 2. Video Thử Nghiệm Trial Reels (`workflows/trial_reels.py`)
- **Mục đích:** Tận dụng tính năng **Trial Reels** của Instagram (cho phép đăng thử nghiệm video tới những người chưa theo dõi để đo lường tỷ lệ giữ chân).
- **3 Biến thể sinh ra từ 1 video gốc:**
  - **Bản A (High Urgency Punch):** Phóng to ngay từ giây đầu (Zoom 1.12), câu Hook giật tít cảnh báo trực diện, nhịp cắt nhanh, âm thanh dồn dập.
  - **Bản B (Curiosity Question):** Câu Hook đặt câu hỏi gợi mở sự tò mò, nhịp kể chuyện điềm tĩnh, nhạc nền du dương.
  - **Bản C (Contrarian Editorial):** Câu Hook đi ngược số đông ("Hầu hết mọi người đang hiểu sai về..."), phong cách tạp chí tối giản, tinh tế.
- **Hiệu quả:** Thuật toán Instagram không đánh giá đây là các video trùng lặp (re-up) vì câu mở đầu, nhịp độ và cấu trúc thị giác hoàn toàn khác biệt.
