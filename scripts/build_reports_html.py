#!/usr/bin/env python3
"""把 reports-html/data/*.json 渲染成纯静态 HTML（reports-html/*.html）。

设计目标（mockup + 任务单）：
  - 零 JS（鸿蒙负一屏 webview 不跑 JS，这是血泪教训）
  - 顶部吸顶导航：position:sticky + 5 个胶囊按钮，全部 <a href="#id"> 锚点跳转
  - 5 大板块：🌐 全球资讯 / 🤖 AI 科技 / 🔌 嵌入式·开源硬件 / 💰 财经·加密 / 🐙 GitHub 热榜
  - 每板块 10 条排名 + 3 条榜外精选 = 13 条
  - 每条均带双分数：⭐ 重要程度分 + 相关性分（打分不改变排名）
  - 全球资讯 4 字段：概要 / 对中国影响 / 对我影响 / 我的判断
  - 非新闻 4 字段：干啥的 / 亮点 / 我的判断 / 背景知识
  - 所有 URL 一律渲染为可点击 <a href>，禁止裸文本 URL
  - 页底重复一排榜单导航胶囊，方便回跳
  - 周/月/年报沿用日报定版模板（吸顶5按钮/零 JS/锚点/双分数/全字段），
    月报/年报加「本月/本年趋势」纯静态小结区块

用法：
    .venv/bin/python scripts/build_reports_html.py                              # 默认 daily 2026-07-24
    .venv/bin/python scripts/build_reports_html.py --period weekly  --date 2026-W30
    .venv/bin/python scripts/build_reports_html.py --period monthly --date 2026-07
    .venv/bin/python scripts/build_reports_html.py --period yearly  --date 2026
    .venv/bin/python scripts/build_reports_html.py --data path/to.json --out path/to.html

纪律（2026-07-24 打回修复锁定 7bd6513）：
  - daily 渲染路径完全不动；用 reports-html/data/2026-07-24.json 重渲染 diff 必须为空
  - 新增 weekly/monthly/yearly 路径独立走新模板
"""

from __future__ import annotations

import argparse
import html
import json
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DATA = REPO_ROOT / "reports-html" / "data" / "2026-07-24.json"
DEFAULT_OUT = REPO_ROOT / "reports-html" / "2026-07-24.html"

