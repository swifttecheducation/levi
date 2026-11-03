#!/bin/bash
# Khởi động cài đặt và onboarding trên macOS / Linux
# Dùng môi trường ảo .venv để không lỗi "externally-managed-environment" (PEP 668) trên macOS/Homebrew & Linux mới.
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install -r requirements.txt --quiet
.venv/bin/python studio.py onboard
