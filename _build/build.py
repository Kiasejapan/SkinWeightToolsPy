#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build.py - セクションファイルを番号順に結合して単一 .py を生成
_build/ 内で実行される前提。

使い方:
    python build.py              # 通常ビルド
    python build.py --no-stamp   # リリース日スタンプをスキップ
"""
from __future__ import print_function
import os
import re
import sys
import glob
import shutil
import py_compile
from datetime import date

# === 設定 ===
OUT = "DoraSkinWeightToolsPy.py"
FINAL = os.path.join("..", OUT)
SRC = "src"
BACKUP = "backup"


def main():
    no_stamp = "--no-stamp" in sys.argv
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # --- バックアップ ---
    if not os.path.exists(BACKUP):
        os.makedirs(BACKUP)
    if os.path.exists(FINAL):
        bak = os.path.join(BACKUP, OUT + ".bak")
        shutil.copy2(FINAL, bak)
        print("[INFO] Backup created: {}".format(bak))

    # --- ソースファイル一覧 ---
    src_files = sorted(glob.glob(os.path.join(SRC, "*.txt")))
    if not src_files:
        print("[ERROR] No .txt files found in {}/".format(SRC))
        sys.exit(1)

    print("[INFO] Source files:")
    for f in src_files:
        print("  {}".format(os.path.basename(f)))

    # --- 結合 ---
    combined = []
    for f in src_files:
        with open(f, "r", encoding="utf-8") as fh:
            combined.append(fh.read())
        print("[+] {}".format(os.path.basename(f)))

    merged = "".join(combined)
    print("[INFO] {} files merged.".format(len(src_files)))

    # --- リリース日スタンプ ---
    if not no_stamp:
        stamp = date.today().isoformat()
        merged = re.sub(
            r'(__RELEASE_DATE__\s*=\s*[\'"]).*?([\'"])',
            r'\g<1>{}\2'.format(stamp),
            merged,
            count=1,
        )
        print("[INFO] Release date stamped: {}".format(stamp))

    # --- 一時ファイルに書き出し ---
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(merged)

    # --- 構文チェック ---
    try:
        py_compile.compile(OUT, doraise=True)
    except py_compile.PyCompileError as e:
        print("[ERROR] Syntax check failed: {}".format(e))
        os.remove(OUT)
        sys.exit(1)

    # --- ルートにコピー ---
    shutil.copy2(OUT, FINAL)
    os.remove(OUT)
    print("[OK] Build complete: {}".format(FINAL))


if __name__ == "__main__":
    main()
