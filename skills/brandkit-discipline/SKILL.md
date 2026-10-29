---
name: brandkit-discipline
description: "Kỷ luật tuân thủ Brand Kit tuyệt đối: Không bịa icon AI sến súa, bám sát mẫu khách đưa 100% và chỉ render khi kiểm thử đạt 100% chuẩn xác."
---

# 🛡️ BRAND KIT DISCIPLINE & QUALITY GATE

> **Kỷ luật cốt lõi của Hệ thống Xưởng Dựng Phim AI:**
> Đảm bảo mọi video xuất xưởng đều chuẩn nhận diện thương hiệu, không mang dấu vết "AI rẻ tiền", sao chép chính xác 100% mẫu tham chiếu của khách hàng và chỉ được bấm nút render khi đã vượt qua toàn bộ các bài kiểm thử chất lượng.

---

## 📌 ĐIỀU 1: LUÔN TUÂN THỦ BRAND KIT (BRAND KIT FIRST)

Mọi quyết định về mặt hình ảnh, chữ viết, màu sắc đều phải bắt đầu từ `brand-kit.md` và `product/creative-vault/user-style.json`:

1. **Font chữ chuẩn hóa (100% CapCut Free & Việt hóa hoàn hảo):**
   - **Tiêu đề chính (Headline / Takeover):** `Playfair Display` (`PlayfairDisplay-VF.ttf`) — Serif sang trọng, đẳng cấp.
   - **Phụ đề chạy chữ (Captions / Read-along):** `Be Vietnam Pro` (`BeVietnamPro-Medium.ttf`) — Dễ đọc, nét tròn trịa.
   - **Nét chữ ký / Điểm nhấn (Accent / Thought bubble):** `Caveat` (`Caveat-VF.ttf`) — Viết tay tự nhiên.
2. **Bảng màu chuẩn (Palette):**
   - Chỉ dùng các mã màu đã quy định trong Brand Kit (ví dụ với *Editorial Luxe*: `#F2EDE4` Kem Yến Mạch, `#212C1B` Xanh Thông Đậm, `#FFADBF` Hồng Phấn, `#720000` Đỏ Rượu Vang).
   - **TUYỆT ĐỐI KHÔNG** tự ý dùng màu neon, tím xanh cyber AI, hoặc gradient sến súa không rõ nguồn gốc.
3. **Vị trí bố cục an toàn (Safe Zones):**
   - **Hook Title:** Luôn đặt ở khoảng trống trên đầu (`y = 0.72` headroom), không đè lên mặt người nói.
   - **Phụ đề (Captions):** Luôn khóa dưới cằm (`chin-lock`, `y = -0.65` đến `-0.68`), tránh bị thanh menu TikTok / Reels / Shorts che khuất.

---

## 🚫 ĐIỀU 2: CẤM ICON AI SẾN SÚA & KHÔNG TÙY TIỆN BỊA ĐẶT (ANTI-AI SLOP)

Khách hàng tìm đến dịch vụ chuyên nghiệp vì họ muốn video trông như do **đạo diễn & editor cao cấp** dựng, chứ không phải một công cụ AI tạo rác nội dung:

1. **Tuyệt đối cấm:**
   - Cấm chèn các icon 3D bóng bẩy, emoji hoạt hình sến súa ("trông rất AI").
   - Cấm các hiệu ứng sticker nổi lơ lửng vô nghĩa.
   - Cấm tự ý bịa đặt số liệu, trích dẫn, hoặc tính năng mà khách hàng không yêu cầu.
2. **Ưu tiên:**
   - Dùng nghệ thuật chữ (Typography) tinh tế, có trọng lượng và khoảng thở.
   - Dùng thẻ nội dung tối giản (Clean cards), giao diện ứng dụng thực tế (Real UI mockups), hoặc B-roll chân thực.
   - Mọi yếu tố đồ họa xuất hiện trên màn hình phải có lý do phục vụ nội dung câu nói, không được thêm vào cho "đỡ trống".

---

## 🎯 ĐIỀU 3: BÁM SÁT MẪU CỦA KHÁCH Y HỆT 100% (EXACT REFERENCE REPLICATION)

Khi khách hàng cung cấp một video mẫu (link Facebook Reel, Instagram Reel, TikTok, hoặc file mp4 tham chiếu):

1. **Đo đạc và phân tích chính xác:**
   - Phân tích nhịp cắt đến từng mili-giây (`FFT cross-correlation` hoặc `scene peak detection`).
   - Sao chép chính xác tỷ lệ phóng to (Zoom punch-in: 100% -> 115% -> 120%).
   - Đồng bộ nhịp cắt âm thanh và hiệu ứng âm thanh (SFX Whoosh, Pop, Click, Snap) đúng từng khung hình (frame-accurate).
2. **Không tự ý sáng tác lệch mẫu:**
   - Khách muốn nhịp nhanh (Rapid-fire) thì dựng dồn dập.
   - Khách muốn tối giản sang trọng (Editorial) thì giữ nhịp thở thoáng, tinh tế.
   - Không được tự ý thay đổi cấu trúc mà không có sự đồng ý của khách.

---

## 🛑 ĐIỀU 4: CỔNG KIỂM SOÁT ZERO-ERROR TRƯỚC KHI RENDER (PRE-RENDER GATE)

**NGUYÊN TẮC BẤT DI BẤT DỊCH:** Không bao giờ bấm render nếu video chưa đạt chuẩn hoặc còn nghi ngờ sai lệch. Làm và sửa đến bao giờ chuẩn 100% mới thôi.

Trước khi xuất file:
1. **Kiểm tra cú pháp (Syntax Check):** `python -m py_compile` tất cả các script liên quan.
2. **Kiểm tra đồng bộ (EDL Alignment Check):** Đảm bảo nhịp cắt không bị lệch tiếng, không bị giật khung hình (0 drop frames).
3. **Kiểm tra chuẩn âm thanh (Loudness Gate):** Chuẩn -16 LUFS (Mean: -18 to -19 dB, Max: < -1.5 dBFS).
4. **Kiểm tra CapCut Draft:** Xác nhận `draft_content.json` nạp đủ tracks, đúng phân giải 1080x1920, và ghim đứng đầu trong `root_meta_info.json`.
5. **Báo cáo kết quả kiểm thử:** Luôn trình bày bảng kết quả kiểm thử (Verification Evidence) rõ ràng cho người dùng.
