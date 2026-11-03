#!/bin/bash
# Dựng video tự động 1-chạm trên macOS / Linux (dùng .venv do run_cai_dat.sh tạo nếu có)
cd "$(dirname "$0")"

if [ -x ".venv/bin/python" ]; then
    PY=".venv/bin/python"
else
    PY="python3"
fi
"$PY" studio.py autopilot "$@"
