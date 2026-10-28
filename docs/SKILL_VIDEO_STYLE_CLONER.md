# 🎬 Kỹ Năng Sao Chép Phong Cách Biên Tập Video (Video Style Cloner)

> **Kỹ năng tái sử dụng (Reusable Video Editing Skill) dựa trên 5 công nghệ mũi nhọn:**  
> 1. [blixvip/MotionClone](https://github.com/blixvip/MotionClone): Sao chép quỹ đạo chuyển động camera (Camera Trajectory & Dynamics).  
> 2. [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes): Hoạt họa khai báo, kinetic text và vật lý lò xo (Spring Physics).  
> 3. [cloudai-x/threejs-skills](https://github.com/cloudai-x/threejs-skills): 3D không gian, card xoay quanh người (Orbit Cards), chiều sâu sân khấu.  
> 4. [fogleman/ln](https://github.com/fogleman/ln): Đồ họa vector 3D, đường nét wireframe line-art công nghệ và kiến trúc.  
> 5. [zhuyansen/awesome-claude-video-skills](https://github.com/zhuyansen/awesome-claude-video-skills): Tiêu chuẩn kỹ năng biên tập video thông minh cho AI Agent.

---

## 1. Mục Đích & Khái Niệm

Khi người dùng đưa ra một hoặc nhiều video mẫu (Inspo / Reference Videos):
```text
Study these reference videos:
[PASTE VIDEO LINKS / PATHS]
Analyze their cuts, pacing, captions, zooms, animations and transitions.
Use these resources to choose and set up relevant editing tools:
https://github.com/fogleman/ln
https://github.com/blixvip/MotionClone
https://github.com/heygen-com/hyperframes
https://github.com/cloudai-x/threejs-skills
https://github.com/zhuyansen/awesome-claude-video-skills
- Create a reusable video editing skill that follows this style.
```

Hệ thống **Levi Super Studio v4.0** sẽ:
1. **Quét và phân tích toàn diện:** Nhịp cắt, tiết tấu mở đầu 3s (Hook-Burst), quỹ đạo phóng gần, font chữ phân cấp, hiệu ứng chuyển cảnh.
2. **Trích xuất Dấu Vân Tay Biên Tập (Editing Fingerprint):** Định lượng hóa thành các thông số toán học cụ thể (cuts/giây, độ nảy spring physics, đường cong Bézier).
3. **Sao chép và áp dụng:** Tái tạo chính xác năng lượng và phong cách biên tập đó lên chính video thô của người dùng, xuất ra CapCut Draft, Premiere Pro XML, After Effects JSX và render trực tiếp file MP4.

---

## 2. 5 Trụ Cột Công Nghệ & Ứng Dụng Trong Pipeline

### 1. MotionClone (`blixvip/MotionClone`)
- **Vai trò:** Phân tích nhịp độ camera của video mẫu và sao chép quỹ đạo chuyển động.
- **Ứng dụng:**
  - Tự động tạo các điểm keyframe phóng gần dạng `cubic-bezier(0.25, 0.1, 0.25, 1.0)` với tỉ lệ phóng `1.08x` đến `1.15x`.
  - Phóng nhanh dứt khoát tại các từ khóa giật mắt (Punch Zoom), chậm dần và lùi nhẹ ở các đoạn giải thích dài.

### 2. HyperFrames (`heygen-com/hyperframes`)
- **Vai trò:** Khung hoạt họa khai báo theo thời gian thực (Declarative Motion).
- **Ứng dụng:**
  - Kiểm soát độ nảy chữ Kinetic Typography bằng mô hình lò xo vật lý: `stiffness: 120-180`, `damping: 14-18`.
  - Khóa chặt vùng an toàn TikTok & Instagram Reels: `x: 150 -> 930px`, `y: 270 -> 1620px`.
  - Neo chữ dưới cằm bằng AI YuNet Chin-Lock.

### 3. Three.js Skills (`cloudai-x/threejs-skills`)
- **Vai trò:** Đưa các yếu tố 3D không gian vào video dọc 9:16.
- **Ứng dụng:**
  - Hiệu ứng thẻ thông tin bay theo quỹ đạo hình elip xoay quanh đầu nhân vật (Orbit Cards — Style X1).
  - Khối lập phương hoặc icon 3D bóng lật mở (Style X18).

### 4. LN 3D Vector Engine (`fogleman/ln`)
- **Vai trò:** Vẽ các đường nét vector wireframe, bản vẽ kỹ thuật, sơ đồ kiến trúc dạng line-art.
- **Ứng dụng:**
  - Tạo các đường viền phát sáng, biểu đồ vẽ tay sau lưng vọt lên con số chốt (Style X10).
  - Khung giao diện công nghệ HUD sắc nét không bị vỡ hạt pixel.

### 5. Awesome Claude Video Skills (`zhuyansen/awesome-claude-video-skills`)
- **Vai trò:** Cấu trúc hóa cỗ máy thành Agent Skill chuẩn mực (`SKILL.md`), cho phép Google Gemini, Anthropic Claude Code và ChatGPT gọi tự động qua khẩu lệnh ngôn ngữ tự nhiên.

---

## 3. Cách Sử Dụng Trên CLI

```bash
# 1. Chỉ phân tích và xuất bản báo cáo dấu vân tay của video mẫu:
python studio.py analyze --ref inbox/video_inspo.mp4

# 2. Phân tích video mẫu và áp dụng ngay vào video thô của bạn:
python studio.py clone --ref inbox/video_inspo.mp4 --video inbox/video_chinh.mp4

# 3. Phân tích, áp dụng và render thẳng video MP4 hoàn thiện:
python studio.py clone --ref inbox/video_inspo.mp4 --render
```

---

## 4. Cách Sử Dụng Bằng Hội Thoại Với AI

Người dùng chỉ cần dán link hoặc đường dẫn video và nhắn:
- *"Nghiên cứu video này `inbox/mau_reels.mp4` và phân tích nhịp cắt, pacing, zoom, transitions"*
- *"Hãy sao chép phong cách biên tập của video này và dựng video trong inbox của tôi"*
- *"Dựng video của tôi theo phong cách nhịp nhanh MotionClone"*
