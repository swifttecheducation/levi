# 🏛️ Quy Trình Thiết Lập Nhận Diện Thương Hiệu 7 Trụ Cột (Brand Kit Wizard)

> **Tài liệu kỹ thuật và hướng dẫn phỏng vấn định vị thương hiệu dành cho LEVI SUPER STUDIO v4.0**

---

## 1. Tổng Quan Về Trụ Sở Thương Hiệu (Brand Homebase)

Trong dựng phim tự động hóa bằng AI, nếu không có bộ nhận diện vững chắc, các video xuất xưởng sẽ trông nhạt nhòa, thiếu cá tính và dễ mắc các lỗi phiên âm tên riêng, sai lệch màu sắc hay vi phạm từ ngữ cấm kỵ.

Tệp `brand-kit.md` đóng vai trò là **Trụ Sở Thương Hiệu (Brand Homebase)** cốt lõi. Mọi luồng trong Levi Super Studio (Autopilot, Director Interactive, CapCut Draft, Premiere Pro XML, After Effects JSX, Whisper Subtitles, Remotion) đều tự động đọc dữ liệu từ tệp này để cá nhân hóa 100% video xuất xưởng.

---

## 2. Chi Tiết 7 Trụ Cột & Các Câu Hỏi Phỏng Vấn (Interview Options)

Khi chạy lệnh:
```bash
python studio.py brand
# hoặc
python studio.py brand-kit
```
Hệ thống sẽ dẫn dắt người dùng qua cuộc phỏng vấn tương tác với đầy đủ 7 trụ cột:

### 📌 [Trụ Cột 1/7] Định Vị Thương Hiệu & Kênh Đăng Tải (Brand Identity & Channels)
- **Câu hỏi 1 (Tên thương hiệu):** *"Tên thương hiệu hoặc tên kênh của bạn là gì?"*
  - Mặc định: `Levi Studio`
  - Ý nghĩa: Được in vào metadata dự án, tiêu đề video, kịch bản After Effects và watermark.
- **Câu hỏi 2 (Chân dung khách hàng & Giải pháp):** *"Bạn giúp đỡ ai, và giải pháp/giá trị bạn mang lại cho họ là gì?"*
  - Mặc định: `Nhà sáng tạo nội dung, Marketer và Chuyên gia số`
  - Ý nghĩa: Giúp AI định hình góc nhìn kịch bản, lựa chọn B-roll phù hợp với đối tượng mục tiêu.
- **Câu hỏi 3 & 4 (Kênh đăng tải):** *"Tài khoản Instagram và TikTok của bạn"*
  - Mặc định: `@tênkênh`
  - Ý nghĩa: Tự động điền vào nhãn dán góc màn hình (Social Handle Badge) và mô tả video.

---

### 📌 [Trụ Cột 2/7] Giọng Điệu Thương Hiệu (Voice & Tone)
- **Câu hỏi 1 (Mô tả giọng điệu):** *"Mô tả giọng điệu của bạn (ví dụ: điềm tĩnh, sâu sắc, thực chiến, truyền cảm hứng, hóm hỉnh...)"*
  - Mặc định: `Điềm tĩnh, sâu sắc, thực chiến và truyền cảm hứng`
  - Ý nghĩa: Hướng dẫn AI trong việc phân bổ nhịp cắt (Pacing), tốc độ nói và lựa chọn nhạc nền (BGM).
- **Câu hỏi 2 (Tiêu chuẩn cảm xúc - Gut Check):** *"Cảm xúc bạn muốn người xem cảm nhận sau khi xem video của bạn?"*
  - Mặc định: `Người xem cảm thấy được khai sáng, nhận được giá trị thực tế áp dụng được ngay.`
  - Ý nghĩa: Thước đo kiểm duyệt kịch bản và nhịp điệu của AI Director trước khi xuất bản.

---

### 📌 [Trụ Cột 3/7] Quy Tắc Câu Từ Cấm Kỵ Bất Biến (Hard Rules & Blacklist)
- **Câu hỏi:** *"Những từ ngữ hoặc cách diễn đạt cấm kỵ mà AI không bao giờ được phép vi phạm? (ngăn cách bằng dấu phẩy)"*
  - Mặc định gợi ý: `Không giật tít rẻ tiền, Không cam kết 100%, Không nói quá, Không tạo áp lực FOMO tiêu cực`
  - Ý nghĩa: Tránh các chính sách cấm quảng cáo của Meta/TikTok/Google, bảo vệ uy tín thương hiệu lâu dài.

---

### 📌 [Trụ Cột 4/7] Câu Từ Quen Thuộc Đặc Trưng (Voice DNA)
- **Câu hỏi 1 (Cấu trúc mở bài - Intro Hook):** *"Cấu trúc câu mở đầu quen thuộc của bạn"*
  - Mặc định gợi ý: `Nhiều người nghĩ..., nhưng thực ra...`
  - Ý nghĩa: Tự động dùng để tạo tiêu đề động giật mắt (Editorial Hook) trong 3 giây đầu video.
