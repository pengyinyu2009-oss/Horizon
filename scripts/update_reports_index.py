#!/usr/bin/env python3
"""Refresh the four-board navigation index from verified daily lineage.

Beyond the latest-daily block, the index carries 最新周报 / 最近日报 /
周期报历史 sections. Those used to be hand-written in the template and
went stale the moment a new week shipped (the page still advertised
2026-W31 thirteen weeks later), so they are now derived from the report
files that actually sit next to the index — the publish step copies
every summary into the same directory.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import date as date_type
from datetime import timedelta
from pathlib import Path


EXPECTED_BOARDS = {"global", "ai", "github", "ee"}
FRONT_DATE_RE = re.compile(r"(?m)^date:\s*\d{4}-\d{2}-\d{2}\s*$")
LATEST_DAILY_RE = re.compile(
    r"(?ms)^## 📅 最新日报（.*?^---\s*$"
)
LATEST_WEEKLY_RE = re.compile(
    r"(?ms)^## 📅 最新周报（.*?^---\s*$"
)
RECENT_DAILIES_RE = re.compile(
    r"(?ms)^## 🗂 最近日报.*?^---\s*$"
)
PERIOD_HISTORY_RE = re.compile(
    r"(?ms)^## 🗓 周期报历史.*?^---\s*$"
)
PUBLISH_LINE_RE = re.compile(r"(?m)^- \*\*发布\*\*：.*$")
WEEKDAYS_ZH = ("周一", "周二", "周三", "周四", "周五", "周六", "周日")

# Report filenames the roll-up pipeline produces, e.g.
# 2026-W43-周榜-zh.md / 2026-08-月榜-zh.md / 2026-H1-年榜-zh.md
WEEKLY_NAME_RE = re.compile(r"^(?P<pid>\d{4}-W\d{2})-周榜-(?P<lang>[a-z]{2})\.md$")
MONTHLY_NAME_RE = re.compile(r"^(?P<pid>\d{4}-\d{2})-月榜-(?P<lang>[a-z]{2})\.md$")
YEARLY_NAME_RE = re.compile(r"^(?P<pid>\d{4}(?:-H[12])?)-年榜-(?P<lang>[a-z]{2})\.md$")
DAILY_NAME_RE = re.compile(
    r"^(?P<date>\d{4}-\d{2}-\d{2})-(?:global|horizon|github-trending|ee)-zh\.md$"
)
RECENT_DAILY_COUNT = 7


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


# --- period-report discovery ------------------------------------------------


def _iso_monday(pid: str) -> date_type:
    """'2026-W43' -> the Monday of that ISO week."""
    year, week = pid.split("-W")
    return date_type.fromisocalendar(int(year), int(week), 1)


def _weekly_sort_key(pid: str):
    year, week = pid.split("-W")
    return (int(year), int(week))


def _missing_weekly_ids(weeklies: list[str]) -> list[str]:
    """ISO weeks with no report between the first and last available one.

    A hole here is not a rendering bug — it means the underlying dailies
    never existed (the 2026-09-15..10-11 outage left W38-W41 empty), and
    the monthly/yearly chains refuse to build on it. Surfacing the hole
    keeps the index honest instead of silently listing a shorter range.
    """
    if len(weeklies) < 2:
        return []
    present = set(weeklies)
    missing: list[str] = []
    cursor = _iso_monday(min(weeklies, key=_weekly_sort_key))
    last = _iso_monday(max(weeklies, key=_weekly_sort_key))
    while cursor <= last:
        iso_year, iso_week, _ = cursor.isocalendar()
        pid = f"{iso_year}-W{iso_week:02d}"
        if pid not in present:
            missing.append(pid)
        cursor += timedelta(days=7)
    return missing


def _discover_period_reports(posts_dir: Path) -> dict:
    """Scan the directory next to the index for published report files."""
    weeklies: set[str] = set()
    monthlies: set[str] = set()
    yearlies: set[str] = set()
    dailies: set[str] = set()
    for path in posts_dir.glob("*.md"):
        for pattern, bucket in (
            (WEEKLY_NAME_RE, weeklies),
            (MONTHLY_NAME_RE, monthlies),
            (YEARLY_NAME_RE, yearlies),
            (DAILY_NAME_RE, dailies),
        ):
            match = pattern.match(path.name)
            if match:
                bucket.add(match.group("pid") if pattern is not DAILY_NAME_RE else match.group("date"))
                break
    return {
        "weeklies": sorted(weeklies, key=_weekly_sort_key),
        "monthlies": sorted(monthlies),
        "yearlies": sorted(yearlies),
        "dailies": sorted(dailies, reverse=True),
    }


def _report_links(ids: list[str], suffix: str) -> str:
    return " · ".join(f"[{pid}](/reports-html/{pid}-{suffix}.html)" for pid in ids)


def _latest_weekly_section(found: dict) -> str:
    weeklies = found["weeklies"]
    if not weeklies:
        body = "周报待发布（每周一 10:47 BJT 生成上一周）。"
    else:
        latest = weeklies[-1]
        body = (
            f"[**{latest} 周榜汇总**](/reports-html/{latest}-周榜-zh.html)\n"
            "- 4 大榜单周维度聚合 · 跨榜单主线 + 行动建议\n"
            "- 发布：每周一 10:47 BJT（与本报导航同步刷新）"
        )
    return f"""## 📅 最新周报（{weeklies[-1] if weeklies else "待发布"}）

