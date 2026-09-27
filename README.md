# 屏北高中 Agent Skill 懶人包

> 給屏北高中教師研習用的 AI Agent 技能（Skills）。
> 每個技能都是一份純文字說明書，AI 讀了就照著做——**不是程式，不需要會寫程式。**
>
> ✅ 適用：**Codex Desktop**、**Claude Code**（兩者都支援 Skills）

**不用打指令就能安裝**：跳到下方「[安裝：一段話交給 AI Agent](#安裝一段話交給-ai-agent)」，複製那段話貼給你的 AI Agent 就好。

想了解每個工具在做什麼，看姊妹 repo：👉 **[屏北高中 Agent 基本功懶人包](https://github.com/frentexx/ppsh-agent-basics-packs)**

---

## 技能清單

| 技能 | 你怎麼叫它 | 它會做什麼 | 對應教材 |
|---|---|---|---|
| `ppsh-project-init` | 「初始化專案」 | 建立 `AGENTS.md`（專案藍圖）與 `handoff.md`（交接檔），並放一行 `@AGENTS.md` 的 `CLAUDE.md` 讓 Claude Code 自動讀藍圖 | A5 |
| `ppsh-startup` | 「開工」 | 讀兩份檔案，回報上次做到哪、下一步 | A5 |
| `ppsh-shutdown` | 「收工」 | 把今天進度寫進交接檔，提醒雲端硬碟同步 | A5 |
| `ppsh-office-reader` | 「幫我讀這份 Word／PDF／簡報／Excel」 | 把檔案轉成文字再閱讀，不改原檔 | A3、A4 |

### 產出技能（速成版 S2 使用）

| 技能 | 你怎麼叫它 | 產出 | 要 API 金鑰嗎 |
|---|---|---|---|
| `ppsh-soil-infographic` | 「做一張圖卡」「做懶人包」「一張圖看懂」 | **單頁 PNG**，發 LINE 群用 | ✅ **不用** |
| `ppsh-soil-teaching-deck` | 「做教學簡報」「做上課用的投影片」 | **可編輯的 .pptx** | ✅ **不用**（AI 插圖才要） |
| `ppsh-soil-html-deck` | 「做網頁版簡報」「做可分享連結的簡報」 | **單一 .html**，可互動、可線上分享 | ✅ **不用**（AI 插圖才要） |

### 附錄技能（本場研習不裝，課後想用再說）

| 技能 | 產出 | 要 API 金鑰嗎 |
|---|---|---|
| `ppsh-soil-image-deck` | 每頁一張 AI 生圖的 .pptx | **Codex Desktop：✅ 不用**（用 Codex 內建生圖，會用掉 ChatGPT 方案額度）<br>**Claude Code：❌ 要付費的 Gemini 金鑰**（Claude Code 沒有內建生圖） |
| `ppsh-draw` | 單張 AI 插圖 PNG | ❌ **一定要，而且要付費** |

> **選錯技能會整份重做，先分清楚**：
> 「**資訊圖表**」= infographic = **一張圖**（`ppsh-soil-infographic`）；
> 「**圖表**」= chart = 長條圖圓餅圖，那是簡報裡的一個元件。
> 要「一頁一頁講」才是簡報技能。

**所有技能都不碰 git、不上傳任何東西**（`ppsh-draw` 與 `ppsh-soil-image-deck` 例外：它們會把提示詞送到生圖服務）。
跨電腦接續靠 Google 雲端硬碟電腦版。

> **關於 AI 插圖**：三個產出技能在**沒有金鑰時會自動改用向量版面**，照樣做出完整成品，
> 只是沒有 AI 插畫——**不會失敗、不會中斷**。真的想要 AI 插圖，最省錢的做法是
> 用學校 Google 帳號到 [aistudio.google.com](https://aistudio.google.com) 免費生圖，
> 存檔後自己放進簡報（**網頁介面免費，API 要錢**，這兩件事常被搞混）。

---

## 安裝：一段話交給 AI Agent

**老師不用打任何指令。** 只要做四件事：

1. 打開 **Codex Desktop** 或 **Claude Code**
2. 把下面這段話**整段複製、貼上、送出**
3. AI 要動到電腦時會跳出確認，**看一眼、按同意**
4. AI 說「裝好了，請重開」時，把 Codex／Claude Code **整個關掉再打開**

```text
請讀取 https://github.com/frentexx/ppsh-agent-skills 的 README.md，
照其中「給 AI Agent 的安裝步驟」，幫我把屏北高中的技能和需要的工具全部裝好。
我不熟指令：請你自己判斷、自己執行，需要我同意的地方跳出確認就好，不要叫我自己打指令。
全部做完後，用一張簡單的表告訴我結果，以及我接下來要做什麼。
```

**怎麼確認裝好了**：重開後問它「**你有哪些 ppsh 開頭的技能？**」，列得出 7 個就成功了。

**裝到一半失敗**：不用自己修。把 AI 最後給你的結果表**截圖給研習講師**。
（中途被要求重開也沒關係，重開後**再貼一次同一段話**，已經裝好的會自動跳過。）

---

## 給 AI Agent 的安裝步驟（老師不用看這段）

> 你正在幫一位**不熟指令**的高中老師安裝技能。規則：
> - **所有指令由你執行**，不要叫老師自己打指令，也不要把參數說明丟給老師看。
> - 會改動電腦的步驟（安裝軟體、寫入技能資料夾）照你所在 Agent 的權限確認機制取得同意即可；只讀的檢查直接跑。
> - **不要讀取、索取或顯示任何 API 金鑰**；這 7 個技能都不需要金鑰。
> - 某一步失敗就停在那一步，用白話說明卡在哪；**不要換成本文件以外的方法硬裝**。
> - 可以重複執行：已經裝好的項目檢查通過就跳過，不要重裝。

### 要裝的技能（7 個）

`ppsh-project-init`、`ppsh-startup`、`ppsh-shutdown`、`ppsh-office-reader`、`ppsh-soil-infographic`、`ppsh-soil-teaching-deck`、`ppsh-soil-html-deck`

**不要裝** `ppsh-soil-image-deck`、`ppsh-draw`（附錄技能，要老師明確指名才裝）。

### 步驟 1：判斷你是哪個 Agent

| 你是 | 技能資料夾（Windows） | 技能資料夾（macOS） | npx 的 `-a` |
|---|---|---|---|
| Codex Desktop | `%USERPROFILE%\.agents\skills\` | `~/.agents/skills/` | `codex` |
| Claude Code | `%USERPROFILE%\.claude\skills\` | `~/.claude/skills/` | `claude-code` |

- Codex **不要用內建的 `$skill-installer`**：它會裝到 `.codex\skills\`，不是官方的個人技能資料夾。
- 只裝到**你自己**的資料夾。老師若說兩個 Agent 都要，才兩邊都裝。

### 步驟 2：安裝技能

**路線 A（`node --version` 有版本號時優先用）：**

```powershell
npx skills add frentexx/ppsh-agent-skills -s ppsh-project-init ppsh-startup ppsh-shutdown ppsh-office-reader ppsh-soil-infographic ppsh-soil-teaching-deck ppsh-soil-html-deck -a <codex 或 claude-code> -g -y --copy
```

PowerShell 回「因為這個系統上已停用指令碼執行」→ 把 `npx` 改成 `npx.cmd` 重跑。

**路線 B（沒有 Node.js，或路線 A 失敗）：下載 ZIP 後複製**

```powershell
$tmp = Join-Path $env:TEMP "ppsh-agent-skills"
Invoke-WebRequest "https://github.com/frentexx/ppsh-agent-skills/archive/refs/heads/main.zip" -OutFile "$tmp.zip"
Expand-Archive "$tmp.zip" -DestinationPath $tmp -Force
$dst = "$env:USERPROFILE\.agents\skills"   # Claude Code 改成 "$env:USERPROFILE\.claude\skills"
New-Item -ItemType Directory -Force $dst | Out-Null
foreach ($s in 'ppsh-project-init','ppsh-startup','ppsh-shutdown','ppsh-office-reader','ppsh-soil-infographic','ppsh-soil-teaching-deck','ppsh-soil-html-deck') {
  Copy-Item "$tmp\ppsh-agent-skills-main\skills\$s" $dst -Recurse -Force
}
```

macOS 用 `curl -L -o` 下載、`unzip` 解壓，再 `cp -R` 到上表的資料夾。

### 步驟 3：確認技能檔案到位（只讀）

```powershell
$dir = "$env:USERPROFILE\.agents\skills"   # Claude Code 改成 "$env:USERPROFILE\.claude\skills"
foreach ($s in 'ppsh-project-init','ppsh-startup','ppsh-shutdown','ppsh-office-reader','ppsh-soil-infographic','ppsh-soil-teaching-deck','ppsh-soil-html-deck') {
  "{0,-26} {1}" -f $s, (Test-Path "$dir\$s\SKILL.md")
}
"render.py                  {0}" -f (Test-Path "$dir\ppsh-soil-infographic\render.py")
```

8 行都要是 `True`。

### 步驟 4：補齊執行環境

技能裝好不代表能用。先全部檢查一輪，**只補缺的**：

| 需要什麼 | 給哪個技能用 | 檢查（只讀） | 缺了怎麼補（要同意） |
|---|---|---|---|
| Python 3.12 或 3.13 | 三個 `ppsh-soil-*` | `python --version`；失敗再試 `py -0p` | `winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements` |
| python-pptx、Pillow、PyYAML、lxml（另建議 matplotlib、latex2mathml） | `ppsh-soil-teaching-deck` | `python -X utf8 -c "import importlib.util as u; [print(m, 'OK' if u.find_spec(m) else '缺') for m in ['pptx','PIL','yaml','lxml','matplotlib','latex2mathml']]"` | `python -X utf8 -m pip install python-pptx Pillow PyYAML lxml matplotlib latex2mathml` |
| Chrome 或 Edge | `ppsh-soil-infographic` | `Test-Path` 這兩個路徑，**任一個 `True` 就算有**：`C:\Program Files\Google\Chrome\Application\chrome.exe`、`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` | 有 Edge 就不用補；都沒有才 `winget install --id Google.Chrome -e --accept-source-agreements --accept-package-agreements` |
| uv ＋ MarkItDown | `ppsh-office-reader` | `markitdown --version`；失敗再看 `uv --version` | `winget install --id astral-sh.uv -e --accept-source-agreements --accept-package-agreements`，再 `uv tool install "markitdown[pdf,docx,pptx,xlsx]"` |

容易踩的坑：

- **`python` 跳出 Microsoft Store 或沒反應**＝Windows 的市集空殼，不是真的 Python。看 `py -0p`：有版本就把上表的 `python` 全部換成 `py -3.13`（換成列出的版本）；沒有才安裝。
- **不要用 `where.exe chrome` 判斷瀏覽器**，瀏覽器通常不在 PATH 裡。
- **Python 3.14 以上**：套件可能要現場編譯，會跑好幾分鐘，先告訴老師「正常，請等」。
- **剛用 winget 裝好的 Python／uv，這個對話還叫不到**（PATH 要重開才更新）。這時直接結束並請老師重開、再貼一次同一段話；重跑時已完成的步驟會檢查通過自動跳過。
- 更完整的說明與疑難排解：[基本功懶人包](https://github.com/frentexx/ppsh-agent-basics-packs) 的 00（環境）、01（MarkItDown）、03（產出技能）。

### 步驟 5：回報老師

用白話表格回報，**不要貼指令輸出原文**：

| 項目 | 結果 |
|---|---|
| 7 個技能 | ✅ 全部裝好／❌ 缺哪幾個 |
| Python（做簡報、圖卡用） | ✅ 版本／❌ |
| 瀏覽器（做圖卡用） | ✅ Chrome 或 Edge／❌ |
| Office 讀取工具 | ✅／❌ |

最後一定要明確告訴老師下一步，例如：
「請把 Codex（或 Claude Code）**整個關掉再打開**，然後問我：『你有哪些 ppsh 開頭的技能？』」

有任何一項 ❌：說明卡在哪一步、錯誤訊息第一行，請老師**截圖給研習講師**，不要自己換別的方法硬裝。

---

## 安全說明

- 這些技能**只在你的專案資料夾裡讀寫檔案**（Markdown、圖卡 PNG、.pptx、.html、AI 生圖，以及 Office 檔的文字副本），不會存到桌面、下載或技能資料夾。專案資料夾＝你開啟 Agent 對話時所在的資料夾；看不出是哪個專案時，AI 會先問你。
- 安裝任何技能前，都建議先打開 `SKILL.md` 看一遍——**這也是研習教的：來路不明的技能先讀再裝。**
- `ppsh-office-reader` 讀出來的內容會送到 AI 模型端處理，含學生個資的檔案請先去識別化。

## 授權

MIT License。架構參考 [mathruffian-dot/codex-lazy-packs](https://github.com/mathruffian-dot/codex-lazy-packs)（MIT）。

### 改作來源

| 技能 | 來源 | 改了什麼 |
|---|---|---|
| `ppsh-soil-teaching-deck`、`ppsh-soil-html-deck`、`ppsh-soil-image-deck` | 改作自 [mathruffian-dot/soil-deck-skills](https://github.com/mathruffian-dot/soil-deck-skills)（MIT，© 2026 mathruffian-dot），原作授權全文附於各技能資料夾的 `LICENSE` | 生圖改為選用並支援無金鑰時改走向量版面、生圖改走 Gemini（image-deck 改為 Codex 內建生圖優先、沒有才走 Gemini）、移除寫死的本機路徑、幾何圖改用 Chrome 渲染、html-deck 拿掉頁數限制並改為投影可讀字級、加研習版須知 |
| `ppsh-soil-html-deck` 的 `references/firebase-interact.md` | 移植自 [mathruffian-dot/claude-html-slide-builder](https://github.com/mathruffian-dot/claude-html-slide-builder)（MIT） | — |
| `ppsh-soil-infographic`、`ppsh-draw` 及其餘技能 | 本校自編 | — |

SOIL 教學簡報設計邏輯出自李俊儀教授的 SOIL Teaching Deck Workflow。
