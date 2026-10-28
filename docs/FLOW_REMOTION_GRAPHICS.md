# ⚛️ LUỒNG REMOTION 60FPS GPU GRAPHICS & KÊNH ALPHA

> Sử dụng sức mạnh của code web (React 18 + Remotion 4) để tạo ra các hiệu ứng đồ họa chuyển động siêu mượt 60fps mà các phần mềm dựng phim truyền thống rất khó làm được.

---

## 1. Vai Trò Của Remotion Trong Levi Super Studio
- Remotion đóng vai trò như một **Xưởng Đồ Họa Cục Bộ (Local Motion Farm)**:
  - Sinh hoạt họa Terminal chạy lệnh gõ chữ sống động.
  - Sinh hoạt họa VS Code biên tập code với highlight cú pháp.
  - Sinh thẻ thống kê số liệu tăng trưởng (Metric Counters).
  - Sinh tiêu đề tạp chí phong cách Editorial ([`EditorialHook.tsx`](../engines/remotion/src/components/EditorialHook.tsx)).
  - Sinh hiệu ứng rung lắc tự nhiên của máy quay cầm tay (*Handheld Camera Drift*).

---

## 2. Xuất Kênh Alpha Trong Suốt (ProRes 4444 / WebM VP9)
Thay vì xuất video nền đen, `engines/remotion/render_alpha.py` xuất ra video có **kênh Alpha trong suốt**:
- **ProRes 4444 (`--codec=prores --pixel-format=yuva444p10le`):** Chuẩn nén cao cấp cho Adobe Premiere Pro và After Effects.
- **WebM VP9 (`--codec=vp9 --pixel-format=yuva420p`):** Chuẩn nén nhẹ nhàng cho CapCut Desktop.

Khi kéo file đồ họa này vào Track trên của Premiere hoặc CapCut, phần nền sẽ tự động trong suốt, chỉ để lại các dòng chữ và thẻ đồ họa bay mượt mà trên nền video người nói.

---

## 3. Xem Trước Bằng Trình Duyệt (Remotion Studio)
Để xem trước và tùy chỉnh đồ họa trên trình duyệt:
```bash
cd engines/remotion
npm install
npm run studio
```
Trình duyệt sẽ mở cổng `http://localhost:3000` để bạn kéo timeline và điều chỉnh tham số Props trực quan.
