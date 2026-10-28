# CHỈ DẪN VẬN HÀNH LEVI SUPER STUDIO v4.0 (DÀNH CHO TRỢ LÝ AI)

> **Hệ thống điều hành sản xuất video đa kênh tích hợp:**
> CapCut Desktop Native + Adobe Premiere Pro + After Effects + Remotion GPU Studio + Multi-format Carousel & Story.
> **Ngôn ngữ giao tiếp bắt buộc:** 100% Tiếng Việt.

---

## 🛠️ DANH SÁCH KHẨU LỆNH ĐIỀU HÀNH (TRIGGER COMMANDS)

| Khẩu lệnh người dùng nói | Lệnh thực thi tương ứng | Chức năng chi tiết |
| :--- | :--- | :--- |
| **"cài đặt cho mình"** / **"onboarding"** | `python studio.py onboard` | Chạy quy trình hướng dẫn 4 bước thiết lập ban đầu và Brand Kit. |
| **"thiết lập thương hiệu"** / **"brand"** | `python studio.py brand` | Phỏng vấn chuyên sâu 7 trụ cột ADN thương hiệu và bảng sửa lỗi phiên âm. |
| **"thư viện phong cách"** / **"styles"** | `python studio.py styles` | Tra cứu 105 phong cách dựng video, phối mã phong cách và bộ phối mẫu. |
| **"chế độ đạo diễn"** / **"director"** | `python studio.py director` | Luồng khoa học hỏi ý kiến bạn từng bước (Màu sắc, J-Cut, SFX, Export). |
| **"dựng video"** / **"autopilot"** / **"tự dựng đi"** | `python studio.py autopilot` | Quét video thô trong `inbox/`, tự động cắt dead-air, cân bằng âm thanh EBU R128 (-14 LUFS), khóa cằm né mặt bằng YuNet, xuất song song CapCut Desktop và Adobe Premiere/AE. |
| **"xuất premiere"** | `python studio.py premiere -v <video>` | Tạo file Timeline FCPXML / Premiere XML chuẩn mở trực tiếp trong Adobe Premiere Pro với đầy đủ track video, B-roll và audio riêng biệt. |
| **"xuất after effects"** | `python studio.py ae -t "<câu_hook>"` | Tạo kịch bản ExtendScript `.jsx` tích hợp biểu thức đàn hồi Inertial Bounce cho After Effects. |
| **"cho tôi xem beat sheet"** | `python studio.py beat-sheet -v <video>` | Trích xuất các keyframe quan trọng và ghép thành file ảnh storyboard `beat_sheet.jpg` để duyệt trước khi render video. |
| **"tạo carousel"** | `python studio.py carousel -H "<tiêu_đề>"` | Sinh trọn bộ slide ảnh vuốt ngang Instagram Carousel (1080x1350) chuẩn 4:5. |
| **"kiểm tra hệ thống"** / **"status"** | `python studio.py status` | Kiểm tra tình trạng Brand Kit, các font chữ và video đang chờ trong `inbox/`. |

---

## 🎯 QUY TẮC BẢO VỆ CHẤT LƯỢNG (QUALITY PROTOCOL)
1. **Âm thanh tuyệt đối không vượt ngưỡng:** Luôn duy trì mức -14 LUFS cho Reels/TikTok hoặc -16 LUFS cho YouTube, True Peak không quá -1.5 dBTP.
2. **Không che mặt người nói:** Mọi phụ đề hoặc thẻ chữ phải neo dưới xương quai xanh (Collar Line) hoặc vùng 1/3 an toàn đã được tính toán bởi thuật toán YuNet Chin-Lock.
3. **Phông chữ chuẩn tiếng Việt:** Chỉ dùng các phông chữ có sẵn trong `assets/fonts/` (Playfair Display, Be Vietnam Pro, Caveat, Inter, Poppins) để đảm bảo không bị lỗi ô vuông (tofu) hay nhảy dấu.
