/* Horizon App — 日报 + 每日电源课 */
"use strict";

const FEED_URL = "/reports-html/data/app-latest.json";
const LS = { feed: "hz.app.feed", theme: "hz.app.theme", done: "hz.app.done", board: "hz.app.board" };

const $ = (id) => document.getElementById(id);
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set(k, v) { localStorage.setItem(k, JSON.stringify(v)); },
};

/* ---------- tabs ---------- */
const VIEWS = ["report", "lesson", "me"];
function show(view) {
  for (const v of VIEWS) $(`view-${v}`).hidden = v !== view;
  document.querySelectorAll(".tab").forEach((t) =>
    t.classList.toggle("active", t.dataset.view === view));
}
document.querySelectorAll(".tab").forEach((t) =>
  t.addEventListener("click", () => show(t.dataset.view)));

/* ---------- theme ---------- */
function applyTheme(mode) {
  const dark = mode === "dark" || (mode === "auto" && matchMedia("(prefers-color-scheme: dark)").matches);
  document.documentElement.dataset.theme = dark ? "dark" : "light";
  $("theme-btn").textContent = dark ? "☀️" : "🌙";
}
const themeMode = () => store.get(LS.theme, "auto");
applyTheme(themeMode());
$("theme-btn").onclick = () => {
  const dark = document.documentElement.dataset.theme === "dark";
  const mode = dark ? "light" : "dark";
  store.set(LS.theme, mode); applyTheme(mode);
};
$("theme-select").value = themeMode();
$("theme-select").onchange = (e) => { store.set(LS.theme, e.target.value); applyTheme(e.target.value); };

/* ---------- report feed ---------- */
const BOARD_META = {
  "global": { name: "🌍 全球新闻" },
  "ai": { name: "🤖 Horizon 总榜" },
  "github-trending": { name: "🔥 GitHub 热榜" },
  "ee": { name: "🔧 电子工程师" },
};
let FEED = null;
let curBoard = null;

function esc(s) { return String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

async function loadFeed() {
  try {
    const r = await fetch(FEED_URL, { cache: "no-cache" });
    if (!r.ok) throw new Error(r.status);
    FEED = await r.json();
    store.set(LS.feed, FEED);
  } catch {
    FEED = store.get(LS.feed, null);
    if (!FEED) {
      $("feed-date").hidden = true;
      const e = $("feed-err");
      e.hidden = false;
      e.innerHTML = "今日日报数据还没准备好。<br>可以稍后再试，或先看 <a href='/reports-html/index.html'>Web 版</a>。";
      return;
    }
  }
  $("feed-date").textContent = `日报 · ${FEED.date} · 共 ${FEED.total} 条 · 数据完整性 ${FEED.boards_ok}/4`;
  $("hdr-date").textContent = FEED.date;
  curBoard = store.get(LS.board, FEED.boards[0]?.id);
  if (!FEED.boards.some((b) => b.id === curBoard)) curBoard = FEED.boards[0]?.id;
  renderBoards();
  renderBoardItems();
}

function renderBoards() {
  const chips = $("board-chips");
  chips.innerHTML = "";
  for (const b of FEED.boards) {
    const btn = document.createElement("button");
    btn.className = "chip" + (b.id === curBoard ? " active" : "");
    btn.textContent = BOARD_META[b.id]?.name || b.name;
    btn.onclick = () => { curBoard = b.id; store.set(LS.board, b.id); renderBoards(); renderBoardItems(); };
    chips.appendChild(btn);
  }
}

function secRow(label, text) {
  if (!text) return "";
  return `<div class="sec"><span class="lab">${esc(label)}</span><span class="val">${esc(text)}</span></div>`;
}

function renderBoardItems() {
  const b = FEED.boards.find((x) => x.id === curBoard);
  const box = $("board-list");
  if (!b) { box.innerHTML = ""; return; }
  const rows = b.items.map((it, i) => {
    const pills = [
      `<span class="pill">⭐ ${esc(it.score)}/10</span>`,
      it.relevance != null ? `<span class="pill gold">相关 ${esc(it.relevance)}/10</span>` : "",
      it.rec != null ? `<span class="pill gold">推荐 ${"⭐".repeat(it.rec_stars)}${"☆".repeat(5 - it.rec_stars)} ${esc(it.rec)}/5</span>` : "",
      it.must_see ? `<span class="pill fire">🔥 必看</span>` : "",
      it.stars ? `<span class="pill">${esc(it.stars)}</span>` : "",
    ].filter(Boolean).join("");
    const secs = [
      secRow("入选理由", it.pick_reason),
      secRow("背景", it.background),
      secRow("项目用途", it.project_usage),
      secRow("对中国影响", it.impact_cn),
      secRow("对沈阳影响", it.impact_local),
      secRow("对我影响", it.impact_me),
    ].join("");
    return `<div class="item" data-i="${i}">
      <div class="h">
        <span class="idx">${i + 1}</span>
        <div style="flex:1">
          <div class="tt">${it.must_see ? "🔥 " : ""}<a href="${esc(it.url)}" target="_blank" rel="noopener">${esc(it.title)}</a></div>
          <div class="meta">${pills}</div>
        </div>
      </div>
      <div class="sum">${esc(it.summary || "")}</div>
      <div class="more">
        ${secs}
        ${it.tags ? `<div class="tags">${esc(it.tags)}</div>` : ""}
        <div class="hint">点击收起 · <a href="${esc(it.url)}" target="_blank">原文 ↗</a></div>
      </div>
    </div>`;
  }).join("");
  box.innerHTML = rows || "<div class='hint'>本榜暂无条目</div>";
  box.querySelectorAll(".item").forEach((el) => {
    el.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) return;
      el.classList.toggle("open");
    });
  });
}

