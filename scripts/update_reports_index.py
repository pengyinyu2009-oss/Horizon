#!/usr/bin/env python3
"""Refresh the four-board navigation index from verified daily lineage."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date as date_type
from pathlib import Path


EXPECTED_BOARDS = {"global", "ai", "github", "ee"}
FRONT_DATE_RE = re.compile(r"(?m)^date:\s*\d{4}-\d{2}-\d{2}\s*$")
LATEST_DAILY_RE = re.compile(
    r"(?ms)^## 📅 最新日报（.*?^---\s*$"
)
PUBLISH_LINE_RE = re.compile(r"(?m)^- \*\*发布\*\*：.*$")
WEEKDAYS_ZH = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")


class IndexUpdateError(RuntimeError):
    """Raised when an index cannot be safely refreshed."""


def _verified_lineage(lineage_path: Path, expected_date: str) -> dict:
    try:
        lineage = json.loads(lineage_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise IndexUpdateError(f"invalid lineage file: {lineage_path}") from exc

    boards = lineage.get("boards")
    if (
        lineage.get("date") != expected_date
        or lineage.get("passed") is not True
        or not isinstance(lineage.get("total_items"), int)
        or lineage["total_items"] <= 0
        or not isinstance(boards, dict)
        or set(boards) != EXPECTED_BOARDS
        or any(board.get("passed") is not True for board in boards.values())
    ):
        raise IndexUpdateError(
            f"lineage is not a verified four-board result for {expected_date}"
        )
    return lineage


def _replace_once(pattern: re.Pattern, replacement: str, text: str, label: str) -> str:
    updated, count = pattern.subn(replacement, text, count=1)
    if count != 1:
        raise IndexUpdateError(f"index is missing a unique {label} marker")
    return updated


def update_reports_index(index_path: Path, date: str, lineage_path: Path) -> None:
    """Atomically update the navigation index for one verified daily report."""
    try:
        parsed_date = date_type.fromisoformat(date)
        current = index_path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        raise IndexUpdateError(f"cannot read navigation index for {date}") from exc

    lineage = _verified_lineage(lineage_path, date)
    weekday = WEEKDAYS_ZH[parsed_date.weekday()]
    latest_section = f"""## 📅 最新日报（{date} {weekday}）

[**{date} 4 榜单汇总**](/reports-html/{date}.html)
- 🌍 全球新闻 · 🤖 Horizon 总榜 · 🔥 GitHub 热榜（日 / 周 / 月）· 🔧 电子工程师
- 共 {lineage['total_items']} 条，每条双评分 + 入选理由
- 数据完整性：4/4 榜单 lineage 校验通过

---"""
    publish_line = (
        "- **发布**：VPS 08:17 BJT 主任务；"
        "10:30 / 21:17 幂等补偿；GitHub Actions 仅手动备用"
    )

    updated = _replace_once(
        FRONT_DATE_RE, f"date: {date}", current, "front-matter date"
    )
    updated = _replace_once(
        LATEST_DAILY_RE, latest_section, updated, "latest daily section"
    )
    updated = _replace_once(
        PUBLISH_LINE_RE, publish_line, updated, "publication description"
    )

    temporary = index_path.with_name(f".{index_path.name}.tmp.{os.getpid()}")
    temporary.write_text(updated, encoding="utf-8")
    os.replace(temporary, index_path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--lineage", type=Path, required=True)
    args = parser.parse_args()

    update_reports_index(args.index, args.date, args.lineage)
    print(f"reports index updated date={args.date}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
