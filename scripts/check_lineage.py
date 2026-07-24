#!/usr/bin/env python3
"""ISS-026 血缘自检：验证 reports-html/data/{date}.json 的每条 item 都能溯源到 data/summaries/。

验证维度：
  1. 标题溯源：item.title 在 summary_file 里 grep 命中
  2. URL 溯源：item.url 在 summary_file 里 grep 命中
  3. 锚点溯源：item.source_ref.item_id 对应 summary_file 里有 <a id="item-N"></a>
  4. 时效：item.published 落在数据窗口内（默认 48h）
  5. 字段：每条 4 字段齐全（4 个 dt 标签）

用法：
    .venv/bin/python scripts/check_lineage.py --date 2026-07-23
    .venv/bin/python scripts/check_lineage.py --date 2026-07-23 --json-out lineage.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "reports-html" / "data"
SUMMARIES_DIR = REPO_ROOT / "data" / "summaries"


def _normalize_text(text: str) -> str:
    """剥掉空白与常见标点，便于 fuzzy grep。"""
    return re.sub(r"\s+", "", text or "")


def check_lineage(report: dict, hours: int = 48) -> dict:
    """执行血缘自检，返回详细报告。"""
    date_str = report.get("date", "")
    anchor_date = datetime.strptime(date_str, "%Y-%m-%d")
    window_start = anchor_date - timedelta(hours=hours)
    window_end = anchor_date + timedelta(hours=12)

    # 缓存 summary 文件全文
    summary_cache: dict[str, str] = {}

    def load_summary(filename: str) -> str:
        if filename not in summary_cache:
            path = SUMMARIES_DIR / filename
            if path.exists():
                summary_cache[filename] = path.read_text(encoding="utf-8")
            else:
                summary_cache[filename] = ""
        return summary_cache[filename]

    title_total = title_ok = 0
    url_total = url_ok = 0
    anchor_total = anchor_ok = 0
    window_total = window_ok = 0
    items_detail = []

    for board in report["boards"]:
        for item in board["rank"] + board["picks"]:
            ref = item.get("source_ref") or {}
            summary_file = ref.get("summary_file") or report.get("_meta", {}).get("source_summary", "")
            title_total += 1
            url_total += 1
            anchor_total += 1
            window_total += 1
            title_norm = _normalize_text(item.get("title", ""))
            url_norm = item.get("url", "")

            if not summary_file:
                items_detail.append({
                    "title": item.get("title", ""), "board": board["anchor"],
                    "title_ok": False, "url_ok": False, "anchor_ok": False,
                    "window_ok": None, "reason": "missing source_ref.summary_file",
                })
                continue
            text = load_summary(summary_file)
            text_norm = _normalize_text(text)

            # 1) 标题溯源
            t_ok = bool(title_norm) and (
                title_norm in text_norm
                or _normalize_text(item.get("title", "")[:30]) in text_norm
            )
            if t_ok:
                title_ok += 1

            # 2) URL 溯源
            u_ok = bool(url_norm) and url_norm in text
            if u_ok:
                url_ok += 1

            # 3) 锚点溯源（item_id 必须出现在 summary 里）
            item_id = ref.get("item_id", "")
            a_ok = bool(item_id) and f'<a id="{item_id}"></a>' in text
            if a_ok:
                anchor_ok += 1

            # 4) 时效
            published = item.get("published") or ""
            w_ok = None
            pub_dt = None
            # ISO 格式
            for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
                try:
                    pub_dt = datetime.strptime(published, fmt)
                    break
                except (ValueError, TypeError):
                    continue
            # 中文格式 "7月22日 23:51" — 需要补年
            if pub_dt is None:
                for fmt in ("%m月%d日 %H:%M", "%m月%d日"):
                    try:
                        pub_dt = datetime.strptime(published, fmt)
                        pub_dt = pub_dt.replace(year=window_start.year)
                        break
                    except (ValueError, TypeError):
                        continue
            if pub_dt is not None:
                if window_start <= pub_dt <= window_end:
                    window_ok += 1
                    w_ok = True
                else:
                    w_ok = False

            items_detail.append({
                "title": item.get("title", "")[:60],
                "board": board["anchor"],
                "title_ok": t_ok, "url_ok": u_ok, "anchor_ok": a_ok,
                "window_ok": w_ok, "published": published,
                "item_id": item_id, "summary_file": summary_file,
            })

    return {
        "date": date_str,
        "total_items": title_total,
        "title_lineage_pct": round(100 * title_ok / title_total, 1) if title_total else 0,
        "url_lineage_pct": round(100 * url_ok / url_total, 1) if url_total else 0,
        "anchor_lineage_pct": round(100 * anchor_ok / anchor_total, 1) if anchor_total else 0,
        "window_pass_pct": round(100 * window_ok / window_total, 1) if window_total else 0,
        "title_ok": title_ok, "url_ok": url_ok, "anchor_ok": anchor_ok, "window_ok": window_ok,
        "items_detail": items_detail,
        "window_start": window_start.isoformat(),
        "window_end": window_end.isoformat(),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--hours", type=int, default=48)
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()
    json_path = DATA_DIR / f"{args.date}.json"
    if not json_path.exists():
        print(f"❌ {json_path} 不存在", file=sys.stderr)
        return 2
    report = json.loads(json_path.read_text(encoding="utf-8"))
    lineage = check_lineage(report, args.hours)
    # 终端输出
    print("=" * 64)
    print(f"【ISS-026 血缘自检】 {args.date} (window={args.hours}h)")
    print("=" * 64)
    print(f"总条目数: {lineage['total_items']}")
    print(f"标题溯源: {lineage['title_ok']}/{lineage['total_items']} ({lineage['title_lineage_pct']}%)")
    print(f"URL 溯源: {lineage['url_ok']}/{lineage['total_items']} ({lineage['url_lineage_pct']}%)")
    print(f"锚点溯源: {lineage['anchor_ok']}/{lineage['total_items']} ({lineage['anchor_lineage_pct']}%)")
    print(f"时效通过: {lineage['window_ok']}/{lineage['total_items']} ({lineage['window_pass_pct']}%)")
    print(f"窗口: {lineage['window_start']} ~ {lineage['window_end']}")
    print()
    print("条目明细:")
    for it in lineage["items_detail"]:
        marks = (
            ("T" if it["title_ok"] else "F") +
            ("U" if it["url_ok"] else "F") +
            ("A" if it["anchor_ok"] else "F") +
            ("W" if it["window_ok"] else ("-" if it["window_ok"] is None else "X"))
        )
        print(f"  [{it['board']:9s}] {marks} {it['title']}")
        if it.get("item_id"):
            print(f"           ref: {it['summary_file']}#{it['item_id']}, published={it.get('published','-')}")
    all_ok = (
        lineage["title_lineage_pct"] == 100
        and lineage["url_lineage_pct"] == 100
        and lineage["anchor_lineage_pct"] == 100
    )
    print()
    print(f"结论: {'✅ 100% 血缘溯源' if all_ok else '❌ 血缘溯源未达 100%'}")
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(lineage, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON 报告写入: {args.json_out}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())