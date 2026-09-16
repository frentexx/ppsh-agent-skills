# 即時互動元件（文字雲 / 投票）— Firebase 版

移植自 [claude-html-slide-builder](https://github.com/mathruffian-dot/claude-html-slide-builder)，
搭配 soil-html-deck 使用：讓某一頁投影片變成「上課當下學生手機同步輸入、畫面即時更新」的互動頁。

> 這是**選用**元件，只有骨架階段被標記需要「破冰文字雲」「課堂投票」的頁面才會用到。
> 沒有這類需求的簡報完全不用讀這份檔案。

---

## 使用前必做：確認 Firebase 專案與規則

**不要用來源 repo 裡的公用示範專案**（`teacherstudy-109ef`，資料公開共用，不同人的課會混在一起）。

改用使用者自己的 Firebase 專案：
1. 詢問使用者要用哪個 Firebase 專案（若使用者之前做過其他 Firebase 專案，如 `basic-learning-2384f`，可以問是否沿用）
2. 跟使用者要 `firebaseConfig`（在 Firebase Console → 專案設定 → 一般 → 你的應用程式）
3. **提醒使用者到 Firestore 規則加一條**（文字雲/投票需要讓未登入的學生也能寫入，跟公告用的「僅教師可寫」規則不同）：

```
match /{deckSlug}_wordcloud/{doc} {
  allow read: if true;
  allow write: if request.resource.data.word is string
               && request.resource.data.word.size() <= 20;
}
match /{deckSlug}_poll/{doc} {
  allow read, write: if true;
}
```

> `{deckSlug}` 是每份簡報自訂的英文短名前綴，不同簡報用不同集合名稱，資料才不會互相污染。
> 投票用 `allow read, write: if true` 是因為要用「合併寫入使用者投票」的匿名 userId 方式，
> 沒有登入機制就無法再收斂權限，這是這類免登入即時互動元件的已知取捨——不要拿來蒐集敏感資料。

---

## 元件一：即時文字雲

需要的 CDN（加在 `<head>` 裡）：
```html
<script src="https://cdn.jsdelivr.net/npm/wordcloud@1.2.2/src/wordcloud2.min.js"></script>
```

### Section HTML

```html
<section id="slide-wordcloud">
  <h2 style="font-size:1.1em; margin-bottom:0.4em;"><!-- 問題標題 --></h2>
  <div style="display:grid; grid-template-columns:250px 1fr; gap:14px; height:460px;">

    <div style="display:flex; flex-direction:column; gap:10px;">
      <div style="background:rgba(255,255,255,0.06); border-radius:10px; padding:14px;">
        <div style="font-size:0.38em; color:var(--accent2); font-weight:700; margin-bottom:8px;">輸入你的答案</div>
        <input id="wc-input" type="text" placeholder="輸入關鍵詞…" maxlength="20"
          style="width:100%; padding:8px 12px; border-radius:8px; border:1px solid rgba(79,195,247,0.3);
                 background:rgba(255,255,255,0.08); color:#fff; font-size:13px;
                 box-sizing:border-box; font-family:inherit; outline:none;" />
        <button id="wc-btn"
          style="width:100%; margin-top:8px; padding:9px; background:var(--accent2); color:#0d1117;
                 border:none; border-radius:8px; font-weight:700; font-size:13px; cursor:pointer;">
          送出 ↵
        </button>
      </div>
      <div style="background:rgba(255,255,255,0.06); border-radius:10px; padding:14px; flex:1; overflow:hidden; display:flex; flex-direction:column;">
        <div style="font-size:0.38em; color:var(--accent2); font-weight:700; margin-bottom:8px;">
          熱門答案
          <span style="display:inline-block; background:#ff4757; color:#fff; padding:2px 7px;
                       border-radius:10px; font-size:0.85em; animation:pulse 1.5s infinite;">LIVE</span>
        </div>
        <div id="wc-list" style="font-size:0.34em; overflow-y:auto; flex:1; color:#ccc;"></div>
        <div style="margin-top:8px; font-size:0.32em; color:#666; border-top:1px solid rgba(255,255,255,0.08); padding-top:6px;">
          總提交：<span id="wc-total" style="color:var(--accent); font-weight:700;">0</span>　
          不同答案：<span id="wc-unique" style="color:var(--accent2); font-weight:700;">0</span>
        </div>
      </div>
    </div>

    <div style="background:rgba(255,255,255,0.04); border-radius:12px; overflow:hidden;
                position:relative; border:1px solid rgba(255,255,255,0.07);">
      <canvas id="wc-canvas" style="width:100%; height:100%; display:block;"></canvas>
      <div id="wc-empty" style="position:absolute; top:50%; left:50%; transform:translate(-50%,-50%);
                                 color:#444; font-size:0.42em; text-align:center;
                                 pointer-events:none; line-height:2;">
        輸入第一個答案<br>文字雲就會出現 ✨
      </div>
    </div>
  </div>
</section>
```

### Firebase Module Script（放在 `</body>` 前）

```html
<script type="module">
  import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js';
  import {
    getFirestore, collection, addDoc, onSnapshot,
    serverTimestamp, query, orderBy
  } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';

  const firebaseConfig = { /* {{FIREBASE_CONFIG}} 由使用者提供，套用實際專案設定 */ };
  const app = initializeApp(firebaseConfig);
  const fdb = getFirestore(app);
  // 集合名稱一律用 <簡報slug>_wordcloud，不同簡報換掉 <slug>
  const wordsRef = collection(fdb, '{{DECK_SLUG}}_wordcloud');

  const COLORS = ['#4fc3f7','#e8643a','#ffb74d','#81c784','#ce93d8','#80deea','#f48fb1'];
  let wcData = [];

  window.wcSubmit = async function() {
    const input = document.getElementById('wc-input');
    const word = input.value.trim();
    if (!word) return;
    const btn = document.getElementById('wc-btn');
    btn.disabled = true;
    try {
      await addDoc(wordsRef, { word, created_at: serverTimestamp() });
      input.value = '';
    } catch(e) { console.error(e); }
    finally { btn.disabled = false; }
  };

  document.getElementById('wc-input')?.addEventListener('keypress', e => {
    if (e.key === 'Enter') window.wcSubmit();
  });
  document.getElementById('wc-btn')?.addEventListener('click', window.wcSubmit);

  onSnapshot(query(wordsRef, orderBy('created_at', 'asc')), snap => {
    const words = [];
    snap.forEach(doc => words.push(doc.data().word));
    const counts = {};
    words.forEach(w => counts[w] = (counts[w] || 0) + 1);
    wcData = Object.entries(counts).sort((a, b) => b[1] - a[1]);

    document.getElementById('wc-total').textContent = words.length;
    document.getElementById('wc-unique').textContent = wcData.length;

    const listEl = document.getElementById('wc-list');
    listEl.innerHTML = wcData.slice(0, 12).map(([w, c]) =>
      `<div style="display:flex;justify-content:space-between;padding:4px 0;
                   border-bottom:1px solid rgba(255,255,255,0.06);">
        <span>${w}</span><span style="color:var(--accent);font-weight:700;">${c}</span>
      </div>`
    ).join('') || '<div style="color:#555;padding:8px 0;">尚無資料</div>';

    const empty = document.getElementById('wc-empty');
    if (empty) empty.style.display = wcData.length > 0 ? 'none' : '';
    drawWordCloud();
  });

  function drawWordCloud() {
    const canvas = document.getElementById('wc-canvas');
    if (!canvas || typeof WordCloud === 'undefined') return;
    const rect = canvas.getBoundingClientRect();
    if (rect.width < 10 || rect.height < 10) return;
    canvas.width = rect.width;
    canvas.height = rect.height;
    if (wcData.length === 0) return;
    const maxCount = wcData[0][1];
    WordCloud(canvas, {
      list: wcData.map(([w, c]) => [w, Math.max(18, Math.round((c / maxCount) * 76))]),
      gridSize: 6,
      weightFactor: 1,
      fontFamily: '"Microsoft JhengHei", "Noto Sans TC", sans-serif',
      color: () => COLORS[Math.floor(Math.random() * COLORS.length)],
      backgroundColor: 'transparent',
      rotateRatio: 0.3,
      shuffle: true,
    });
  }

  // soil-html-deck 用的是自訂切頁邏輯（見 SKILL.md 第5步），不是 Reveal.js，
  // 所以改用 data-slide 屬性變化來偵測切頁，見下方「與 soil-html-deck 切頁邏輯整合」
</script>
```

---

## 元件二：單選投票

### Section HTML

```html
<section id="slide-poll">
  <h2><!-- 投票問題 --></h2>
  <div id="poll-options" style="display:flex; flex-direction:column; gap:12px; margin-top:0.8em;"></div>
  <div style="font-size:0.38em; color:#666; text-align:center; margin-top:0.8em;">
    已投票：<span id="poll-total">0</span> 人
  </div>
</section>
```

### Firebase Module Script

```html
<script type="module">
  import { initializeApp } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-app.js';
  import {
    getFirestore, doc, setDoc, onSnapshot, serverTimestamp
  } from 'https://www.gstatic.com/firebasejs/12.16.0/firebase-firestore.js';

  const firebaseConfig = { /* {{FIREBASE_CONFIG}} */ };
  const app = initializeApp(firebaseConfig);
  const fdb = getFirestore(app);

  // 選項設定（根據實際題目修改）
  const OPTIONS = [
    { id: 'a', label: '選項 A' },
    { id: 'b', label: '選項 B' },
    { id: 'c', label: '選項 C' },
  ];
  const pollRef = doc(fdb, '{{DECK_SLUG}}_poll', 'results');

  const userId = 'user_' + Math.random().toString(36).slice(2, 9);
  let myVote = null;

  const container = document.getElementById('poll-options');
  OPTIONS.forEach(opt => {
    const btn = document.createElement('button');
    btn.id = `poll-btn-${opt.id}`;
    btn.innerHTML = `
      <div style="display:flex;align-items:center;gap:12px;">
        <span style="flex:0 0 24px;height:24px;border-radius:50%;border:2px solid rgba(255,255,255,0.3);
                     display:flex;align-items:center;justify-content:center;font-size:12px;"
              id="poll-check-${opt.id}"></span>
        <span style="flex:1;text-align:left;">${opt.label}</span>
        <span id="poll-bar-wrap-${opt.id}"
              style="flex:0 0 120px;height:8px;background:rgba(255,255,255,0.1);border-radius:4px;overflow:hidden;">
          <div id="poll-bar-${opt.id}" style="height:100%;width:0;background:var(--accent2);border-radius:4px;transition:width 0.4s;"></div>
        </span>
        <span id="poll-pct-${opt.id}" style="flex:0 0 36px;text-align:right;font-size:0.75em;color:#888;">0%</span>
      </div>
    `;
    btn.style.cssText = `width:100%;padding:12px 16px;background:rgba(255,255,255,0.06);
      border:1px solid rgba(255,255,255,0.12);border-radius:10px;color:#fff;
      font-size:0.48em;cursor:pointer;font-family:inherit;text-align:left;`;
    btn.onclick = () => vote(opt.id);
    container.appendChild(btn);
  });

  async function vote(optId) {
    myVote = optId;
    const data = {};
    data[`votes.${userId}`] = optId;
    data.updated_at = serverTimestamp();
    await setDoc(pollRef, data, { merge: true });
  }

  onSnapshot(pollRef, snap => {
    const data = snap.data() || {};
    const votes = data.votes || {};
    const counts = {};
    OPTIONS.forEach(o => counts[o.id] = 0);
    Object.values(votes).forEach(v => { if (counts[v] !== undefined) counts[v]++; });
    const total = Object.values(counts).reduce((a, b) => a + b, 0);

    document.getElementById('poll-total').textContent = total;
    OPTIONS.forEach(opt => {
      const pct = total > 0 ? Math.round((counts[opt.id] / total) * 100) : 0;
      document.getElementById(`poll-bar-${opt.id}`).style.width = pct + '%';
      document.getElementById(`poll-pct-${opt.id}`).textContent = pct + '%';
      const check = document.getElementById(`poll-check-${opt.id}`);
      if (myVote === opt.id) {
        check.textContent = '✓';
        check.style.background = 'var(--accent2)';
        check.style.borderColor = 'var(--accent2)';
      }
    });
  });
</script>
```

---

## 與 soil-html-deck 切頁邏輯整合

soil-html-deck 用的是自訂 `data-slide` 屬性 + JS 切頁（不是 Reveal.js 的 `Reveal.on('slidechanged', ...)`）。
文字雲用 canvas 繪製，切到該頁時 canvas 尺寸可能還是 0，要比照 SKILL.md 既有的
「lazy render（切到該頁才初始化）」原則，在 soil-html-deck 現有的切頁函式裡加一段：

```js
// 在既有的切頁函式（跳到下一頁/上一頁的那個函式）裡加：
if (slides[currentSlide].id === 'slide-wordcloud') {
  setTimeout(drawWordCloud, 150);
}
```

投票元件沒有 canvas 尺寸問題，`onSnapshot` 掛載後會自己即時更新，不需要額外處理切頁。

---

## 何時該用（骨架階段的判斷原則）

| 情境 | 用哪個元件 |
|------|-----------|
| 開場破冰、先備知識調查、課尾反思 | 文字雲 |
| 概念確認、意見調查、前測/後測 | 投票 |
| 一份簡報通常只需要 0–1 頁用這類元件，不要多頁重複用，互動感會被稀釋 |

**不適用**：離線播放的簡報（沒有網路無法即時同步）、需要保護學生隱私不宜蒐集任何輸入的場合。
