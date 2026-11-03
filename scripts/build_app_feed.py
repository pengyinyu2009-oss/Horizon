#!/usr/bin/env python3
"""Build the app data feed (app-latest.json) from the four board summaries.

The PWA at /app/ fetches /reports-html/data/app-latest.json. This script
parses the four unified-layout board markdowns (global / horizon /
github-trending / ee) for a given date and emits one compact JSON:

  {version, generated_at, date, total, boards_ok,
   boards: [{id, name, items: [{id, title, url, score, relevance,
             stars, rec, rec_stars, must_see, summary, sections{...},
             tags, source_line}]}]}

Non-fatal by contract: the publish pipeline treats a feed failure as a
warning (the app keeps showing the previous day's feed).
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path

# (显示 id, 文件名中缀, 名称) —— 主榜文件中缀是 horizon 而非 ai
BOARDS = [
    ("global", "global", "🌍 全球新闻"),
    ("ai", "horizon", "🤖 Horizon 总榜"),
    ("github-trending", "github-trending", "🔥 GitHub 热榜"),
    ("ee", "ee", "🔧 电子工程师"),
]

ANCHOR_RE = re.compile(r'^<a id="item-([^"]+)"></a>\s*$', re.M)
HEADER_RE = re.compile(
    r"^#{2,3}\s+(?:🔥\s+)?\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*"
    r"⭐️?\s*(?P<score>[\d.?]+)/10"
    r"(?:\s*·\s*相关\s*(?P<rel>[\d.?]+)/10)?"
    r"(?:\s*·\s*推荐\s*(?P<recstars>[\u2b50\ufe0f]*)[\u2606]*\s*(?P<rec>[\d.]+)/5)?",
    re.M,
)
STARS_RE = re.compile(r"⭐\s*([\d.]+\s*[万kK]?)\s*总星标")
SECTION_LABELS = {
    "入选理由": "pick_reason",
    "背景": "background",
    "对这个项目有什么用": "project_usage",
    "对中国影响": "impact_cn",
    "对我影响": "impact_me",
    "社区讨论": "discussion",
}
LOCAL_RE = re.compile(r"^对(?!中国)\S{1,10}?影响$")
TAGS_RE = re.compile(r"^\*\*标签\*\*: (.+)$")


def _parse_blocks(text: str) -> list[dict]:
    """Split one board markdown into per-item blocks."""
    anchors = list(ANCHOR_RE.finditer(text))
    blocks = []
    for i, m in enumerate(anchors):
        end = anchors[i + 1].start() if i + 1 < len(anchors) else len(text)
        blocks.append(text[m.start():end])
    return blocks


def _parse_item(block: str, item_id: str) -> dict:
    item = {"id": item_id}
    hm = HEADER_RE.search(block)
    if hm:
        item["title"] = hm.group("title").strip()
        item["url"] = hm.group("url").strip()
        try:
            item["score"] = float(hm.group("score"))
        except ValueError:
            pass
        if hm.group("rel"):
            try:
                item["relevance"] = float(hm.group("rel"))
            except ValueError:
                pass
        if hm.group("rec"):
            item["rec"] = float(hm.group("rec"))
            item["rec_stars"] = len(hm.group("recstars").replace("\ufe0f", ""))
    else:
        item["title"] = ""
        item["url"] = ""
    item["must_see"] = bool(re.search(r"^#{2,3}\s+🔥", block, re.M))
    sm = STARS_RE.search(block)
    if sm:
        item["stars"] = sm.group(1).strip()
    # summary = 第一段正文（标题行后、信源行前的非空行）
    lines = [ln for ln in block.split("\n") if ln.strip()]
    summary = ""
    for ln in lines[1:]:
        if ln.startswith(("**", "github_trending", "rss", "hackernews", "reddit")):
            break
    else:
        pass
    for ln in lines[1:]:
        if ln.startswith("**") or re.match(r"^(github_trending|rss|hackernews|reddit|telegram|twitter)\b", ln):
            break
        if not summary and not ln.startswith("##"):
            summary = ln
    item["summary"] = summary
    # 信源行
    src = ""
    for ln in lines[1:]:
        if re.match(r"^(github_trending|rss|hackernews|reddit|telegram|twitter)\b", ln):
            src = ln
            break
    item["source_line"] = src[:120]
    # 分栏目
    sections = {}
    cur = None
    for ln in lines:
        m = re.match(r"^\*\*([^*]+)\*\*: (.+)$", ln)
        if m:
            label = m.group(1).strip()
            key = SECTION_LABELS.get(label)
            if key is None and LOCAL_RE.match(label):
                key = "impact_local"
            if key:
                cur = key
                sections[key] = m.group(2).strip()
            elif label == "标签":
                cur = None
        # 分栏目都是单段行，无需续行处理
    item["sections"] = {k: v for k, v in sections.items()}
    # 标签
    for ln in lines:
        tm = TAGS_RE.match(ln)
        if tm:
            item["tags"] = tm.group(1).strip()
    return item


def build_feed(src_dir: Path, date: str) -> dict:
    boards = []
    ok = 0
    total = 0
    for board_id, infix, name in BOARDS:
        path = src_dir / f"{date}-{infix}-zh.md"
        items = []
        if path.is_file():
            ok += 1
            text = path.read_text(encoding="utf-8")
            for block in _parse_blocks(text):
                m = ANCHOR_RE.match(block)
                if not m:
                    continue
                item = _parse_item(block, m.group(1))
                items.append(item)
        boards.append({"id": board_id, "name": name, "items": items})
        total += len(items)
    now = datetime.now(ZoneInfo("Asia/Shanghai"))
    return {
        "version": 1,
        "generated_at": now.isoformat(timespec="seconds"),
        "date": date,
        "total": total,
        "boards_ok": ok,
        "boards": boards,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--src", type=Path, required=True, help="board markdown 目录")
    ap.add_argument("--date", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    feed = build_feed(args.src, args.date)
    if feed["total"] == 0:
        print(f"app feed: no items found for {args.date} in {args.src}")
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.out.with_name(args.out.name + f".tmp.{os.getpid()}" if False else str(os.getpid()))
    tmp.write_text(json.dumps(feed, ensure_ascii=False, separators=(",", ":")),
                   encoding="utf-8")
    os.replace(tmp, args.out)
    print(f"app feed written: {args.out} date={args.date} total={feed['total']}")
    return 0


if __name__ == "__main__":
    import os
    raise SystemExit(main())