- **Câu hỏi 2 (Câu chào / Lời kết - Outro CTA):** *"Câu chào hoặc lời kết đặc trưng của bạn"*
  - Mặc định gợi ý: `Cùng kiên trì mỗi ngày nhé. Follow để giỏi lên cùng mình!`
  - Ý nghĩa: Tự động chèn vào thẻ kết thúc (End-screen Card) của Timeline CapCut/Premiere.

---

### 📌 [Trụ Cột 5/7] Phong Cách Thị Giác, Font Chữ & Bảng Màu (Typography & Colors)
Cung cấp 3 gói phong cách thiết kế chuẩn điện ảnh đã được Việt hóa 100% (không bao giờ lỗi dấu tiếng Việt):
- **Lựa chọn [1] Editorial Luxe (Tạp chí Sang trọng):**
  - Font tiêu đề chính: `Playfair Display` (Serif cổ điển sang trọng)
  - Font phụ đề: `Be Vietnam Pro` (Sans-serif hiện đại, độ đọc tối ưu)
  - Font điểm nhấn: `Caveat` (Chữ viết tay nghệ thuật)
  - Màu nền chính: `#F2EDE4` (Kem Yến Mạch) | Tương phản: `#212C1B` (Xanh Thông Đậm)
- **Lựa chọn [2] Modern Minimal (Tối giản Hiện đại):**
  - Font tiêu đề chính: `Inter` (Bold, hiện đại như Apple)
  - Font phụ đề: `Be Vietnam Pro`
  - Font điểm nhấn: `Space Grotesk`
  - Màu nền chính: `#FFFFFF` | Tương phản: `#121212`
- **Lựa chọn [3] Gen Z Pop (Năng động & Phá cách):**
  - Font tiêu đề chính: `Poppins` (Tròn trịa, bắt mắt)
  - Font phụ đề: `Be Vietnam Pro`
  - Font điểm nhấn: `Caveat`
  - Màu nền chính: `#FFE600` (Vàng Electric) | Tương phản: `#1E1E24`

---

### 📌 [Trụ Cột 6/7] Sản Phẩm & Phễu Chuyển Đổi Tự Động (ManyChat Automation)
- **Câu hỏi 1 (Sản phẩm chính):** *"Sản phẩm, khóa học hoặc dịch vụ chính bạn cung cấp"*
  - Mặc định: `Khóa Học Dựng Phim AI Triệu View`
- **Câu hỏi 2 (Quà tặng Lead Magnet):** *"Quà tặng miễn phí để hút khách hàng (Ebook, Checklist, Template...)"*
  - Mặc định: `Bản Đồ Kịch Bản Video 1 Triệu View`
- **Câu hỏi 3 (Từ khóa kích hoạt chatbot):** *"Từ khóa kích hoạt chatbot ManyChat (ngăn cách bằng dấu phẩy)"*
  - Mặc định: `LEVI, STUDIO, VIP, INBOX`
  - Ý nghĩa: Tự động tạo hạ tầng Call-To-Action (CTA Overlay) với sticker chỉ dẫn: *"Bình luận 'LEVI' để nhận quà ngay trong DM"*.

---

### 📌 [Trụ Cột 7/7] Sửa Lỗi Phiên Âm Giọng Nói Đặc Thù (Phonetic Auto-Corrections)
Khắc phục triệt để nhược điểm của OpenAI Whisper khi nghe tiếng Anh lẫn tiếng Việt hoặc các thuật ngữ chuyên môn:
- **Cú pháp nhập:** `từ_nghe_nhầm -> từ_đúng (ngăn cách bằng dấu phẩy)`
- **Ví dụ mặc định:** `lê vi -> Levi, s u per -> Super, r e e l s -> Reels, cáp cắt -> CapCut, bờ rê mia -> Premiere`
- **Cơ chế:** Hàm `BrandEngine.apply_phonetic_corrections()` tự động quét toàn bộ phụ đề và kịch bản, thay thế chính xác 100% bằng Regex không phân biệt hoa thường.

---

## 3. Cách Sử Dụng Với Các Mô Hình AI Khác Nhau

| Nền tảng AI | Cách kích hoạt cuộc phỏng vấn Brand Kit |
|---|---|
| **Google Gemini / Antigravity** | Nhắn: *"Hãy phỏng vấn mình để tạo Brand Kit 7 trụ cột"* hoặc gõ `/brand` |
| **Anthropic Claude Code** | Nhắn: *"Chạy phỏng vấn thiết lập nhận diện thương hiệu"* |
| **ChatGPT (Custom GPT)** | Nhắn: *"Thiết lập brand kit cho tôi"* |
| **Terminal / CLI** | Chạy lệnh `python studio.py brand` |

---

## 4. Tự Động Cập Nhật & Lưu Trữ

Sau khi hoàn tất phỏng vấn, tệp `brand-kit.md` tại thư mục gốc dự án sẽ được cập nhật ngay lập tức:
- Mọi video dựng tiếp theo bằng lệnh `autopilot` hoặc `director` sẽ tự động mang màu sắc, font chữ và phong cách mới.
- Không cần cấu hình lại thủ công.