/* ---------- lessons ---------- */
let CUR = null;      // lessons.json
let doneSet = new Set(store.get(LS.done, []));

function todayStr() { return new Date().toISOString().slice(0, 10); }

function daysBetween(a, b) {
  return Math.round((new Date(b) - new Date(a)) / 86400000);
}

function todayLesson() {
  if (!CUR) return null;
  const idx = Math.min(Math.max(daysBetween(CUR.start_date, todayStr()), 0), CUR.lessons.length - 1);
  return CUR.lessons[idx];
}

function loadDone() { doneSet = new Set(store.get(LS.done, [])); }
function saveDone() { store.set(LS.done, [...doneSet]); }

function blockHtml(b) {
  if (b.type === "img") {
    return `<img loading="lazy" src="./data/${esc(b.src)}" alt="讲义插图">`;
  }
  if (b.formula) return `<div class="blk formula">${esc(b.text)}</div>`;
  const isHead = b.style === "h" || /^(核心原理|算例|自测题|上讲自测答案|下一讲预告|与 OBC|规律)/.test(b.text || "");
  if (isHead) return `<div class="blk h">${esc(b.text)}</div>`;
  if (/^图　/.test(b.text || "")) return `<div class="blk" style="text-align:center;font-size:11px;color:var(--sub)">${esc(b.text)}</div>`;
  return `<div class="blk">${esc(b.text)}</div>`;
}

function renderLesson() {
  if (!CUR) return;
  const t = todayLesson();
  const done = doneSet.has(String(t.n));
  const hero = $("lesson-today");
  hero.innerHTML = `
    <div class="lesson-hero">
      <div class="tag">今日一课 · 第 ${t.n} 讲 · ${t.minutes} 分钟</div>
      <div class="lt">${esc(t.title)}</div>
      <div class="lmeta">${esc((t.tags || []).join(" · "))}</div>
      <button class="done-btn${done ? " done" : ""}" id="btn-done">${done ? "✓ 已完成" : "标记完成"}</button>
    </div>
    <div class="lesson-body">${t.blocks.map(blockHtml).join("")}</div>`;
  $("btn-done").onclick = () => {
    if (doneSet.has(String(t.n))) doneSet.delete(String(t.n));
    else doneSet.add(String(t.n));
    saveDone(); renderLesson(); renderMe();
  };
  renderOutline();
}

function renderOutline() {
  const box = $("lesson-outline");
  const t = todayLesson();
  const byStage = [[CUR.stages[0], CUR.lessons.slice(0, 12)], [CUR.stages[1], CUR.lessons.slice(12)]];
  box.innerHTML = byStage.map(([st, ls]) => `
    <div class="stage">${esc(st.title)}</div>
    ${ls.map((l) => {
      const done = doneSet.has(String(l.n));
      const isToday = t && l.n === t.n;
      return `<button class="lrow${done ? " done" : ""}${isToday ? " today" : ""}" data-n="${l.n}">
        <span class="n">${done ? "✓" : l.n}</span>
        <span class="ot">${esc(l.title)}${isToday ? `<span class="sub">今天的课</span>` : ""}</span>
        <span class="st">${done ? "⭐" : ""}</span>
      </button>`;
    }).join("")}`).join("");
  box.querySelectorAll(".lrow").forEach((el) => el.addEventListener("click", () => {
    const n = Number(el.dataset.n);
    showLessonN(n);
  }));
}

