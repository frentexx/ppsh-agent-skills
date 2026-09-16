#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTML → PNG 渲染器（headless Chrome / Edge）

用法:
  python -X utf8 render.py 圖檔.html --out 輸出.png
  python -X utf8 render.py 圖檔.html --out 輸出.png --size 1080x1440 --scale 2

設計重點:
- 不生圖、不呼叫任何 API，純粹把已渲染的網頁拍成點陣圖
- 中文路徑用 pathlib.as_uri() 轉 file:// URI，自動百分比編碼
- 帶 ?shot=1 給頁面，讓頁面自己隱藏「下載 PNG」按鈕等螢幕限定 UI
- --virtual-time-budget 等 Google Fonts 與 CSS 載完才快門，避免拍到未套字體的版本
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def find_browser() -> str:
    for p in CANDIDATES:
        if os.path.isfile(p):
            return p
    sys.exit("找不到 Chrome 或 Edge。請確認其中一個已安裝，或用 --browser 指定 exe 路徑。")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html", help="來源 HTML 檔")
    ap.add_argument("--out", required=True, help="輸出 PNG 路徑")
    ap.add_argument("--size", default="1536x1024", help="版面尺寸 WxH（預設 1536x1024 橫式）")
    ap.add_argument("--scale", type=int, default=2, help="像素密度倍率（預設 2 = 高 DPI）")
    ap.add_argument("--wait", type=int, default=12000, help="等待毫秒數，讓字體與 CSS 載完")
    ap.add_argument("--browser", default=None, help="自訂瀏覽器 exe 路徑")
    ap.add_argument("--transparent", action="store_true",
                    help="透明背景（把 SVG 幾何圖插進 pptx／簡報時用，避免壓到底色）")
    a = ap.parse_args()

    src = Path(a.html).resolve()
    if not src.is_file():
        sys.exit(f"找不到來源檔：{src}")
    out = Path(a.out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    try:
        w, h = (int(v) for v in a.size.lower().split("x"))
    except ValueError:
        sys.exit("--size 格式錯誤，應為 1536x1024 這種形式")

    browser = a.browser or find_browser()
    # ?shot=1 讓頁面隱藏螢幕限定 UI；as_uri() 處理中文路徑
    url = src.as_uri() + "?shot=1"

    cmd = [
        browser, "--headless", "--disable-gpu", "--hide-scrollbars",
        f"--force-device-scale-factor={a.scale}",
        f"--window-size={w},{h}",
    ]
    if a.transparent:
        # 00000000 = 全透明；頁面本身的 body 背景也必須留空才看得到效果
        cmd.append("--default-background-color=00000000")
    cmd += [
        f"--virtual-time-budget={a.wait}",
        f"--screenshot={out}",
        url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")

    if not out.is_file():
        sys.exit(f"渲染失敗，沒有產生檔案。\nstderr:\n{proc.stderr[-2000:]}")

    # 驗收：確認尺寸真的等於 期望值 × scale，並回報檔案大小
    try:
        from PIL import Image
        with Image.open(out) as im:
            got_w, got_h = im.size
        want = (w * a.scale, h * a.scale)
        flag = "OK" if (got_w, got_h) == want else f"注意：預期 {want[0]}x{want[1]}"
        print(f"[{flag}] {out}")
        print(f"     {got_w}x{got_h} px · {out.stat().st_size/1024/1024:.2f} MB")
    except ImportError:
        print(f"[OK] {out} · {out.stat().st_size/1024/1024:.2f} MB（未安裝 Pillow，略過尺寸驗收）")


if __name__ == "__main__":
    main()
