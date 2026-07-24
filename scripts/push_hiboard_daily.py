#!/usr/bin/env python3
"""把 Horizon 每日日报推送到鸿蒙负一屏（通过 today-task 技能）。

用法：
    .venv/bin/python scripts/push_hiboard_daily.py                # 推送今天的日报
    .venv/bin/python scripts/push_hiboard_daily.py --date 2026-07-20
    .venv/bin/python scripts/push_hiboard_daily.py --test         # 发送一条测试卡片

成功退出码 0，失败非 0。日报不存在或推送失败都会明确报错。
"""

import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_PUSH = ROOT / "skills" / "today-task" / "scripts" / "task_push.py"
VENV_PY = ROOT / ".venv" / "bin" / "python"
SITE = "https://horizon.pyyaiai.com"  # apex/www 的 /2026/... 日报链接曾 404；日报内容统一走 horizon 子域

STATS_RE = re.compile(r"^>\s*(从\s*\d+\s*条内容中筛选出\s*\d+\s*条重要资讯。)", re.M)
DETAIL_RE = re.compile(r"其中\s*\*\*(\d+)\s*条\s*8\s*分以上\*\*")
INDEX_RE = re.compile(r"^\d+\.\s+\[(.+?)\]\(#item-\d+\)\s*⭐️\s*([\d.]+)", re.M)


def build_digest(date_str: str, md: str) -> tuple[str, str, str]:
    """从日报 markdown 提取摘要卡片内容。返回 (task_name, task_content, task_result)"""
    stats_m = STATS_RE.search(md)
    stats = stats_m.group(1).rstrip("。") if stats_m else "今日日报已生成"
    detail_m = DETAIL_RE.search(md)
    detail = f"，其中 {detail_m.group(1)} 条 8 分以上详报" if detail_m else ""

    items = INDEX_RE.findall(md)
    lines = [f"{i}. ⭐{score} {title}" for i, (title, score) in enumerate(items, 1)]
    index_block = "\n".join(lines) if lines else "（未解析到索引）"

    # 负一屏 webview 不跑 JS：必须指 reports-html 静态页，不能指 docsify 壳
    # （/YYYY/MM/DD/horizon-zh.html 会永远「加载中」）
    post_url = f"{SITE}/reports-html/{date_str}.html"
    # 合并日页内 GitHub 热榜段锚点（render 产物为同日 {date}.html）
    oshw_url = f"{SITE}/reports-html/{date_str}.html#oshw"

    task_name = f"Horizon 每日日报 · {date_str}"
    task_content = (
        f"# 📰 Horizon 每日日报 · {date_str}\n\n"
        f"{stats}{detail}。\n\n"
        f"{index_block}\n\n"
        f"---\n"
        f"[阅读完整日报]({post_url}) · [GitHub 热榜]({oshw_url})"
    )
    # 负一屏卡片不宜过长，安全截断（技能默认上限 5000）
    if len(task_content) > 4500:
        task_content = task_content[:4500] + "\n…（更多见完整日报）"

    task_result = f"已生成 · {len(items)} 条入选" if items else "已生成"
    return task_name, task_content, task_result


def push(task_name: str, task_content: str, task_result: str) -> int:
    payload = {
        "task_name": task_name,
        "task_content": task_content,
        "task_result": task_result,
    }
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", prefix="horizon_push_", delete=False, encoding="utf-8"
    ) as f:
        json.dump(payload, f, ensure_ascii=False)
        tmp = f.name
    try:
        proc = subprocess.run(
            [str(VENV_PY), str(SKILL_PUSH), "--data", tmp],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(ROOT),
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        print(out.strip())
        ok = proc.returncode == 0 and ("推送成功" in out or "success" in out.lower())
        if not ok:
            print(f"❌ 推送失败（exit {proc.returncode}）", file=sys.stderr)
            return 1
        return 0
    finally:
        Path(tmp).unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="推送 Horizon 日报到鸿蒙负一屏")
    ap.add_argument("--date", default=datetime.now().strftime("%Y-%m-%d"), help="日报日期 YYYY-MM-DD")
    ap.add_argument("--test", action="store_true", help="发送测试卡片")
    args = ap.parse_args()

    if args.test:
        now = datetime.now().strftime("%H:%M")
        return push(
            "Horizon 推送测试",
            f"# ✅ Horizon 负一屏推送测试\n\n通道已打通，每天 08:17 日报生成后将自动推送到这里。\n\n测试时间：{args.date} {now}",
            "测试成功",
        )

    md_path = ROOT / "data" / "summaries" / f"{args.date}-horizon-zh.md"
    if not md_path.exists():
        print(f"❌ 日报不存在: {md_path}", file=sys.stderr)
        return 2
    name, content, result = build_digest(args.date, md_path.read_text(encoding="utf-8"))
    return push(name, content, result)


if __name__ == "__main__":
    sys.exit(main())