function showLessonN(n) {
  const l = CUR.lessons.find((x) => x.n === n);
  const done = doneSet.has(String(n));
  $("lesson-today").innerHTML = `
    <div class="lesson-hero">
      <div class="tag">第 ${l.n} 讲 · ${l.minutes} 分钟${l.n === todayLesson()?.n ? " · 今天的课" : ""}</div>
      <div class="lt">${esc(l.title)}</div>
      <div class="lmeta">${esc((l.tags || []).join(" · "))}</div>
      <button class="done-btn${done ? " done" : ""}" id="btn-done">${done ? "✓ 已完成" : "标记完成"}${l.n === todayLesson()?.n ? "" : ""}</button>
    </div>
    <div class="lesson-body">${l.blocks.map(blockHtml).join("")}</div>`;
  $("btn-done").onclick = () => {
    if (doneSet.has(String(n))) doneSet.delete(String(n));
    else doneSet.add(String(n));
    saveDone(); showLessonN(n); renderMe();
  };
}

/* ---------- me tab ---------- */
function renderMe() {
  loadDone();
  const total = CUR ? CUR.lessons.length : 20;
  const doneCount = [...doneSet].filter((x) => Number(x) <= total).length;
  // streak: 从今天往回数连续完成的天数（不早于开课日）
  let streak = 0;
  const start = CUR ? CUR.start_date : todayStr();
  for (let i = 0; i < 400; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = d.toISOString().slice(0, 10);
    if (daysBetween(start, dateStr) < 0) break; // 开课日之前
    const dayN = Math.min(Math.max(daysBetween(start, dateStr), 0), total - 1);
    const lesson = CUR?.lessons[dayN];
    if (lesson && doneSet.has(String(lesson.n))) streak++;
    else if (i === 0) continue; // 今天没完成不断链
    else break;
  }
  $("me-stats").innerHTML = `
    <div class="box"><div class="v">${streak}</div><div class="k">连续天数</div></div>
    <div class="box"><div class="v">${doneCount}/${total}</div><div class="k">已完成</div></div>
    <div class="box"><div class="v">${Math.round((doneCount / total) * 100)}%</div><div class="k">进度</div></div>`;
  const stages = [
    ["第 1-12 讲 · 基础", 1, 12],
    ["第 13-20 讲 · OBC 进阶", 13, 20],
  ];
  $("stage-bars").innerHTML = stages.map(([name, a, b]) => {
    const c = [...doneSet].filter((x) => Number(x) >= a && Number(x) <= b).length;
    const pct = Math.round((c / (b - a + 1)) * 100);
    return `<div class="sb"><div class="t"><span>${name}</span><span>${c}/${b - a + 1}</span></div>
      <div class="bar"><i style="width:${pct}%"></i></div></div>`;
  }).join("");
}

/* ---------- misc ---------- */
$("btn-clear").onclick = () => {
  localStorage.removeItem(LS.feed); localStorage.removeItem(LS.done); localStorage.removeItem(LS.board);
  location.reload();
};

const hdrNow = new Date();
$("hdr-date").textContent = `${hdrNow.getMonth() + 1}月${hdrNow.getDate()}日`;
$("lesson-count").textContent = "";
$("lesson-tail").textContent = "第 21 讲起按需扩展：图腾柱双闭环 · CLLC 同步整流时序 · CAN 充电握手 · 800V 平台专题";

async function loadLessons() {
  try {
    const r = await fetch("./data/lessons.json", { cache: "no-cache" });
    if (!r.ok) throw new Error(r.status);
    CUR = await r.json();
    renderLesson();
    renderMe();
  } catch (e) {
    $("lesson-err").hidden = false;
    $("lesson-err").textContent = "课程数据加载失败，请检查网络后重试。";
  }
}

/* ---------- service worker ---------- */
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
}

/* ---------- boot ---------- */
loadLessons();
loadFeed();
