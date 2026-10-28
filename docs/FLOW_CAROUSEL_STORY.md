# 📸 LUỒNG CAROUSEL (1080x1350) & STORY (9:16) ĐA KÊNH

> Tối ưu hóa triết lý: "Quay đúng 1 lần — Có ngay trọn bộ nội dung đa kênh".

---

## 1. Instagram Carousel Kit (Tỉ lệ 4:5 — 1080x1350)
- **Mục đích:** Tạo bài đăng vuốt ngang giữ chân người xem lâu nhất trên Instagram.
- **Cấu trúc bài viết chuẩn:**
  1. **Slide 1 (Hook Cover):** Tiêu đề giật mắt kèm số thứ tự `1 / N`.
  2. **Slide 2 (Reframe):** Đặt vấn đề hoặc lật ngược góc nhìn quen thuộc.
  3. **Slide 3-4 (Points/Value):** Luận điểm cốt lõi và bài học thực chiến.
  4. **Slide cuối (Closer CTA):** Kêu gọi hành động và nhắc từ khóa ManyChat (`"Comment LEVI để nhận tài liệu"`).
- **Lệnh tạo:**
  ```bash
  python studio.py carousel -H "3 Bí Mật Xây Kênh Triệu View"
  ```
  Các file ảnh chất lượng cao sẽ được xuất ra thư mục `outbox/carousel/slide_01.jpg`, `slide_02.jpg`... sẵn sàng đăng tải.

---

## 2. Story Kit (Tỉ lệ 9:16 — 1080x1920)
- **Mục đích:** Tạo chuỗi tin ngắn Instagram Story tương tác cao (Poll, Link, AMA).
- **Điểm đặc biệt:**
  - Tự động chừa vùng an toàn ở giữa màn hình (y: 900 -> 1250px) để khi bạn đăng lên Story bằng điện thoại, bạn có thể dán trực tiếp:
    - **Sticker Bình chọn (Poll)**
    - **Sticker Câu hỏi (Ask Me Anything)**
    - **Sticker Dán đường link (Link)**
    - **Sticker Đếm ngược (Countdown)**
  - Chữ và tiêu đề không bao giờ bị đè lên bởi các thanh điều hướng của Instagram.
