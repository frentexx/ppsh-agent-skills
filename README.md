# 屏北高中 Agent Skill 懶人包

> 給屏北高中教師研習用的 AI Agent 技能（Skills）。
> 每個技能都是一份純文字說明書，AI 讀了就照著做——**不是程式，不需要會寫程式。**
>
> ✅ 適用：**Codex Desktop**、**Claude Code**（兩者都支援 Skills）

安裝步驟、環境檢查、疑難排解請看姊妹 repo：
👉 **[屏北高中 Agent 基本功懶人包](https://github.com/frentexx/ppsh-agent-basics-packs)**

---

## 技能清單

| 技能 | 你怎麼叫它 | 它會做什麼 | 對應教材 |
|---|---|---|---|
| `ppsh-project-init` | 「初始化專案」 | 建立 `AGENTS.md`（專案藍圖）與 `handoff.md`（交接檔） | A5 |
| `ppsh-startup` | 「開工」 | 讀兩份檔案，回報上次做到哪、下一步 | A5 |
| `ppsh-shutdown` | 「收工」 | 把今天進度寫進交接檔，提醒雲端硬碟同步 | A5 |
| `ppsh-office-reader` | 「幫我讀這份 Word／PDF／簡報／Excel」 | 把檔案轉成文字再閱讀，不改原檔 | A3、A4 |

**三個技能都不碰 git、不上傳任何東西。** 跨電腦接續靠 Google 雲端硬碟電腦版。

---

## 最簡單的安裝方式：交給你的 AI Agent

把下面這段貼給你的 AI Agent：

```text
請讀取 https://github.com/frentexx/ppsh-agent-basics-packs 的 02-專案初始化開工收工技能.md，
照裡面的步驟幫我檢查環境並安裝技能。每一個會改動電腦的指令，先給我看、經我同意再執行。
```

## 自己下指令安裝

需要先裝好 **Node.js**（沒有的話看基本功懶人包的 00）。在 PowerShell 或終端機執行：

**Codex Desktop：**

```powershell
npx skills add frentexx/ppsh-agent-skills -s ppsh-project-init ppsh-startup ppsh-shutdown ppsh-office-reader -a codex -g -y --copy
```

**Claude Code：**

```powershell
npx skills add frentexx/ppsh-agent-skills -s ppsh-project-init ppsh-startup ppsh-shutdown ppsh-office-reader -a claude-code -g -y --copy
```

**兩個都有：** 把 `-a codex` 換成 `-a codex claude-code`。

| 參數 | 意思 |
|---|---|
| `-s` | 要裝哪幾個技能 |
| `-a` | 裝給哪個 Agent |
| `-g` | 裝到個人層級（所有專案都能用） |
| `-y` | 不逐項詢問 |
| `--copy` | 直接複製檔案（Windows 建議加，避免捷徑權限問題） |

裝完**重新開啟** Codex Desktop 或 Claude Code，技能才會出現。

## 不能用 npx 時：手動複製

1. 按本頁綠色 **Code** → **Download ZIP**，解壓縮
2. 把 `skills` 資料夾裡的四個 `ppsh-*` 資料夾，複製到：

| Agent | 目的地（Windows） | 目的地（macOS） |
|---|---|---|
| Codex Desktop | `%USERPROFILE%\.agents\skills\` | `~/.agents/skills/` |
| Claude Code | `%USERPROFILE%\.claude\skills\` | `~/.claude/skills/` |

3. 重新開啟 Agent

---

## 安全說明

- 這些技能**只會讀寫你專案資料夾裡的 Markdown 檔**，以及把 Office 檔轉成文字副本。
- 安裝任何技能前，都建議先打開 `SKILL.md` 看一遍——**這也是研習教的：來路不明的技能先讀再裝。**
- `ppsh-office-reader` 讀出來的內容會送到 AI 模型端處理，含學生個資的檔案請先去識別化。

## 授權

MIT License。架構參考 [mathruffian-dot/codex-lazy-packs](https://github.com/mathruffian-dot/codex-lazy-packs)（MIT）。
