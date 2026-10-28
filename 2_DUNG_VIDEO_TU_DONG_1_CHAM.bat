@echo off
chcp 65001 > nul
title LEVI SUPER STUDIO v4.0 - DỰNG TỰ ĐỘNG 1-CHẠM (AUTOPILOT)
echo =====================================================================
echo ⚡ LEVI SUPER STUDIO v4.0 — CỖ MÁY DỰNG VIDEO TỰ ĐỘNG 1-CHẠM
echo =====================================================================
echo.
echo 🔍 Đang quét video thô trong thư mục inbox/...
echo.
python studio.py autopilot
echo.
echo =====================================================================
echo 📁 Kiểm tra kết quả video và dự án tại thư mục: outbox/
echo 🎉 Nhấn phím bất kỳ để đóng cửa sổ.
pause > nul
