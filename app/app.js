/* Horizon App v2 — 日报 + 每日电源课 + 立创复刻 */
"use strict";

const FEED_URL = "/reports-html/data/app-latest.json";
const LS = { feed: "hz.app.feed", theme: "hz.app.theme", done: "hz.app.done", board: "hz.app.board", quiz: "hz.app.quiz", review: "hz.app.review" };

const $ = (id) => document.getElementById(id);
const store = {
  get(k, d) { try { return JSON.parse(localStorage.getItem(k)) ?? d; } catch { return d; } },
  set(k, v) { localStorage.setItem(k, JSON.stringify(v)); },
};
function esc(s) { return String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }

/* ---------- tabs / theme ---------- */
const VIEWS = ["report", "lesson", "fuke", "me"];
const TITLES = { report: "日报", lesson: "课程", fuke: "复刻", me: "我的" };
function show(view) {
  for (const v of VIEWS) $(`view-${v}`).hidden = v !== view;
  $("view-title").textContent = TITLES[view];
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.view === view));
}
document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => show(t.dataset.view)));

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

/* ---------- report ---------- */
const BOARD_META = {
  global: { name: "全球", full: "🌍 全球新闻" },
  ai: { name: "总榜", full: "🤖 Horizon 总榜" },
  "github-trending": { name: "热榜", full: "🔥 GitHub 热榜" },
  ee: { name: "嵌入式", full: "🔧 电子工程师" },
};
let FEED = null;
let curBoard = null;

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
      e.innerHTML = "今日日报数据还没准备好。<br>稍后再试，或先看 <a href='/reports-html/index.html'>Web 版</a>。";
      return;
    }
  }
  $("feed-date").textContent = `${FEED.date} · ${FEED.total} 条 · 血缘 ${FEED.boards_ok}/4 通过`;
  $("hdr-date").textContent = FEED.date;
  curBoard = store.get(LS.board, FEED.boards[0]?.id);
  if (!FEED.boards.some((b) => b.id === curBoard)) curBoard = FEED.boards[0]?.id;
  renderSeg();
  renderItems();
}

function renderSeg() {
  const seg = $("board-seg");
  seg.innerHTML = "";
  for (const b of FEED.boards) {
    const btn = document.createElement("button");
    btn.className = b.id === curBoard ? "active" : "";
    btn.textContent = BOARD_META[b.id]?.name || b.name;
    btn.onclick = () => { curBoard = b.id; store.set(LS.board, b.id); renderSeg(); renderItems(); };
    seg.appendChild(btn);
  }
}

function secRow(label, text) {
  if (!text) return "";
  return `<div class="srow"><span class="lab">${esc(label)}</span><span class="val">${esc(text)}</span></div>`;
}

function recBadge(it) {
  if (it.rec10 == null) return "";
  const cls = it.rec10 >= 7.5 ? "" : it.rec10 >= 5 ? "mid" : "low";
  return `<span class="rec ${cls}">推荐 ${it.rec10}</span>`;
}

