# 🎬 LUỒNG ĐẠO DIỄN KHOA HỌC TỪNG BƯỚC (INTERACTIVE DIRECTOR MODE)

> **Triết lý:** Dựng phim không phải là một chuỗi hành động máy móc. Tại mỗi khâu sáng tạo then chốt, hệ thống dừng lại, báo cáo dữ liệu phân tích và hỏi ý kiến người dùng: Bạn có muốn dùng tính năng này không, muốn tinh chỉnh gì hay muốn bỏ qua để sang bước tiếp theo?

---

## 🏛️ 5 BƯỚC KHOA HỌC TRONG LUỒNG TƯƠNG TÁC

### 📍 BƯỚC 1/5: TỐI ƯU NHỊP CẮT ĐIỆN ẢNH & KHOẢNG LẶNG (PACING & J-CUT)
- **Hệ thống phân tích:** Đọc transcript, đo đạc từng khoảng im lặng giữa các câu.
- **Điểm thông minh:** Tự động phân biệt giữa *"Dead-Air vô nghĩa"* và *"Khoảng lặng kịch tính (Dramatic Pause)"* sau câu hỏi hoặc câu khẳng định mạnh.
- **Câu hỏi cho bạn:**
  > *"Bạn có muốn bật J-Cut (âm thanh cất lên trước 120ms) và giữ lại các khoảng lặng kịch tính? (y: Bật / n: Cắt thẳng / s: Bỏ qua)"*
- **Tác dụng:** Giúp câu nói tự nhiên, truyền cảm, loại bỏ cảm giác nói dồn dập máy móc.

---

### 📍 BƯỚC 2/5: QUẢN LÝ MÀU SẮC ĐIỆN ẢNH (CINEMA COLOR SCIENCE)
- **Hệ thống phân tích:** Nhận diện không gian màu của video (`Apple Log`, `Sony S-Log3`, `HDR` hoặc `Rec.709`).
- **Câu hỏi cho bạn:**
  > *"Chọn phong cách màu bạn muốn áp dụng:*  
  > *[1] Teal & Orange (Hollywood hiện đại, da sáng rực rỡ)*  
  > *[2] Kodak Film Emulation (Ấm áp, hoài cổ tạp chí)*  
  > *[3] Clean & Crisp Corporate (Trong trẻo, tự nhiên)*  
  > *[s] Giữ nguyên màu gốc (Bỏ qua)"*
- **Tác dụng:** Biến video quay bằng điện thoại hoặc máy ảnh thành tone màu điện ảnh chuẩn rạp chỉ với 1 phím bấm.

---

### 📍 BƯỚC 3/5: KHÓA CẰM NÉ MẶT (CHIN-LOCK) & CHUYỂN ĐỘNG BEZIER
- **Hệ thống phân tích:** Mạng nơ-ron OpenCV YuNet quét tọa độ cằm và góc nghiêng đầu từng frame, tính toán vùng an toàn neo chữ dưới xương quai xanh (Y ~ 1320px).
- **Câu hỏi cho bạn:**
  > *"Bật gia tốc chuyển động Bezier Ease-out và mô phỏng Motion Blur 180° khi zoom cận? (y/n/s)"*
- **Tác dụng:** Cú zoom cận mặt (Punch-In Zoom) sẽ lướt mượt mà có độ mờ chuyển động nhẹ, không gây mỏi mắt người xem.

---

### 📍 BƯỚC 4/5: THIẾT KẾ ÂM THANH & B-ROLL THEO TỪ KHÓA (SEMANTIC FOLEY & VISUAL)
- **Hệ thống phân tích:** Quét toàn bộ ngữ nghĩa bài nói để phát hiện các điểm nhấn (Tài chính, Đột phá, Chuyển hướng, Kêu gọi hành động).
- **Câu hỏi cho bạn:**
  > *"Tìm thấy N điểm nhấn ngữ nghĩa. Tự động chèn các hiệu ứng âm thanh Foley SFX và B-Roll tương ứng? (y/n/s)"*
- **Tác dụng:** Tự động lồng tiếng 'ka-ching', chuông ý tưởng 'ting', chuyển cảnh 'whoosh' đúng thời điểm từ khóa vang lên.

---

### 📍 BƯỚC 5/5: LỰA CHỌN NỀN TẢNG XUẤT BẢN (EXPORT DISPATCHER)
- **Câu hỏi cho bạn:**
  > *"Chọn nền tảng bạn muốn xuất:*  
  > *[1] Chỉ xuất dự án CapCut Desktop (Chỉnh nhanh trên laptop/mobile)*  
  > *[2] Chỉ xuất Adobe Premiere Pro XML & After Effects JSX (Chuẩn điện ảnh)*  
  > *[3] Xuất TRỌN BỘ CẢ HAI + Storyboard Beat Sheet + Carousel (Khuyến nghị)"*
- **Tác dụng:** Tối ưu hóa đầu ra theo đúng mục đích sử dụng của bạn tại thời điểm đó.

---

## 💻 CÁCH KHỞI CHẠY

```bash
# 1. Chế độ tương tác hỏi từng bước (Khuyến nghị cho Editor)
python studio.py director

# 2. Hoặc chỉ định video cụ thể
python studio.py director --video "inbox/my_video.mp4"

# 3. Chạy tự động các lựa chọn tối ưu nhất mà không cần hỏi
python studio.py director --auto
```
