#!/usr/bin/env python3
"""生成 GitHub 热榜页面（docs/github-trending.md）。

数据源：OSSInsight trends API（无需 token）。
周期：过去 24 小时 / 过去一周 / 过去一月。

用法：
    .venv/bin/python scripts/github_trending.py          # 只更新本地文件
    .venv/bin/python scripts/github_trending.py --push   # 更新本地文件并提交到 master（Pages 发布源）
"""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx

API = "https://api.ossinsight.io/v1/trends/repos/"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT = REPO_ROOT / "docs" / "github-trending.md"
TOP_N = 25

PERIODS = [
    ("past_24_hours", "🔥 今日热榜（过去 24 小时）"),
    ("past_week", "📈 本周热榜（过去 7 天）"),
    ("past_month", "🏆 本月热榜（过去 30 天）"),
]

GITHUB_REPO = "pengyinyu2009-oss/Horizon"
PAGES_BRANCH = "master"
PAGES_PATH = "docs/github-trending.md"


def fetch(period: str) -> list[dict]:
    resp = httpx.get(API, params={"period": period}, timeout=30)
    resp.raise_for_status()
    rows = resp.json()["data"]["rows"]
    return rows[:TOP_N]


def esc(text: str) -> str:
    return (text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_table(rows: list[dict]) -> str:
    lines = [
        "| # | 仓库 | 语言 | ⭐ 新增 | Forks | 简介 |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        name = r.get("repo_name", "")
        lang = r.get("primary_language") or "-"
        stars = r.get("stars") or "0"
        forks = r.get("forks") or "0"
        desc = esc(r.get("description") or "")[:80]
        lines.append(
            f"| {i} | [{name}](https://github.com/{name}) | {lang} | {stars} | {forks} | {desc} |"
        )
    return "\n".join(lines)


def build_page(data: dict[str, list[dict]]) -> str:
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")
    parts = [
        "---",
        "layout: default",
        "title: GitHub 热榜",
        "---",
        "",
        "# GitHub 热榜",
        "",
        f"> 数据来源：[OSSInsight](https://ossinsight.io) · 更新于 {now}（北京时间）· 每日自动刷新",
        "",
    ]
    for period, heading in PERIODS:
        parts.append(f"## {heading}")
        parts.append("")
        rows = data.get(period) or []
        if rows:
            parts.append(render_table(rows))
        else:
            parts.append("*暂无数据*")
        parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("[← 返回首页](index)")
    parts.append("")
    return "\n".join(parts)


def push_to_master(content: str) -> None:
    """通过 gh api 把页面提交到 Pages 发布分支 master。"""
    api = f"repos/{GITHUB_REPO}/contents/{PAGES_PATH}"
    sha = None
    probe = subprocess.run(
        ["gh", "api", api, "--jq", ".sha", "-H", f"X-GitHub-Api-Version: 2022-11-28"],
        capture_output=True, text=True,
    )
    # GET 默认 ref 是仓库默认分支(main)，必须指定 master
    probe = subprocess.run(
        ["gh", "api", f"{api}?ref={PAGES_BRANCH}", "--jq", ".sha"],
        capture_output=True, text=True,
    )
    if probe.returncode == 0:
        sha = probe.stdout.strip() or None

    payload = {
        "message": "📊 GitHub trending: daily refresh",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": PAGES_BRANCH,
    }
    if sha:
        payload["sha"] = sha
    result = subprocess.run(
        ["gh", "api", api, "-X", "PUT", "--input", "-"],
        input=json.dumps(payload), capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"push failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(f"pushed to {GITHUB_REPO}@{PAGES_BRANCH}:{PAGES_PATH}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true", help="提交到 master 分支")
    args = parser.parse_args()

    data = {}
    for period, _ in PERIODS:
        try:
            data[period] = fetch(period)
            print(f"{period}: {len(data[period])} repos")
        except Exception as exc:  # noqa: BLE001
            print(f"{period}: fetch failed: {exc}", file=sys.stderr)
            data[period] = []

    page = build_page(data)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else None
    # 对比时忽略「更新于」时间戳行
    def strip_ts(text: str) -> str:
        return "\n".join(l for l in text.splitlines() if not l.startswith("> 数据来源"))

    if old is not None and strip_ts(old) == strip_ts(page) and not args.push:
        print("no change")
        return
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT}")
    if args.push:
        push_to_master(page)


if __name__ == "__main__":
    main()
