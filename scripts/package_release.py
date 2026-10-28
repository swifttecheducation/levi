#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/package_release.py — Đóng gói sản phẩm thương mại LEVI SUPER STUDIO v4.0.
Tạo gói nén ZIP chuẩn thương mại cho khách hàng:
- Loại bỏ toàn bộ file rác (.git, __pycache__, .pytest_cache, temp files).
- Giữ nguyên toàn bộ mã nguồn, model AI, font chữ Việt hóa, file chạy nhanh .bat, .sh, tài liệu cẩm nang.
- Đóng gói thành: dist/LEVI_SUPER_STUDIO_v4.0_COMMERCIAL.zip
"""

import os
import sys
import zipfile
import shutil

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(REPO_ROOT, "dist")
ZIP_NAME = "LEVI_SUPER_STUDIO_v4.0_COMMERCIAL.zip"
ZIP_PATH = os.path.join(DIST_DIR, ZIP_NAME)

EXCLUDE_DIRS = {
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "venv",
    ".venv",
    "env",
    "dist"
}

EXCLUDE_EXTS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".DS_Store"
}

EXCLUDE_FILES = {
    "Thumbs.db",
    "desktop.ini"
}


def clean_pycache():
    """Xóa sạch các thư mục __pycache__ trước khi đóng gói."""
    count = 0
    for root, dirs, files in os.walk(REPO_ROOT, topdown=False):
        for d in dirs:
            if d == "__pycache__":
                full_path = os.path.join(root, d)
                shutil.rmtree(full_path, ignore_errors=True)
                count += 1
    return count


def package_release() -> str:
    print("\n" + "=" * 65)
    print("📦 ĐÓNG GÓI PHÁT HÀNH THƯƠNG MẠI — LEVI SUPER STUDIO v4.0")
    print("=" * 65)

    pycache_cleaned = clean_pycache()
    print(f"🧹 Đã dọn dẹp sạch {pycache_cleaned} thư mục __pycache__.")

    os.makedirs(DIST_DIR, exist_ok=True)
    if os.path.exists(ZIP_PATH):
        os.remove(ZIP_PATH)

    file_count = 0
    total_uncompressed_bytes = 0

    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(REPO_ROOT):
            # Lọc bỏ thư mục loại trừ
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                ext = os.path.splitext(file)[1].lower()
                if ext in EXCLUDE_EXTS:
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, REPO_ROOT)

                # Bọc trong thư mục gốc LEVI_SUPER_STUDIO
                archive_name = os.path.join("LEVI_SUPER_STUDIO", rel_path)
                zipf.write(full_path, archive_name)
                file_count += 1
                total_uncompressed_bytes += os.path.getsize(full_path)

    zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)
    raw_size_mb = total_uncompressed_bytes / (1024 * 1024)

    print(f"✅ Đã đóng gói thành công {file_count} tệp tin.")
    print(f"📁 Tệp gói hoàn thiện : {ZIP_PATH}")
    print(f"📊 Kích thước gói nén : {zip_size_mb:.2f} MB (Kích thước gốc: {raw_size_mb:.2f} MB)")
    print("=" * 65 + "\n")
    return ZIP_PATH


if __name__ == "__main__":
    package_release()
