"""
AI 生圖（Google Gemini 生圖模型，走 OpenAI 相容端點）—— 屏北高中教師研習版

用法：
  python -X utf8 draw.py "一隻穿西裝的龍蝦，扁平向量插畫風"
  python -X utf8 draw.py "研習海報主視覺" --size 1536x1024 --name poster
  python -X utf8 draw.py --probe          # 只檢查有沒有金鑰，不生圖、不花錢

金鑰：GEMINI_API_KEY
  1. 系統環境變數 GEMINI_API_KEY
  2. 當前工作目錄的 .env
  3. 本機金鑰檔 ~/.claude/_secrets/GEMINI_API_KEY.key
     （Codex Desktop 使用者放 ~/.agents/_secrets/GEMINI_API_KEY.key 亦可）

⚠️ 重要：Gemini 的「生圖模型」不在免費層
  在 aistudio.google.com 申請的免費金鑰可以用文字模型，但生圖配額是 0，
  打下去會回 HTTP 429。那不是金鑰壞掉、也不是這支程式有問題，
  是那個 Google Cloud 專案還沒開啟帳單。

  不想付錢又想要 AI 插圖，正確做法是：
  直接到 aistudio.google.com 或 Gemini App 的「網頁介面」生圖（有免費額度），
  存成檔案後自己放進簡報。網頁免費、API 要錢，這兩件事常被搞混。

離開代碼（呼叫端請依此判斷）：
  0  成功
  3  找不到金鑰 —— 這不是錯誤，是「這台電腦沒有設定生圖」。
     呼叫端（ppsh-soil-* 系列技能）收到 3 時，應改走純向量版面，不要中斷整份工作。
  1  其他錯誤（參數錯、API 回錯。429 配額不足也走這裡，訊息會說明原因）

輸出：
  預設放在「當前工作目錄/slides/generated/」
  若該目錄不存在，會建立「./generated/」
"""

import os
import sys
import base64
import argparse
from pathlib import Path
from datetime import datetime

# 沒有金鑰時的專用離開代碼；呼叫端據此改走向量版面，而不是讓整份工作失敗
EXIT_NO_KEY = 3

# 實測 2026-09-16：OpenAI 相容的 images/generations 端點只認得
# gemini-2.5-flash-image 與 gemini-3-pro-image-preview；
# gemini-3.1-flash-image 雖然出現在 /models 清單，走這個端點會回 404。
MODEL = "gemini-2.5-flash-image"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
KEY_ENV = "GEMINI_API_KEY"

DEFAULT_SIZE = "1024x1024"
DEFAULT_N = 1


def load_env_from_file(path: Path):
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def find_key():
    """找得到就回金鑰，找不到回 None。"""
    load_env_from_file(Path.cwd() / ".env")
    key = os.getenv(KEY_ENV)
    if key:
        return key.strip()
    # 環境變數沒有，才讀本機金鑰檔（Claude Code 與 Codex 的資料夾都找一遍）
    for base in (".claude", ".agents"):
        f = Path.home() / base / "_secrets" / f"{KEY_ENV}.key"
        if f.exists():
            key = f.read_text(encoding="utf-8-sig").strip()
            if key:
                return key
    return None


def require_key():
    key = find_key()
    if key:
        return key
    # 找不到金鑰不是「壞掉」，是「這台電腦沒設定生圖」——講清楚該怎麼辦再結束
    print(
        "[no-key] 這台電腦沒有設定 GEMINI_API_KEY，生圖這一步跳過（不是錯誤）。\n"
        "         想要 AI 插圖，建議先用免費的做法：\n"
        "           到 aistudio.google.com 或 Gemini App 的網頁介面生圖，存檔後自己放進簡報。\n"
        "         真的要用 API（會計費，且專案必須先開啟帳單）：\n"
        "           把金鑰存成 ~/.claude/_secrets/GEMINI_API_KEY.key\n"
        "         ⚠️ 金鑰不要貼進和 AI 的對話裡。",
        file=sys.stderr,
    )
    sys.exit(EXIT_NO_KEY)


def resolve_outdir(user_outdir):
    if user_outdir:
        return Path(user_outdir)
    cwd = Path.cwd()
    slides_dir = cwd / "slides"
    if slides_dir.exists():
        return slides_dir / "generated"
    return cwd / "generated"


def draw(key, prompt, size, n, name, outdir):
    from openai import OpenAI
    outdir.mkdir(parents=True, exist_ok=True)
    client = OpenAI(api_key=key, base_url=BASE_URL)
    print(f"畫圖中（{MODEL}, {size}, n={n}） -> {outdir}", file=sys.stderr)
    try:
        result = client.images.generate(
            model=MODEL, prompt=prompt, size=size, n=n, response_format="b64_json"
        )
    except Exception as e:
        msg = str(e)
        if "429" in msg or "quota" in msg.lower():
            # 最常見的狀況，直接翻成人話，免得老師以為是金鑰打錯
            print(
                "錯誤：API 回 429（配額不足）。\n"
                "      最可能的原因：這把金鑰所屬的 Google Cloud 專案還沒開啟帳單，\n"
                "      而 Gemini 的生圖模型不在免費層（免費額度是 0）。\n"
                "      免費替代方案：到 aistudio.google.com 的網頁介面生圖，再自己存檔放進簡報。",
                file=sys.stderr,
            )
            sys.exit(1)
        raise

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []
    for i, item in enumerate(result.data):
        suffix = f"_{i + 1}" if n > 1 else ""
        out_path = outdir / f"{name}_{stamp}{suffix}.png"
        b64 = getattr(item, "b64_json", None)
        if b64:
            out_path.write_bytes(base64.b64decode(b64))
        else:
            url = getattr(item, "url", None)
            if not url:
                sys.exit("錯誤：API 回應既沒有 b64_json 也沒有 url")
            import urllib.request
            with urllib.request.urlopen(url) as resp:
                out_path.write_bytes(resp.read())
        saved.append(out_path)
        print(f"  [OK] {out_path}")
    return saved


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="*")
    parser.add_argument("--probe", action="store_true",
                        help="只檢查有沒有金鑰：有就印出 gemini 並回 0，沒有回 3")
    parser.add_argument("--size", default=DEFAULT_SIZE)
    parser.add_argument("--n", type=int, default=DEFAULT_N)
    parser.add_argument("--name", default="image")
    parser.add_argument("--outdir", default=None)
    args = parser.parse_args()

    # --probe：技能在生圖「之前」先問一句「這台電腦能生圖嗎」，
    # 回 3 就整份改走向量版面，不要等跑到一半才失敗
    if args.probe:
        require_key()
        print("gemini")
        print("[warn] 找得到金鑰不等於生得出圖：若專案未開啟帳單，生圖會回 429。",
              file=sys.stderr)
        sys.exit(0)

    if not args.prompt:
        parser.error("請給提示詞（或用 --probe 只做金鑰檢查）")

    key = require_key()
    draw(key, " ".join(args.prompt), args.size, args.n,
         args.name, resolve_outdir(args.outdir))


if __name__ == "__main__":
    main()