function renderItems() {
  const b = FEED.boards.find((x) => x.id === curBoard);
  const box = $("board-list");
  if (!b) { box.innerHTML = ""; return; }
  const rows = b.items.map((it, i) => {
    const badges = [
      recBadge(it),
      `<span class="dim">客观 ${it.score ?? "?"} · 相关 ${it.relevance ?? "-"}</span>`,
      it.stars ? `<span class="stars-txt">⭐ ${esc(it.stars)}</span>` : "",
      it.must_see ? `<span class="fire">🔥 必看</span>` : "",
    ].filter(Boolean).join("");
    const secs = [
      secRow("入选理由", it.sections?.pick_reason),
      secRow("项目用途", it.sections?.project_usage),
      secRow("背景", it.sections?.background),
      secRow("对中国影响", it.sections?.impact_cn),
      secRow("对沈阳影响", it.sections?.impact_local),
      secRow("对我影响", it.sections?.impact_me),
    ].join("");
    return `<div class="item" data-i="${i}">
      <div class="h">
        <span class="idx">${i + 1}</span>
        <div style="flex:1">
          <div class="tt">${it.must_see ? "🔥 " : ""}<a href="${esc(it.url)}" target="_blank" rel="noopener">${esc(it.title)}</a></div>
          <div class="badges">${badges}</div>
        </div>
      </div>
      <div class="sum">${esc(it.summary || "")}</div>
      <div class="more">${secs}
        ${it.tags ? `<div class="tags">${esc(it.tags)}</div>` : ""}
        <div class="hint">收起 · <a href="${esc(it.url)}" target="_blank">原文 ↗</a></div>
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
let CUR = null, QUIZ = null;
let doneSet = new Set(store.get(LS.done, []));
let reviewMap = store.get(LS.review, {});
let quizDone = store.get(LS.quiz, {});
const loadDone = () => { doneSet = new Set(store.get(LS.done, [])); };
const saveDone = () => store.set(LS.done, [...doneSet]);
const todayStr = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};
const daysBetween = (a, b) => Math.round((new Date(b) - new Date(a)) / 86400000);
const addDays = (dateStr, k) => {
  const d = new Date(dateStr);
  d.setDate(d.getDate() + k);
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
};

function todayLesson() {
  if (!CUR) return null;
  const idx = Math.min(Math.max(daysBetween(CUR.start_date, todayStr()), 0), CUR.lessons.length - 1);
  return CUR.lessons[idx];
}

function blockHtml(b) {
  if (b.type === "img") {
    return `<img class="fig" loading="lazy" src="./data/${esc(b.src)}" alt="讲义插图">`;
  }
  const text = String(b.text ?? "").replace(/⟦([^⟧]+)⟧/g,
    (_m, p) => ` <img class="fml" src="./data/${esc(p)}" alt="公式"> `);
  if (b.formula) return `<div class="blk formula">${text}</div>`;
  if (b.style === "h") return `<div class="blk h">${text}</div>`;
  return `<div class="blk">${text}</div>`;
}

function lessonCard(l, opts = {}) {
  const done = doneSet.has(String(l.n));
  const kick = opts.today ? "今日一课" : `第 ${l.n} 讲`;
  const todayTag = opts.today ? "" : (l.n === todayLesson()?.n ? " · 今天的课" : "");
  return `
    <div class="lhero">
      <div class="kick">${kick} · 第 ${l.n} 讲 · 约 ${l.minutes} 分钟${todayTag}</div>
      <div class="lt">${esc(l.title)}</div>
      <div class="lmeta">${esc((l.tags || []).join(" · ")) || "电源基础"}</div>
      <button class="done-btn${done ? " done" : ""}" id="btn-done">${done ? "✓ 已完成" : "标记完成"}</button>
    </div>
    <div class="lbody">${l.blocks.map(blockHtml).join("")}</div>`;
}

function wireDone(l) {
  $("btn-done").onclick = () => {
    const k = String(l.n);
    if (doneSet.has(k)) {
      doneSet.delete(k);
      delete reviewMap[k]; // 取消完成则撤销复习排期
    } else {
      doneSet.add(k);
      scheduleReview(l.n); // 标记完成 → 进入遗忘曲线排期
    }
    saveDone();
    saveReview();
    renderLessonView(l);
    renderReview();
    renderQuizCenter();
    renderMe();
  };
}

function renderLessonView(l) {
  $("lesson-today").innerHTML = lessonCard(l, { today: l.n === todayLesson()?.n });
  wireDone(l);
  $("lesson-today").querySelectorAll("img.fml,img.fig").forEach((img) => {
    img.style.cursor = "zoom-in";
    img.onclick = () => window.open(img.src, "_blank");
  });
  renderOutline();
}

function renderLesson() {
  if (!CUR) return;
  renderLessonView(todayLesson());
}

function renderOutline() {
  const box = $("lesson-outline");
  const t = todayLesson();
  const groups = CUR.stages.map((st) => [st.title, CUR.lessons.filter((l) => l.n >= st.range[0] && l.n <= st.range[1])]);
  box.innerHTML = groups.map(([st, ls]) => `
    <div class="stage">${esc(st)}</div>
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
    renderLessonView(CUR.lessons.find((x) => x.n === Number(el.dataset.n)));
    window.scrollTo(0, 0);
  }));
}

