@echo off
chcp 65001 > nul
title LEVI SUPER STUDIO v4.0 - KHỞI ĐỘNG & THIẾT LẬP BAN ĐẦU
echo =====================================================================
echo 🚀 LEVI SUPER STUDIO v4.0 — QUY TRÌNH THIẾT LẬP & CHẨN ĐOÁN MÔI TRƯỜNG
echo =====================================================================
echo.
echo [1/3] Đang kiểm tra Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ LỖI: Chưa tìm thấy Python trên máy tính của bạn!
    echo 👉 Vui lòng tải và cài đặt Python từ: https://www.python.org/
    echo 💡 Nhớ tích chọn vào ô: "Add Python to PATH" khi cài đặt!
    echo.
    pause
    exit /b 1
)

echo [2/3] Đang cài đặt / đồng bộ các thư viện cần thiết...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Có cảnh báo khi cài thư viện. Đang tiếp tục chạy...
)

echo.
echo [3/3] Bắt đầu quy trình phỏng vấn & chẩn đoán hệ thống...
echo.
python studio.py onboard
echo.
echo =====================================================================
echo 🎉 Hoàn tất! Nhấn phím bất kỳ để đóng cửa sổ.
pause > nul
