#!/usr/bin/env python3
"""Verify that the four source boards are fully represented in the merged page."""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BOARD_FILES = {
    "global": "global",
    "ai": "horizon",
    "github": "github-trending",
    "ee": "ee",
}
ITEM_START_RE = re.compile(r'<a id="item-(\d+)"></a>')
ITEM_LINK_RE = re.compile(r'\[[^\]]+\]\(https?://[^)]+\)\s*⭐️\s*[\d.]+/10')


def _source_counts(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    starts = list(ITEM_START_RE.finditer(text))
    valid = 0
    for index, match in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
        if ITEM_LINK_RE.search(text[match.start():end]):
            valid += 1
    return len(starts), valid


def verify_four_board_lineage(summaries_dir: Path, date: str) -> dict:
    summaries_dir = summaries_dir.resolve()
    merged_path = summaries_dir / f"{date}-榜单汇总-zh.md"
    merged_text = merged_path.read_text(encoding="utf-8") if merged_path.is_file() else ""
    boards = {}
    reasons = []
    total_items = 0

    for anchor, infix in BOARD_FILES.items():
        source = summaries_dir / f"{date}-{infix}-zh.md"
        if source.is_file():
            source_items, valid_items = _source_counts(source)
        else:
            source_items = valid_items = 0
        merged_items = len(
            re.findall(rf'<a id="item-{re.escape(anchor)}-\d+"></a>', merged_text)
        )
        section_present = f'<a id="sec-{anchor}"></a>' in merged_text
        board_passed = (
            source.is_file()
            and valid_items == source_items
            and merged_items == source_items
            and section_present
        )
        if not board_passed:
            reasons.append(
                f"{anchor}: source={source_items} valid={valid_items} "
                f"merged={merged_items} section={section_present}"
            )
        boards[anchor] = {
            "source_file": source.name,
            "source_items": source_items,
            "valid_items": valid_items,
            "merged_items": merged_items,
            "section_present": section_present,
            "passed": board_passed,
        }
        total_items += source_items

    return {
        "date": date,
        "checked_at": datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(),
        "passed": merged_path.is_file() and not reasons,
        "merged_file": merged_path.name,
        "total_items": total_items,
        "boards": boards,
        "reasons": reasons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", required=True)
    parser.add_argument("--summaries-dir", type=Path, required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    result = verify_four_board_lineage(args.summaries_dir, args.date)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    print(payload)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.json_out.with_name(
            f".{args.json_out.name}.tmp.{os.getpid()}"
        )
        temporary.write_text(payload, encoding="utf-8")
        os.replace(temporary, args.json_out)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