/* ---------- 遗忘曲线复习 + 测验 ---------- */
const saveReview = () => store.set(LS.review, reviewMap);
const saveQuiz = () => store.set(LS.quiz, quizDone);
const reviewSteps = () => QUIZ?.steps || [1, 2, 4, 7, 15, 30];

function scheduleReview(n) {
  // 艾宾浩斯：完成当天起 +1/+2/+4/+7/+15/+30 天各复习一轮
  reviewMap[String(n)] = { s: 0, due: addDays(todayStr(), 1) };
}

function dueReviewList() {
  const today = todayStr();
  return Object.entries(reviewMap)
    .filter(([_, r]) => r.due <= today)
    .sort((a, b) => (a[1].due < b[1].due ? -1 : 1));
}

function renderReview() {
  const box = $("lesson-review");
  if (!box) return;
  const due = dueReviewList();
  if (!due.length) {
    const pending = Object.keys(reviewMap).length;
    box.innerHTML = `
      <div class="kcard">
        <div class="kick">🧠 遗忘曲线复习</div>
        <div class="kd">${pending
          ? `今天没有到期的复习 🎉 排期中的 ${pending} 讲按 1/2/4/7/15/30 天节奏自动出现。`
          : "学完一讲并点「标记完成」，就会自动进入 1/2/4/7/15/30 天的复习排期。"}</div>
      </div>`;
    return;
  }
  box.innerHTML = `
    <div class="kcard">
      <div class="kick">🧠 今日复习 · ${due.length} 讲到期</div>
      ${due.map(([n, r]) => {
        const l = CUR?.lessons.find((x) => x.n === Number(n));
        return l ? `<div class="epr" data-n="${n}">
          <span class="en">${String(n).padStart(2, "0")}</span>
          <span class="et">${esc(l.title)}</span>
          <span class="ec">第 ${r.s + 1} 轮 →</span>
        </div>` : "";
      }).join("")}
    </div>`;
  box.querySelectorAll(".epr").forEach((el) =>
    el.addEventListener("click", () => startReview(Number(el.dataset.n))));
}

function startReview(n) {
  const box = $("lesson-review");
  const l = CUR?.lessons.find((x) => x.n === n);
  const bank = QUIZ?.bank?.[n] || [];
  if (!l || !bank.length) { delete reviewMap[String(n)]; saveReview(); renderReview(); return; }
  const q = bank[Math.floor(Math.random() * bank.length)];
  const ans = QUIZ?.answers?.[n] || null;
  box.innerHTML = `
    <div class="kcard">
      <div class="kick">复习 · 第 ${n} 讲 ${esc(l.title)}</div>
      <div class="epbody lbody" style="margin:10px 0">${blockHtml({ type: "text", text: q })}</div>
      ${ans ? `<button class="pbtn" id="rv-ans">展开参考答案</button>
        <div class="qans lbody" id="rv-ansbox" hidden>${ans.map((a) => blockHtml({ type: "text", text: a })).join("")}</div>` : ""}
      <div class="pills">
        <button class="pbtn good" id="rv-ok">😀 记得</button>
        <button class="pbtn" id="rv-fuzzy">🤔 模糊</button>
        <button class="pbtn bad" id="rv-no">😵 忘了</button>
      </div>
    </div>`;
  const ansBtn = $("rv-ans");
  if (ansBtn) ansBtn.onclick = () => {
    const b = $("rv-ansbox");
    b.hidden = !b.hidden;
    ansBtn.textContent = b.hidden ? "展开参考答案" : "收起答案";
  };
  $("rv-ok").onclick = () => gradeReview(n, "ok");
  $("rv-fuzzy").onclick = () => gradeReview(n, "fuzzy");
  $("rv-no").onclick = () => gradeReview(n, "no");
}

