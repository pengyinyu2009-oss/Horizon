#!/usr/bin/env python3
"""Merge the four per-board daily summaries into one {date}-榜单汇总-zh.md.

Boards (2026-07-28 four-board system):
  sec-global  ← {date}-global-zh.md           🌍 全球新闻
  sec-ai      ← {date}-horizon-zh.md          🤖 Horizon 总榜
  sec-github  ← {date}-github-trending-zh.md  🔥 GitHub 热榜（日/周/月子榜）
  sec-ee      ← {date}-ee-zh.md               🔧 电子工程师

Per board the script:
  - strips the Jekyll front matter
  - drops the board's own H1 (kept when it is a 【评分故障空报】 banner)
  - namespaces item anchors (item-3 → item-global-3, incl. TOC links)
    so all four boards can coexist on one page
  - demotes every heading one level to fit under the section header

A missing board becomes a placeholder section instead of failing the
merge; only when ALL boards are missing does the script exit 1.

Usage:
    uv run python scripts/merge_boards.py --date 2026-07-28
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

SUMMARIES_DIR = Path("data") / "summaries"

# (anchor, source-file infix, section label)
BOARDS = [
    ("global", "global", "🌍 全球新闻"),
    ("ai", "horizon", "🤖 Horizon 总榜"),
    ("github", "github-trending", "🔥 GitHub 热榜"),
    ("ee", "ee", "🔧 电子工程师"),
]

_HEADING_RE = re.compile(r"^(#{1,5})\s")
_ITEM_COUNT_RE = re.compile(r'<a id="item-')


def _strip_front_matter(text: str) -> str:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text


def _demote_and_namespace(body: str, anchor: str) -> str:
    """Namespace item anchors and demote headings (code-fence aware)."""
    body = body.replace('<a id="item-', f'<a id="item-{anchor}-')
    body = body.replace("](#item-", f"](#item-{anchor}-")

    out_lines = []
    in_fence = False
    for line in body.split("\n"):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if not in_fence:
            m = _HEADING_RE.match(line)
            if m:
                line = "#" + line
        out_lines.append(line)
    return "\n".join(out_lines)


def _drop_board_h1(body: str) -> str:
    """Drop the board's own H1 (redundant under the section header).

    Scoring-failure banners (【评分故障空报】) are kept — demoted like
    every other heading — because they ARE the board's content.
    """
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        if line.startswith("# ") and "【评分故障空报】" not in line:
            del lines[i]
            # swallow the blank line right after the dropped H1
            if i < len(lines) and not lines[i].strip():
                del lines[i]
        break
    return "\n".join(lines)


def merge_boards(date: str, summaries_dir: Path) -> tuple[str, list[str]]:
    """Build the merged markdown; returns (markdown, missing_boards)."""
    missing = []
    sections = []
    for anchor, infix, label in BOARDS:
        path = summaries_dir / f"{date}-{infix}-zh.md"
        if not path.exists():
            missing.append(anchor)
            sections.append(
                f'<a id="sec-{anchor}"></a>\n'
                f"## {label}\n\n"
                f"⚠️ 今日该榜单未生成（生成步骤失败，详见 pipeline 告警）。\n"
            )
            continue
        body = _strip_front_matter(path.read_text(encoding="utf-8"))
        n_items = len(_ITEM_COUNT_RE.findall(body))
        body = _drop_board_h1(body)
        body = _demote_and_namespace(body, anchor)
        count_label = f"（{n_items} 条）" if n_items else ""
        sections.append(
            f'<a id="sec-{anchor}"></a>\n'
            f"## {label}{count_label}\n\n"
            f"{body.strip()}\n"
        )

    nav = " · ".join(f"[{label}](#sec-{anchor})" for anchor, _, label in BOARDS)
    header = f"""---
layout: default
title: "Horizon 日报(4 榜单):{date} (ZH)"
date: {date}
lang: zh
period: daily
period_id: {date}
---

> **4 大榜单，一页到底。** 🌍 全球新闻（每条含对中国影响 / 对我影响）· 🤖 Horizon 总榜 · 🔥 GitHub 热榜（日 / 周 / 月三子榜）· 🔧 电子工程师（值得复刻与学习）。
> 每条双评分：⭐️ 客观分（事件重要性）· 相关分（与你画像的相关性）；每榜取客观分前 10 + 🎯 猜你感兴趣 3 条。
>
> 📑 跳转到: {nav}

---

# Horizon 日报 · {date}

---

"""
    return header + "\n---\n\n".join(sections) + "\n", missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--date",
        default=datetime.now(ZoneInfo("Asia/Shanghai")).strftime("%Y-%m-%d"),
    )
    parser.add_argument("--summaries-dir", type=Path, default=SUMMARIES_DIR)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()

    out_path = args.out or (
        args.summaries_dir / f"{args.date}-榜单汇总-zh.md"
    )
    markdown, missing = merge_boards(args.date, args.summaries_dir)
    if len(missing) == len(BOARDS):
        print(f"merge_boards: all {len(BOARDS)} boards missing for {args.date}", file=sys.stderr)
        return 1
    if missing:
        print(f"merge_boards: WARNING missing boards: {', '.join(missing)}")
    out_path.write_text(markdown, encoding="utf-8")
    print(f"merge_boards: wrote {out_path} ({len(BOARDS) - len(missing)}/{len(BOARDS)} boards)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
