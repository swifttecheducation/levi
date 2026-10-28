---
name: video-style-cloner
description: Study reference video links or files to analyze cuts, pacing, captions, zooms, animations, and transitions, and create a cloned reusable video editing recipe using modern tools (MotionClone camera motion, HyperFrames declarative animations, Three.js 3D elements, and LN vector wireframes). Use when the user asks to analyze reference videos, clone an editing style, or "edit like this video".
---

# Video Style Cloner — Kỹ Năng Phân Tích & Sao Chép Phong Cách Video

Kỹ năng này biến yêu cầu: *"Hãy nghiên cứu video mẫu này và dựng video của tôi theo phong cách đó"* thành một quy trình kỹ thuật chuẩn xác, khoa học và có thể tái sử dụng cho mọi video.

Hệ thống kết hợp sức mạnh từ 5 công nghệ biên tập tiên tiến:
- **`blixvip/MotionClone`**: Trích xuất và sao chép quỹ đạo chuyển động camera (Pan, Tilt, Bézier Ease-Out Zoom).
- **`heygen-com/hyperframes`**: Thiết kế chuyển động khai báo (Declarative Motion), vật lý lò xo (Spring Physics), và kiểm soát vùng an toàn (Safe Zones).
- **`cloudai-x/threejs-skills`**: Hiệu ứng 3D không gian, card bay quanh nhân vật (Orbit Cards), chiều sâu sân khấu.
- **`fogleman/ln`**: Đồ họa vector 3D, đường nét wireframe line-art kiến trúc và công nghệ.
- **`zhuyansen/awesome-claude-video-skills`**: Tiêu chuẩn tổ chức kỹ năng video thông minh cho AI Agent.

---

## 🚀 Quy Trình 4 Bước Thực Hiện

### Bước 1: Tiếp nhận Video Mẫu (Study Reference Videos)
Khi người dùng cung cấp link video hoặc đường dẫn file:
- Người dùng gõ: *"Nghiên cứu video này: `<đường_dẫn_hoặc_link>`"* hoặc chạy:
  ```bash
  python studio.py clone --ref <đường_dẫn_video_mẫu>
  ```
- Nếu là link mạng xã hội, hệ thống tải video về thư mục tạm để phân tích hình ảnh và âm thanh.

### Bước 2: Phân Tích Dấu Vân Tay Biên Tập (Editing Fingerprint)
Cỗ máy [`core/style_cloner.py`](core/style_cloner.py) tự động quét toàn bộ video mẫu để đo lường 5 yếu tố then chốt:
1. **Cuts & Cadence:** Số điểm chuyển cảnh trên giây (cuts/sec), độ dài trung bình mỗi cú máy.
2. **Hook-Burst Pacing:** Tần suất cắt nhanh trong 3 giây đầu để giật mắt người xem.
3. **Zooms & Motion:** Nhịp phóng gần (Punch Zoom vs Bézier Zoom) lấy khuôn mặt làm tâm (Face-Centered).
4. **Captions & Safe Zones:** Vị trí phụ đề (dưới xương quai xanh né mặt), font chữ phân cấp (Hook to, Caption gọn), từ khóa đổi màu.
5. **Animations & Transitions:** Hiệu ứng thẻ nổi, đường viền vẽ tay, chia đôi màn hình minh họa.

### Bước 3: Xuất Bản Kế Hoạch Sao Chép (Cloned Style Recipe)
AI Agent tạo ra bản kế hoạch chi tiết định dạng Markdown bao gồm:
- Chỉ số nhịp độ (Pacing Energy): `Fast Burst`, `Medium Dynamic`, hoặc `Calm Editorial`.
- Quỹ đạo MotionClone: Tỉ lệ zoom `1.08x` - `1.15x`, đường cong `cubic-bezier(0.25, 0.1, 0.25, 1.0)`.
- Bộ mã phong cách tương ứng từ Thư viện 105 phong cách (ví dụ: `H1 + C1 + L2 + X5 + M6 + G1`).

### Bước 4: Tái Áp Dụng Lên Video Của Người Dùng
Áp dụng công thức vừa sao chép vào video thô của người dùng trong thư mục `inbox/`:
```bash
python studio.py clone --ref inbox/mau_inspo.mp4 --video inbox/video_cua_toi.mp4
```
Hệ thống sẽ tự động xuất trọn bộ:
- Dự án **CapCut Desktop** (rời track, chỉnh sửa trực tiếp).
- Timeline **Adobe Premiere Pro XML**.
- Kịch bản **After Effects JSX** (nảy lò xo Inertial Bounce).
- Bản render hoàn thiện **MP4** trong `outbox/video_hoan_thien/`.

---

## 🔒 Nguyên Tắc Bất Biến (Ethical Cloning)
1. **Học PHONG CÁCH & NHỊP ĐỘ, KHÔNG SAO CHÉP NỘI DUNG:** Chúng ta học cấu trúc cắt gọt, tiết tấu và visual của video mẫu, nhưng câu chuyện, giọng nói và giá trị truyền tải luôn là 100% của người dùng.
2. **Luôn kiểm soát vùng an toàn (Safe Zone):** Tọa độ text luôn nằm trong vùng an toàn TikTok/Reels và neo dưới cằm bằng thuật toán AI YuNet Chin-Lock.