function gradeReview(n, g) {
  const steps = reviewSteps();
  const r = reviewMap[String(n)] || { s: 0 };
  if (g === "ok") r.s += 1;
  else if (g === "no") r.s = 0;
  if (r.s >= steps.length) delete reviewMap[String(n)]; // 毕业 🎓
  else {
    r.due = addDays(todayStr(), g === "fuzzy" ? 1 : steps[r.s]);
    reviewMap[String(n)] = r;
  }
  saveReview();
  renderReview();
}

function sampleEvenly(arr, k) {
  if (arr.length <= k) return arr;
  const out = [];
  const step = arr.length / k;
  for (let i = 0; i < k; i++) out.push(arr[Math.floor(i * step)]);
  return out;
}

let quizRun = null;

function renderQuizCenter() {
  const box = $("lesson-quiz");
  if (!box) return;
  quizRun = null;
  if (!QUIZ?.quizzes?.length) { box.innerHTML = ""; return; }
  box.innerHTML = QUIZ.quizzes.map((q) => {
    const done = quizDone[q.id];
    const missing = q.cover.filter((n) => !doneSet.has(String(n))).length;
    const ready = missing === 0;
    const state = done
      ? `<span class="qscore">✓ ${done.right}/${done.total} · ${done.date.slice(5)}</span>`
      : ready ? `<span class="ec">开始 →</span>`
      : `<span class="dim">还差 ${missing} 讲</span>`;
    return `<div class="epr qz${done ? " done" : ""}${ready ? " ready" : ""}" data-id="${q.id}">
      <span class="ek">${q.type === "final" ? "综合" : "单元"}</span>
      <span class="et">${esc(q.title)}</span>${state}
    </div>`;
  }).join("");
  box.querySelectorAll(".qz.ready").forEach((el) =>
    el.addEventListener("click", () => startQuiz(el.dataset.id)));
}

function startQuiz(id) {
  const q = QUIZ.quizzes.find((x) => x.id === id);
  if (!q) return;
  const withBank = q.cover.filter((n) => (QUIZ.bank?.[n] || []).length);
  const lessons = q.type === "final" ? sampleEvenly(withBank, 10) : withBank;
  quizRun = { q, picks: [], i: 0, right: 0, wrong: [] };
  for (const n of lessons) {
    const bank = QUIZ.bank[n];
    quizRun.picks.push({ n, text: bank[Math.floor(Math.random() * bank.length)] });
  }
  renderQuizQuestion();
}

function renderQuizQuestion() {
  const box = $("lesson-quiz");
  const { q, picks, i } = quizRun;
  const p = picks[i];
  const ans = QUIZ?.answers?.[p.n] || null;
  box.innerHTML = `
    <div class="kcard">
      <div class="kick">${esc(q.title)} · 第 ${i + 1}/${picks.length} 题（来自第 ${p.n} 讲）</div>
      <div class="epbar"><i style="width:${Math.round((i / picks.length) * 100)}%"></i></div>
      <div class="epbody lbody" style="margin:10px 0">${blockHtml({ type: "text", text: p.text })}</div>
      ${ans ? `<button class="pbtn" id="qz-ans">展开参考答案</button>
        <div class="qans lbody" id="qz-ansbox" hidden>${ans.map((a) => blockHtml({ type: "text", text: a })).join("")}</div>` : `<div class="kmeta">这题没有参考答案，凭记忆自评。</div>`}
      <div class="pills">
        <button class="pbtn good" id="qz-right">答对了</button>
        <button class="pbtn bad" id="qz-wrong">答错了</button>
      </div>
    </div>`;
  const ansBtn = $("qz-ans");
  if (ansBtn) ansBtn.onclick = () => {
    const b = $("qz-ansbox");
    b.hidden = !b.hidden;
    ansBtn.textContent = b.hidden ? "展开参考答案" : "收起答案";
  };
  $("qz-right").onclick = () => gradeQuiz(true);
  $("qz-wrong").onclick = () => gradeQuiz(false);
  window.scrollTo(0, 0);
}