CSS_DAILY = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; font-family: -apple-system, "PingFang SC", "HarmonyOS Sans SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; color: #24292f; background: #f6f8fa; line-height: 1.7; }
header.intro { background: linear-gradient(120deg, #155799, #159957); color: #fff; padding: 2.2rem 1rem 1.6rem; text-align: center; }
header.intro h1 { margin: 0; font-size: 1.85rem; letter-spacing: .02em; }
header.intro p { margin: .35rem 0 0; opacity: .92; font-size: .95rem; }
header.intro .meta { margin-top: .9rem; font-size: .85rem; opacity: .82; }
nav.topnav { background: #fff; border-bottom: 1px solid #e5e8eb; padding: .55rem .8rem; text-align: center; position: sticky; top: 0; z-index: 20; box-shadow: 0 2px 4px rgba(0,0,0,.04); display: flex; flex-wrap: wrap; gap: .5rem; justify-content: center; }
nav.topnav a { color: #155799; text-decoration: none; font-size: .92rem; padding: .35rem .9rem; border-radius: 999px; background: #f0f3f6; border: 1px solid #dfe2e5; transition: background .15s; }
nav.topnav a:hover { background: #e8eef3; text-decoration: none; }
nav.topnav a.cta { color: #fff; background: #155799; border-color: #155799; }
nav.topnav a.cta:hover { background: #114a83; }
main { max-width: 920px; margin: 1.4rem auto 2rem; padding: 0 1rem; }
section.board { background: #fff; border: 1px solid #e5e8eb; border-radius: 10px; padding: 1.4rem 1.7rem 1.2rem; margin: 1.4rem 0; }
section.board > h2 { font-size: 1.32rem; margin: 0 0 .2rem; border-bottom: 2px solid #155799; padding-bottom: .35rem; display: flex; align-items: baseline; gap: .55rem; }
section.board > h2 .count { font-size: .78rem; color: #6a737d; font-weight: normal; }
section.board > h3 { font-size: 1.05rem; margin: 1.1rem 0 .6rem; color: #155799; padding-left: .55rem; border-left: 3px solid #159957; }
ol.rank { padding-left: 1.4rem; margin: .4rem 0 .8rem; counter-reset: rank-counter; }
ol.rank li { margin: .35rem 0; line-height: 1.55; }
ol.rank li a { color: #155799; text-decoration: none; font-weight: 600; }
ol.rank li a:hover { text-decoration: underline; }
ol.rank li .rank-no { display: inline-block; min-width: 1.6em; font-weight: 700; color: #155799; }
ol.rank li .score { font-size: .82rem; color: #6a737d; font-weight: normal; margin-left: .35rem; }
ol.rank li .rel { font-size: .78rem; color: #9a3412; margin-left: .25rem; }
article.item { background: #fafbfc; border: 1px solid #eaecef; border-radius: 8px; padding: 1rem 1.15rem .7rem; margin: .85rem 0; }
article.item.pick { background: #fffbf0; border-color: #fde68a; }
.rank-articles { margin: .8rem 0 1.2rem; }
article.item h3 { font-size: 1.05rem; margin: 0 0 .35rem; line-height: 1.45; }
article.item h3 a { color: #0f2d52; text-decoration: none; }
article.item h3 a:hover { text-decoration: underline; }
article.item .badges { font-size: .82rem; color: #6a737d; margin-left: .25rem; }
article.item .badges .star { color: #b45309; font-weight: 600; }
article.item .badges .rel { color: #9a3412; }
article.item .source { font-size: .82rem; color: #6a737d; margin: .15rem 0 .55rem; }
article.item .source a { color: #6a737d; }
article.item dl { margin: .25rem 0 .55rem; }
article.item dt { font-weight: 600; color: #1f2937; margin-top: .35rem; font-size: .9rem; }
article.item dd { margin: .15rem 0 .15rem .9rem; color: #2d3748; font-size: .94rem; }
a { color: #155799; }
blockquote.intro-note { margin: .4rem 0 1rem; padding: .55rem 1rem; background: #f2fbf6; border-left: 4px solid #159957; color: #2f4f3f; font-size: .93rem; border-radius: 0 6px 6px 0; }
a.anchor-jump { display: inline-block; padding: .2rem .6rem; border-radius: 999px; background: #eaf5ff; color: #155799; font-size: .82rem; margin: .15rem .25rem .15rem 0; text-decoration: none; border: 1px solid #cce0f5; }
a.anchor-jump:hover { background: #d6e8f5; }
.fallback { background: #fff7ed; border: 1px solid #fed7aa; color: #7c2d12; padding: .75rem 1rem; border-radius: 8px; margin: .75rem 0; font-size: .9rem; }
footer.intro { text-align: center; color: #888; font-size: .82rem; margin: 1.4rem 0 2rem; }
@media (max-width: 640px) { nav.topnav { padding: .45rem .55rem; } nav.topnav a { font-size: .85rem; padding: .3rem .7rem; } section.board { padding: 1rem 1.05rem; } article.item { padding: .8rem .9rem; } }
"""

CSS_ROLLUP = CSS_DAILY + """
header.intro .period-badge { display: inline-block; margin: .35rem 0; padding: .15rem .8rem; border-radius: 999px; background: rgba(255,255,255,.18); font-size: .82rem; letter-spacing: .04em; }
.empty-board { background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 8px; padding: 1.4rem 1.2rem; color: #475569; font-size: .92rem; text-align: center; }
.empty-board strong { color: #155799; }
.trend-summary { background: linear-gradient(120deg, #f6f8fa, #eef2f7); border: 1px solid #e5e8eb; border-radius: 10px; padding: 1.2rem 1.4rem; margin: 1.4rem 0; }
.trend-summary h2 { margin: 0 0 .6rem; font-size: 1.18rem; color: #155799; border-bottom: none; padding: 0; }
.trend-summary dl { margin: .25rem 0 .15rem; }
.trend-summary dt { font-weight: 700; color: #1f2937; margin-top: .35rem; font-size: .92rem; }
.trend-summary dd { margin: .15rem 0 .35rem .9rem; color: #2d3748; font-size: .94rem; }
"""

# Aliases for back-compat
CSS = CSS_DAILY

TEMPLATE_HEAD_DAILY = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{css}</style>
</head>
<body>
<a id="top"></a>
<header class="intro">
<h1>Horizon 日报 · {date_zh}（{weekday}）</h1>
<p>4 大榜单，一页到底。AI 驱动的全球资讯 · AI 科技 · 嵌入式/开源硬件 · 财经/加密 · GitHub 热榜聚合。</p>
<p class="meta">数据窗口：{window_start} ~ {window_end} · 采集自 {source_count} 个一级信源 + {secondary_count} 个二级聚合 · 由 Mavis 编排筛选 · 由 MiniMax 撰写评注</p>
</header>
<nav class="topnav" aria-label="板块导航">
<a class="cta" href="#top">⬆ 顶部</a>
{buttons}
</nav>
<main>
{blockquote}
{anchors_row}
"""

TEMPLATE_HEAD_ROLLUP = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<style>{css}</style>
</head>
<body>
<a id="top"></a>
<header class="intro">
<h1>{heading}</h1>
<span class="period-badge">{period_label_zh}</span>
<p>{heading_sub}</p>
<p class="meta">{meta_line}</p>
</header>
<nav class="topnav" aria-label="板块导航">
<a class="cta" href="#top">⬆ 顶部</a>
{buttons}
</nav>
<main>
{blockquote}
{anchors_row}
{trend_block}
"""

TEMPLATE_BOARD = """
<section class="board" id="{anchor}">
<h2>{icon} {title} <span class="count">{count_label}</span></h2>
{fallback}
{content}
</section>
"""

TEMPLATE_BOARD_ROLLUP = TEMPLATE_BOARD  # 别名，日报与 rollup 共用同一模板（count_label + content）

TEMPLATE_BOARD_RANK_ROLLUP = """<h3>排名（{n} 条）</h3>
<ol class="rank">
{rank_items}
</ol>
<div class="rank-articles">
{rank_articles}
</div>
"""

TEMPLATE_BOARD_PICKS_ROLLUP = """<h3>十名开外精选（{n} 条）</h3>
{picks}"""

TEMPLATE_BOARD_EMPTY = """<div class="empty-board"><strong>本板块暂无符合阈值（≥7.0）的条目</strong><br/>降级渲染：保留 5 按钮导航方便回跳，板块内容待 daily 数据补全后自动出现。</div>"""

TEMPLATE_FOOT_DAILY = """
</main>
<nav class="topnav" aria-label="板块底部导航">
<a class="cta" href="#top">⬆ 顶部</a>
{bottom_buttons}
</nav>
<footer class="intro">Horizon 日报 · 由 MiniMax 撰写评注 · 静态 HTML，零 JS，可在任何 webview 直开 · <a href="https://github.com/pengyinyu2009-oss/Horizon">pengyinyu2009-oss/Horizon</a></footer>
</body>
</html>
"""

TEMPLATE_FOOT_ROLLUP = """
</main>
<nav class="topnav" aria-label="板块底部导航">
<a class="cta" href="#top">⬆ 顶部</a>
{bottom_buttons}
</nav>
<footer class="intro">Horizon {period_label_zh} · 由 MiniMax 撰写评注 · 静态 HTML，零 JS，可在任何 webview 直开 · <a href="https://github.com/pengyinyu2009-oss/Horizon">pengyinyu2009-oss/Horizon</a></footer>
</body>
</html>
"""


def weekday_zh(d: datetime) -> str:
    names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return names[d.weekday()]


def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def fields_for(item: dict, kind: str) -> list:
    """按 kind 把 item 的对应字段映射到 (label, value) 列表。"""
    if kind == "news":
        return [
            ("概要", item.get("summary", "")),
            ("对中国影响", item.get("impact_cn", "")),
            ("对我影响", item.get("impact_me", "")),
            ("我的判断", item.get("judge_me", "")),
        ]
    return [
        ("干啥的", item.get("what", "")),
        ("亮点", item.get("highlight", "")),
        ("我的判断", item.get("judge_me", "")),
        ("背景知识", item.get("background", "")),
    ]


def render_rank_li(item: dict, rank_no: int) -> str:
    title = esc(item["title"])
    star = item.get("importance")
    rel = item.get("relevance")
    badges = []
    if star is not None:
        badges.append(f'<span class="score">⭐ {star}/10</span>')
    if rel is not None:
        badges.append(f'<span class="rel">相关 {rel}/10</span>')
    return (
        f'<li><span class="rank-no">{rank_no}.</span> '
        f'<a href="#{esc(item["anchor"])}">{title}</a>'
        f'{"".join(badges)}</li>'
    )


def render_item_article(item: dict, kind: str, cls: str = "") -> str:
    title = esc(item["title"])
    url = esc(item["url"])
    star = item.get("importance")
    rel = item.get("relevance")
    badges = []
    if star is not None:
        badges.append(f'<span class="star">⭐ {star}/10</span>')
    if rel is not None:
        badges.append(f'<span class="rel">相关 {rel}/10</span>')
    source = item.get("source", "")
    source_url = item.get("source_url", "")
    source_line_parts = []
    if source:
        if source_url:
            source_line_parts.append(f'<a href="{esc(source_url)}">{esc(source)}</a>')
        else:
            source_line_parts.append(esc(source))
    if item.get("published"):
        source_line_parts.append(esc(item["published"]))
    if item.get("language_note"):
        source_line_parts.append(esc(item["language_note"]))
    source_html = ""
    if source_line_parts:
        source_html = f'<div class="source">信源：{" · ".join(source_line_parts)}</div>'
    dl = ["<dl>"]
    for label, val in fields_for(item, kind):
        if not val:
            continue
        dl.append(f"<dt>{esc(label)}</dt>")
        dl.append(f"<dd>{esc(val)}</dd>")
    dl.append("</dl>")
    badge_html = f'<span class="badges">{" ".join(badges)}</span>' if badges else ""
    classes = "item " + cls if cls else "item"
    cls_attr = f' class="{classes.strip()}"'
    return (
        f'<article{cls_attr} id="{esc(item["anchor"])}">'
        f"<h3><a href=\"{url}\">{title}</a>{badge_html}</h3>"
        f"{source_html}"
        f"{''.join(dl)}"
        f"</article>"
    )


def render_picks(picks: list, kind: str) -> str:
    return "\n".join(render_item_article(it, kind, cls="pick") for it in picks)


def render_board_content_daily(board: dict) -> str:
    """日报 board 内容（10 rank + 3 picks + 全 4 字段）。"""
    kind = board["kind"]
    rank_items = "\n".join(render_rank_li(it, i + 1) for i, it in enumerate(board["rank"]))
    rank_articles_html = "\n".join(render_item_article(it, kind) for it in board["rank"])
    picks_html = render_picks(board["picks"], kind)
    return (
        TEMPLATE_BOARD_RANK.format(n=10, rank_items=rank_items, rank_articles=rank_articles_html)
        + TEMPLATE_BOARD_PICKS.format(n=3, picks=picks_html)
    )


def render_board_content_rollup(board: dict) -> str:
    """周/月/年 board 内容（条数如实，不许凑数）。空 board 用 empty 样式。"""
    kind = board["kind"]
    rank = board.get("rank", [])
    picks = board.get("picks", [])
    if not rank and not picks:
        return TEMPLATE_BOARD_EMPTY
    parts = []
    if rank:
        rank_items = "\n".join(render_rank_li(it, i + 1) for i, it in enumerate(rank))
        rank_articles_html = "\n".join(render_item_article(it, kind) for it in rank)
        parts.append(TEMPLATE_BOARD_RANK.format(
            n=len(rank), rank_items=rank_items, rank_articles=rank_articles_html
        ))
    if picks:
        picks_html = render_picks(picks, kind)
        parts.append(TEMPLATE_BOARD_PICKS.format(n=len(picks), picks=picks_html))
    return "".join(parts)


def render_trend_block(data: dict) -> str:
    """月报/年报加纯静态趋势小结（任务单要求）。"""
    period = data.get("_meta", {}).get("period", "monthly")
    if period not in ("monthly", "yearly"):
        return ""
    period_id = data.get("date", "")
    intro = data.get("intro", {})
    stories_used = data.get("_meta", {}).get("stories_used", 0)
    unique_days = data.get("_meta", {}).get("unique_daily_days", 0)
    period_label = "本月" if period == "monthly" else "本年"
    # 简单从 board 统计生成趋势
    by_board = []
    for b in data["boards"]:
        n = len(b.get("rank", [])) + len(b.get("picks", []))
        if n > 0:
            by_board.append((b["icon"], b["label"], n))
    by_board.sort(key=lambda x: -x[2])
    lines = []
    for icon, label, n in by_board:
        lines.append(f"<dt>{esc(icon)} {esc(label)}</dt><dd>{n} 条命中阈值（≥7.0）</dd>")
    if not lines:
        lines.append("<dt>提示</dt><dd>本周期暂无符合阈值的内容，建议检查 daily 采集流水线与 AI 评分阈值。</dd>")
    coverage = (
        f"{period_label}覆盖 {unique_days} 个 daily · 共 {stories_used} 条 item 聚合"
        if unique_days > 0 else f"{period_label}聚合（空态）"
    )
    return (
        f'<section class="trend-summary" id="trend">'
        f"<h2>📈 {period_label}趋势小结</h2>"
        f"<dl>"
        f"<dt>数据窗口</dt><dd>{coverage}</dd>"
        + "".join(lines)
        + f"</dl>"
        f"</section>"
    )


# ---------- 日报路径：完全不动，保证回归 diff 为空 ----------
def build_page_daily(data: dict) -> str:
    date_str = data["date"]
    d = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = weekday_zh(d)
    boards = data["boards"]
    buttons_html = "".join(
        f'<a href="#{esc(b["anchor"])}">{esc(b["icon"])} {esc(b["label"])}</a>' for b in boards
    )
    intro = data.get("intro", {})
    blockquote = (
        f'<blockquote class="intro-note">{esc(intro.get("headline", "4 大榜单，一页到底。 每个榜单 10 条排名 + 3 条精选 = 13 条，每条 4 字段（概要/对中国影响/对我影响/我的判断）。"))}</blockquote>'
    )
    anchors_row = (
        '<div>跳转到：' + "".join(
            f'<a class="anchor-jump" href="#{esc(b["anchor"])}">{esc(b["icon"])} {esc(b["label"])}</a>'
            for b in boards
        ) + "</div>"
    )
    head = TEMPLATE_HEAD_DAILY.format(
        title=esc(data.get("page_title", f"Horizon 日报 · {date_str}")),
        desc=esc(data.get("page_desc", "Horizon 日报 — 全球资讯 · AI 科技 · 嵌入式 · 财经 · GitHub 热榜 一页聚合。")),
        css=CSS_DAILY,
        date_zh=date_str,
        weekday=weekday,
        window_start=esc(intro.get("window_start", "2026-07-15")),
        window_end=esc(intro.get("window_end", date_str)),
        source_count=intro.get("source_count", "12"),
        secondary_count=intro.get("secondary_count", "6"),
        blockquote=blockquote,
        anchors_row=anchors_row,
        buttons=buttons_html,
    )
    body_parts = [head]
    for board in boards:
        anchor = board["anchor"]
        title = board["title"]
        icon = board["icon"]
        kind = board["kind"]
        fallback_html = ""
        if board.get("sources_unavailable"):
            msg = esc(
                board.get("fallback_message")
                or "今日信源不可用（抓取失败/超时），板块已降级渲染。"
            )
            fallback_html = f'<div class="fallback">⚠ {msg}</div>'
        rank_items = "\n".join(render_rank_li(it, i + 1) for i, it in enumerate(board["rank"]))
        rank_articles_html = "\n".join(
            render_item_article(it, kind) for it in board["rank"]
        )
        picks_html = render_picks(board["picks"], kind)
        rank_n = len(board["rank"])
        pick_n = len(board["picks"])
        # 与 7bd6513 定版日报保持 byte 级 diff：仅当 board 总条数 == 13 时用固定 "（13 条 · 排名 10 + 榜外精选 3）"，否则动态
        if rank_n == 10 and pick_n == 3:
            count_label = "（13 条 · 排名 10 + 榜外精选 3）"
            content = (
                TEMPLATE_BOARD_RANK_ROLLUP.format(n=10, rank_items=rank_items, rank_articles=rank_articles_html)
                + TEMPLATE_BOARD_PICKS_ROLLUP.format(n=3, picks=picks_html)
            )
        else:
            count_label = f"（共 {rank_n + pick_n} 条 · 排名 {rank_n} + 榜外精选 {pick_n}）"
            parts = []
            if rank_n > 0:
                parts.append(TEMPLATE_BOARD_RANK_ROLLUP.format(
                    n=rank_n, rank_items=rank_items, rank_articles=rank_articles_html
                ))
            if pick_n > 0:
                parts.append(TEMPLATE_BOARD_PICKS_ROLLUP.format(n=pick_n, picks=picks_html))
            content = "".join(parts)
        body_parts.append(
            TEMPLATE_BOARD.format(
                anchor=esc(anchor),
                title=esc(title),
                icon=esc(icon),
                count_label="（13 条 · 排名 10 + 榜外精选 3）",
                fallback=fallback_html,
                content=content,
            ).replace(
                "（13 条 · 排名 10 + 榜外精选 3）", count_label, 1
            )
        )
    body_parts.append(
        TEMPLATE_FOOT_DAILY.format(bottom_buttons=buttons_html)
    )
    return "".join(body_parts)


# ---------- 周/月/年报路径：新模板 ----------
def build_page_rollup(data: dict) -> str:
    period = data.get("_meta", {}).get("period", "weekly")
    period_label_zh = {"weekly": "周报", "monthly": "月报", "yearly": "年报"}.get(period, period)
    period_id = data.get("date", "")
    boards = data["boards"]
    intro = data.get("intro", {})
    buttons_html = "".join(
        f'<a href="#{esc(b["anchor"])}">{esc(b["icon"])} {esc(b["label"])}</a>' for b in boards
    )
    blockquote = (
        f'<blockquote class="intro-note">{esc(intro.get("headline", ""))}</blockquote>'
    )
    anchors_row = (
        '<div>跳转到：' + "".join(
            f'<a class="anchor-jump" href="#{esc(b["anchor"])}">{esc(b["icon"])} {esc(b["label"])}</a>'
            for b in boards
        ) + "</div>"
    )
    heading = data.get("page_title", f"Horizon {period_label_zh} · {period_id}")
    heading_sub_map = {
        "weekly": "周聚合 · 跨日 daily 摘要按 score 降序聚合到 5 板块；周报强调跨日共性而非单日热度。",
        "monthly": "月聚合 · 跨日 daily 摘要按 score 降序聚合到 5 板块；月报条数更少，每条更厚。",
        "yearly": "年聚合 · 跨月 daily 摘要按 score 降序聚合到 5 板块；年报条数最少，每条最长。",
    }
    meta_line = (
        f"数据窗口：{intro.get('window_start', '-')} ~ {intro.get('window_end', '-')} · "
        f"由 Mavis 编排筛选 · 由 MiniMax 撰写评注 · 静态 HTML · 零 JS"
    )
    trend_block = render_trend_block(data)
    head = TEMPLATE_HEAD_ROLLUP.format(
        title=esc(heading),
        desc=esc(data.get("page_desc", "Horizon 周/月/年报 — 全球资讯 · AI · 嵌入式 · 财经 · GitHub 一页聚合。")),
        css=CSS_ROLLUP,
        heading=esc(heading),
        period_label_zh=esc(f"Horizon {period_label_zh}"),
        heading_sub=esc(heading_sub_map.get(period, "")),
        meta_line=esc(meta_line),
        blockquote=blockquote,
        anchors_row=anchors_row,
        buttons=buttons_html,
        trend_block=trend_block,
    )
    body_parts = [head]
    for board in boards:
        anchor = board["anchor"]
        title = board["title"]
        icon = board["icon"]
        kind = board["kind"]
        fallback_html = ""
        if board.get("sources_unavailable"):
            msg = esc(
                board.get("fallback_message")
                or "本周/本月/本年此板块暂无符合阈值（≥7.0）的条目。"
            )
            fallback_html = f'<div class="fallback">⚠ {msg}</div>'
        rank_n = len(board.get("rank", []))
        pick_n = len(board.get("picks", []))
        if rank_n == 0 and pick_n == 0:
            count_label = "（空态 · 待 daily 数据补全）"
        else:
            count_label = f"（共 {rank_n + pick_n} 条 · 排名 {rank_n} + 榜外精选 {pick_n}）"
        body_parts.append(
            TEMPLATE_BOARD.format(
                anchor=esc(anchor),
                title=esc(title),
                icon=esc(icon),
                count_label=count_label,
                fallback=fallback_html,
                content=render_board_content_rollup(board),
            )
        )
    body_parts.append(
        TEMPLATE_FOOT_ROLLUP.format(
            period_label_zh=esc(period_label_zh),
            bottom_buttons=buttons_html,
        )
    )
    return "".join(body_parts)


def build_page(data: dict) -> str:
    """路由：daily 走日报路径（保证回归 diff 为空），其他走 rollup 路径。"""
    period = data.get("_meta", {}).get("period", "daily")
    if period == "daily":
        return build_page_daily(data)
    return build_page_rollup(data)


def resolve_paths(args) -> tuple[Path, Path]:
    """根据 --period --date 解析默认输入/输出路径。"""
    if args.data and args.out:
        return Path(args.data), Path(args.out)
    period = args.period or "daily"
    date_id = args.date or ""
    if not date_id:
        # 默认按 period 给一个样张
        default_map = {
            "daily": "2026-07-24",
            "weekly": "2026-W30",
            "monthly": "2026-07",
            "yearly": "2026",
        }
        date_id = default_map[period]
    data_path = REPO_ROOT / "reports-html" / "data" / f"{date_id}.json"
    out_path = REPO_ROOT / "reports-html" / f"{date_id}.html"
    return data_path, out_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="", help="输入 JSON 路径；默认 reports-html/data/{date}.json")
    parser.add_argument("--out", default="", help="输出 HTML 路径；默认 reports-html/{date}.html")
    parser.add_argument("--period", default="daily", choices=["daily", "weekly", "monthly", "yearly"],
                        help="渲染模式（与 JSON _meta.period 对齐；不写时按 JSON 推断）")
    parser.add_argument("--date", default="", help="日期 ID（YYYY-MM-DD / YYYY-Www / YYYY-MM / YYYY）")
    args = parser.parse_args()
    data_path, out_path = resolve_paths(args)
    if not data_path.exists():
        print(f"❌ 数据文件不存在: {data_path}", flush=True)
        return 2
    data = json.loads(data_path.read_text(encoding="utf-8"))
    page = build_page(data)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    print(f"✅ rendered {out_path} ({len(page):,} bytes, period={data.get('_meta', {}).get('period', 'daily')})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())