{body}

---"""


def _recent_dailies_section(found: dict) -> str:
    dailies = found["dailies"][:RECENT_DAILY_COUNT]
    if not dailies:
        body = "暂无日报。"
    else:
        body = " · ".join(
            f"[{day[5:]}](/reports-html/{day}.html)" for day in dailies
        )
    return f"""## 🗂 最近日报

{body}

---"""


def _period_history_section(found: dict) -> str:
    weeklies = found["weeklies"]
    monthlies = found["monthlies"]
    yearlies = found["yearlies"]

    weekly_line = (
        _report_links(weeklies, "周榜-zh") if weeklies else "待发布（每周一 10:47 BJT）"
    )
    monthly_line = (
        _report_links(monthlies, "月榜-zh") if monthlies else "待发布（每月 8 号发布上月）"
    )
    if yearlies:
        yearly_line = _report_links(yearlies, "年榜-zh")
    else:
        yearly_line = "待发布（H1 于 7 月 15 日、H2 于次年 1 月 15 日）"

    gaps = _missing_weekly_ids(weeklies)
    gap_line = ""
    if gaps:
        gap_line = (
            f"\n- **缺口**：{' / '.join(gaps)} —— 这些周没有日报数据来源，"
            "依赖周报的月报与年报链会一并跳过（门禁拒绝拿残缺数据拼报告）。"
        )

    return f"""## 🗓 周期报历史

- **周榜**：{weekly_line}
- **月榜**：{monthly_line}
- **年榜**：{yearly_line}{gap_line}

---"""


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
- 共 {lineage['total_items']} 条，统一版式五栏目：入选理由 / 背景 / 对中国影响 / 对沈阳影响 / 对我影响
- 🔥 GitHub 热榜每条另有「对这个项目有什么用」+ 五星推荐
- 数据完整性：4/4 榜单 lineage 校验通过

---"""
    publish_line = (
        "- **发布**：VPS 08:17 BJT 主任务；"
        "10:30 / 21:17 幂等补偿；GitHub Actions 仅手动备用"
    )

    # The publish step copies every summary next to this index, so the
    # period-report sections can be derived from what is really there.
    found = _discover_period_reports(index_path.parent)

    updated = _replace_once(
        FRONT_DATE_RE, f"date: {date}", current, "front-matter date"
    )
    updated = _replace_once(
        LATEST_DAILY_RE, latest_section, updated, "latest daily section"
    )
    updated = _replace_once(
        LATEST_WEEKLY_RE, _latest_weekly_section(found), updated, "latest weekly section"
    )
    updated = _replace_once(
        RECENT_DAILIES_RE, _recent_dailies_section(found), updated, "recent dailies section"
    )
    updated = _replace_once(
        PERIOD_HISTORY_RE, _period_history_section(found), updated, "period history section"
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
