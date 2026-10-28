@echo off
chcp 65001 > nul
title LEVI SUPER STUDIO v4.0 - CHẾ ĐỘ ĐẠO DIỄN KHOA HỌC (INTERACTIVE DIRECTOR)
echo =====================================================================
echo 🎬 LEVI SUPER STUDIO v4.0 — CHẾ ĐỘ ĐẠO DIỄN TƯƠNG TÁC 5 BƯỚC
echo =====================================================================
echo.
echo Hệ thống sẽ hỏi ý kiến bạn từng bước: J-Cut, Màu sắc, Khóa cằm, SFX, Export.
echo.
python studio.py director
echo.
echo =====================================================================
echo 📁 Kiểm tra kết quả tại thư mục: outbox/
echo 🎉 Nhấn phím bất kỳ để đóng cửa sổ.
pause > nul