function gradeQuiz(ok) {
  const { picks, i } = quizRun;
  if (!ok) quizRun.wrong.push(picks[i].n);
  else quizRun.right += 1;
  quizRun.i += 1;
  if (quizRun.i < picks.length) { renderQuizQuestion(); return; }
  // 结算：错题所在讲重置到明天复习
  for (const n of quizRun.wrong) reviewMap[String(n)] = { s: 0, due: addDays(todayStr(), 1) };
  saveReview();
  quizDone[quizRun.q.id] = { right: quizRun.right, total: picks.length, date: todayStr() };
  saveQuiz();
  const pct = Math.round((quizRun.right / picks.length) * 100);
  $("lesson-quiz").innerHTML = `
    <div class="kcard">
      <div class="kick">${esc(quizRun.q.title)} · 完成</div>
      <div class="kt">${quizRun.right}/${picks.length} · ${pct >= 80 ? "优秀 🏆" : pct >= 60 ? "不错，继续 💪" : "建议回看错题讲 📖"}</div>
      ${quizRun.wrong.length ? `<div class="kd">错题来自第 ${[...new Set(quizRun.wrong)].join("、")} 讲，已重置进明天的复习计划。</div>` : `<div class="kd">全对，相关讲的复习排期保持不变。</div>`}
      <div class="pills"><button class="pbtn primary" id="qz-back">返回测验中心</button></div>
    </div>`;
  $("qz-back").onclick = () => renderQuizCenter();
}

/* ---------- fuke (立创复刻) ---------- */
let LIAOJIE = null, FUJING = null, fukeDoneSet = new Set(store.get("hz.app.fuke", []));

function mdHtml(md) {
  const lines = md.split("\n");
  let out = "", i = 0;
  const inl = (s) => esc(s)
    .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  while (i < lines.length) {
    const ln = lines[i];
    if (!ln.trim()) { i++; continue; }
    if (ln.startsWith("### ")) { out += `<div class="blk h">${inl(ln.slice(4))}</div>`; i++; continue; }
    if (ln.startsWith("## ")) { out += `<div class="blk h">${inl(ln.slice(3))}</div>`; i++; continue; }
    if (ln.startsWith("# ")) { out += `<div class="blk h">${inl(ln.slice(2))}</div>`; i++; continue; }
    if (/^\s*\|/.test(ln)) {
      const rows = [];
      while (i < lines.length && /^\s*\|/.test(lines[i])) { rows.push(lines[i]); i++; }
      const cells = (r) => r.split("|").slice(1, -1).map((c) => c.trim());
      let t = "<table>";
      rows.forEach((r, ri) => {
        if (/^\s*\|[\s:|-]+\|\s*$/.test(r)) return;
        t += "<tr>" + cells(r).map((c) => `<t${ri === 0 ? "h" : "d"}>${inl(c)}</t${ri === 0 ? "h" : "d"}>`).join("") + "</tr>";
      });
      out += t + "</table>";
      continue;
    }
    if (/^\s*[-*] /.test(ln)) {
      let items = [];
      while (i < lines.length && /^\s*[-*] /.test(lines[i])) { items.push(lines[i].replace(/^\s*[-*] /, "")); i++; }
      out += "<ul>" + items.map((x) => `<li>${inl(x)}</li>`).join("") + "</ul>";
      continue;
    }
    if (/^---/.test(ln)) { out += "<hr>"; i++; continue; }
    out += `<div class="blk">${inl(ln)}</div>`;
    i++;
  }
  return out;
}

async function loadFuke() {
  try {
    const [lr, fr] = await Promise.all([
      fetch("./data/liaojie.json").then((r) => r.json()),
      fetch("./data/fujing.json").then((r) => r.json()),
    ]);
    LIAOJIE = lr.items; FUJING = fr;
  } catch {
    $("fuke-err").hidden = false;
    $("fuke-err").textContent = "复刻数据加载失败，请稍后重试。";
    return;
  }
  renderFuke();
}

