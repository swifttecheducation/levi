#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tests/test_syntax_ast.py — Kiểm tra cú pháp AST toàn bộ mã nguồn Python.
Bắt buộc theo giao thức kiểm thử Zero-Error Gate trước khi push/deploy.
"""

import os
import sys
import ast
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestSyntaxAST(unittest.TestCase):
    def test_all_python_files_syntax(self):
        """Quét và biên dịch AST tất cả các file .py trong repo."""
        py_files = []
        for root, dirs, files in os.walk(REPO_ROOT):
            # Bỏ qua các thư mục tạm / cache
            if any(skip in root for skip in [".git", "__pycache__", "node_modules", "vectcut\\template"]):
                continue
            for f in files:
                if f.endswith(".py"):
                    py_files.append(os.path.join(root, f))

        print(f"\n[Syntax Check] Đang kiểm tra AST cho {len(py_files)} file Python...")
        syntax_errors = []

        for fpath in py_files:
            rel_path = os.path.relpath(fpath, REPO_ROOT)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    source = f.read()
                ast.parse(source, filename=rel_path)
            except SyntaxError as e:
                syntax_errors.append(f"{rel_path}:{e.lineno}: {e.msg}")

        if syntax_errors:
            for err in syntax_errors:
                print(f"  ❌ Syntax Error: {err}")
        else:
            print(f"  ✅ Tất cả {len(py_files)} file Python đạt chuẩn cú pháp AST (0 Lỗi).")

        self.assertEqual(len(syntax_errors), 0, f"Tìm thấy {len(syntax_errors)} lỗi cú pháp!")


if __name__ == "__main__":
    unittest.main()