function renderFuke() {
  // 今日了解
  const dayIdx = Math.max(daysBetween(FUJING.start_date, todayStr()), 0);
  const lj = LIAOJIE[dayIdx % LIAOJIE.length];
  $("fuke-today").innerHTML = `
    <div class="kcard">
      <div class="kick">今日了解 · ${esc(lj.source)}</div>
      <div class="kt">${esc(lj.name)}</div>
      <div class="kd">${esc(lj.oneliner)}</div>
      ${lj.link ? `<div class="kmeta"><a class="kbtn ghost" href="${esc(lj.link)}" target="_blank" rel="noopener">项目页 ↗</a></div>` : ""}
    </div>`;

  // 精讲连载：今日一期
  const epIdx = Math.min(dayIdx, FUJING.episodes.length - 1);
  const ep = FUJING.episodes[epIdx];
  const epDone = fukeDoneSet.has(String(ep.n));
  const pct = Math.round(((epIdx + 1) / FUJING.episodes.length) * 100);
  const weekTitle = (FUJING.week_titles || {})[String(ep.week)] || "";
  $("fuke-series").innerHTML = `
    <div class="kcard">
      <div class="kick">精讲连载 · 第 ${ep.week} 周 ${esc(weekTitle)}</div>
      <div class="kt">${esc(ep.title)}</div>
      <div class="kmeta"><span class="kind">${esc(ep.kind)}</span> 第 ${ep.n}/${FUJING.episodes.length} 期 · 约 ${esc(FUJING.minutes || 12)} 分钟</div>
      <div class="goal">🎯 本期目标：${esc(ep.goal)}</div>
      <div class="epbar"><i style="width:${pct}%"></i></div>
      <div class="kmeta">${esc(FUJING.stage)} · 共 ${FUJING.episodes.length} 期 / ${FUJING.weeks.length} 周</div>
      <div class="epbody lbody">${mdHtml(ep.body)}</div>
      <button class="done-btn" id="fuke-done">${epDone ? "✓ 本期已读" : "本期已读"}</button>
    </div>
    <div class="kcard">
      <div class="ct">连载目录</div>
      ${FUJING.weeks.map((w) => `
        <div class="wk">第 ${w} 周 · ${esc((FUJING.week_titles || {})[String(w)] || "")}</div>
        ${FUJING.episodes.filter((e) => e.week === w).map((e) => {
          const done = fukeDoneSet.has(String(e.n));
          return `<div class="epr${done ? " done" : ""}" data-n="${e.n}">
            <span class="en">${String(e.n).padStart(2, "0")}</span>
            <span class="ek">${esc(e.kind)}</span>
            <span class="et">${esc(e.title)}</span>
            ${e.n === ep.n ? `<span class="ec">今天</span>` : ""}
          </div>`;
        }).join("")}`).join("")}
      ${FUJING.url ? `<div class="kmeta" style="margin-top:10px">开源项目页：<a href="${esc(FUJING.url)}" target="_blank" rel="noopener">${esc(FUJING.url)}</a></div>` : ""}
    </div>
    <div class="kcard">
      <div class="ct">随查手册（不占每日进度）</div>
      ${FUJING.appendix.map((a) => `
        <div class="apx" data-id="${esc(a.id)}">
          <div class="apx-h"><span>${esc(a.icon)} ${esc(a.title)}</span><span class="apx-t">展开</span></div>
          <div class="apx-b lbody" hidden>${mdHtml(a.body)}</div>
        </div>`).join("")}
    </div>`;

  $("fuke-done").onclick = () => {
    const k = String(ep.n);
    if (fukeDoneSet.has(k)) fukeDoneSet.delete(k); else fukeDoneSet.add(k);
    store.set("hz.app.fuke", [...fukeDoneSet]);
    renderFuke();
  };
  document.querySelectorAll(".epr").forEach((el) => el.addEventListener("click", () => {
    const e = FUJING.episodes.find((x) => x.n === Number(el.dataset.n));
    $("fuke-today").insertAdjacentHTML("afterend", "");
    window.scrollTo(0, 0);
    $("fuke-series").innerHTML = `
      <div class="kcard">
        <div class="kick">精讲连载 · 第 ${e.n} 期</div>
        <div class="kt">${esc(e.title)}</div>
        <div class="goal">🎯 本期目标：${esc(e.goal)}</div>
        <div class="epbody lbody">${mdHtml(e.body)}</div>
        <button class="done-btn" onclick="renderFuke()">返回连载</button>
      </div>`;
  }));
  document.querySelectorAll(".apx").forEach((el) => el.addEventListener("click", () => {
    const b = el.querySelector(".apx-b");
    b.hidden = !b.hidden;
    el.querySelector(".apx-t").textContent = b.hidden ? "展开" : "收起";
  }));
}

/* ---------- me ---------- */
function renderMe() {
  loadDone();
  const total = CUR ? CUR.lessons.length : 30;
  const doneCount = [...doneSet].filter((x) => Number(x) <= total).length;
  let streak = 0;
  const start = CUR ? CUR.start_date : todayStr();
  const fmtLocal = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  for (let i = 0; i < 400; i++) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateStr = fmtLocal(d);
    if (daysBetween(start, dateStr) < 0) break;
    const dayN = Math.min(Math.max(daysBetween(start, dateStr), 0), total - 1);
    const lesson = CUR?.lessons[dayN];
    if (lesson && doneSet.has(String(lesson.n))) streak++;
    else if (i === 0) continue;
    else break;
  }
  $("me-stats").innerHTML = `
    <div class="box"><div class="v">${streak}</div><div class="k">连续天数</div></div>
    <div class="box"><div class="v">${doneCount}/${total}</div><div class="k">已完成</div></div>
    <div class="box"><div class="v">${Math.round((doneCount / total) * 100)}%</div><div class="k">进度</div></div>`;
  const stages = (CUR?.stages || []).map((st) => [st.title, st.range[0], st.range[1]]);
  $("stage-bars").innerHTML = stages.map(([name, a, b]) => {
    const c = [...doneSet].filter((x) => Number(x) >= a && Number(x) <= b).length;
    const pct = Math.round((c / (b - a + 1)) * 100);
    return `<div class="sb"><div class="t"><span>${esc(name)}</span><span>${c}/${b - a + 1}</span></div>
      <div class="bar"><i style="width:${pct}%"></i></div></div>`;
  }).join("");
  const recent = [...doneSet].map(Number).sort((a, b) => b - a).slice(0, 6);
  const rec = $("me-recent");
  if (rec) rec.innerHTML = recent.length
    ? recent.map((n) => {
        const l = CUR?.lessons.find((x) => x.n === n);
        return l ? `<div class="mrow"><span>第 ${n} 讲 · ${esc(l.title)}</span><span class="sub">✓ 完成</span></div>` : "";
      }).join("")
    : `<div class="sub" style="padding:4px 0">还没有完成记录 —— 去「课程」看完一讲，点「标记完成」。</div>`;
  const dv = $("data-ver");
  if (dv) dv.textContent = CUR ? `v${CUR.version} · 共 ${CUR.lessons.length} 讲` : "";
}

/* ---------- misc / boot ---------- */
$("btn-clear").onclick = () => {
  localStorage.removeItem(LS.feed); localStorage.removeItem(LS.done);
  localStorage.removeItem(LS.board); localStorage.removeItem("hz.app.fuke");
  localStorage.removeItem(LS.quiz); localStorage.removeItem(LS.review);
  location.reload();
};

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("./sw.js").catch(() => {});
  let swRefreshing = false;
  navigator.serviceWorker.addEventListener("controllerchange", () => {
    if (swRefreshing) return;
    swRefreshing = true;
    location.reload(); // 新版本接管后自动刷新一次，告别旧缓存
  });
}

const loadLessons = async () => {
  try {
    const [lr, qr] = await Promise.all([
      fetch("./data/lessons.json", { cache: "no-cache" }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); }),
      fetch("./data/quizzes.json", { cache: "no-cache" }).then((r) => r.json()).catch(() => null),
    ]);
    CUR = lr;
    QUIZ = qr;
    $("lesson-count").textContent = `${CUR.lessons.length} 讲 · 每天解锁一讲`;
    renderLesson();
    renderReview();
    renderQuizCenter();
    renderMe();
  } catch {
    $("lesson-err").hidden = false;
    $("lesson-err").textContent = "课程数据加载失败，请检查网络后重试。";
  }
};
loadLessons();
loadFuke();
loadFeed();
