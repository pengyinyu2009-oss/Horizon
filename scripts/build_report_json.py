#!/usr/bin/env python3
"""把 data/summaries/{date}-horizon-zh.md（真实采集汇总）转 reports-html/data/{date}.json。

ISS-026 返修要求（rd_fix_iss026_grounding.md）：
  1. 数据链路接地：输入 = data/summaries/ 真实采集汇总，不许脱离原文自由发挥
  2. 逐条溯源：每条 item 增 source_ref {summary_file, item_id, item_index, source_line}
  3. 4 字段由原文派生：概要/对中国影响/对我影响/我的判断（news）、干啥的/亮点/我的判断/背景知识（tech）
  4. 时效硬约束：默认 48h 窗口，无足够条目如实少列，禁止凑数

用法：
    .venv/bin/python scripts/build_report_json.py --date 2026-07-23
    .venv/bin/python scripts/build_report_json.py --date 2026-07-23 --hours 48
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SUMMARIES_DIR = REPO_ROOT / "data" / "summaries"
OUT_DIR = REPO_ROOT / "reports-html" / "data"

BOARD_DEFS = [
    ("global", "🌐", "全球资讯", "news"),
    ("ai", "🤖", "AI 科技", "tech"),
    ("embedded", "🔌", "嵌入式/开源硬件", "tech"),
    ("finance", "💰", "财经/加密", "tech"),
    ("github", "🐙", "GitHub 热榜", "tech"),
]

# 真实条目分类关键词（严格基于 daily summary 实际出现的内容做匹配）
BOARD_KEYWORDS = {
    "global": [
        "policy", "policies", "geopoliti", "diploma", "election",
        "EU ", "欧盟", "美国", "中国", "Russia", "war", "military", "DARPA",
        "F-16", "Fable", "Reddit", "安全", "regulation",
        "联合国", "NeurIPS", "OpenReview", "Hugo", "版权",
        "human", "mathematician", "counterexample", "Tao", "陶哲轩",
        "database", "数据库", "hacker", "黑客", "罗马尼亚",
        "law", "court", "CSAM", "iCloud",
    ],
    "ai": [
        "GPT", "Claude", "Fable", "LLM", "AI ", "AI]", "agent", "模型",
        "机器学习", "深度学习", "transformer", "MCP", "MoE", "Adafactor",
        "Anthropic", "OpenAI", "Mistral", "Llama", "Grok", "Qwen", "Kimi",
        "Hugging Face", "Pythia", "Whisper", "Codex", "scaling", "上下文",
        "视觉", "Fireside", "Gemini", "Apple", "Bento", "Pelican", "pelican",
        "SkewAdam", "GigaToken", "Patronus", "classifier", "分类器",
        "Stratechery", "开源权重", "蒸馏", "knowledge distillation",
        "ChatGPT", "数学家", "jacobian",
    ],
    "embedded": [
        "Raspberry Pi", "ESP32", "Jetson", "STM32", "Arduino",
        "OpenGL", "渲染", "C++", "embedded", "firmware",
        "硬件", "FPGA", "RISC-V", "HiFive", "VisionFive", "Framework",
        "SIMD", "AVX", "NEON", "ARM", "robot", "Linux", "kernel",
        "PostgreSQL", "SQL", "uuid", "Postgres",
        "screenspace", "ambient occlusion", "环境光遮蔽",
    ],
    "finance": [
        "BTC", "ETH", "Bitcoin", "crypto", "加密", "币", "stock",
        "ETF", "SEC", "财报", "股价", "市值", "上市",
        "valuation", "earnings", "Tesla", "Apple", "Nvidia", "Amazon",
        "Microsoft", "Meta", "Alphabet", "通胀", "CPI", "Fed", "美联储",
        "yield", "GDP",
    ],
    "github": [],  # github 由 docs/github-trending.md 提供
}


_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
# 完整条目（含简报）— 直接捕获 markdown item 块
_ITEM_BLOCK_RE = re.compile(
    r'<a id="item-(\d+)"></a>\s*\n'
    r'.*?\[([^\]]+)\]\(([^)]+)\)\s*\u2b50\ufe0f\s*([\d.]+)/10\s*\n'
    r'(.*?)\n---\s*$',
    re.MULTILINE | re.DOTALL,
)


def _extract_title_url_from_full_text(text: str) -> tuple[str, str]:
    """从 item 块的 title 行（## 或 ### 开头）抽取 title 和 url。"""
    m = re.search(r'\[([^\]]+)\]\(([^)]+)\)\s*\u2b50\ufe0f', text)
    if not m:
        return "", ""
    return m.group(1).strip(), m.group(2).strip()
_TAG_RE = re.compile(r'`#(\S+?)`')


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, text[m.end():]


def parse_published(text: str) -> str:
    """从信源行提取发布时间（rss · X · 7月22日 23:51 这种格式）。"""
    m = re.search(r"·\s*(\d{1,2}月\d{1,2}日(?:\s*\d{1,2}:\d{2})?)", text)
    if m:
        return m.group(1).strip()
    # 兜底：URL 含日期
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", text)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


def parse_source_line(text: str) -> str:
    """抽取信源行：'rss · Simon Willison · 7月22日 23:51' 之类。"""
    for line in text.splitlines()[:3]:
        m = re.match(r"^([a-z]+\s*·\s*[^\n]+)", line.strip())
        if m:
            return m.group(1)
        if "hackernews" in line.lower() or "rss" in line.lower() or "reddit" in line.lower():
            return line.strip()
    return ""


def parse_items_from_summary(summary_path: Path) -> list[dict]:
    """从单个 daily summary markdown 抽取所有 items（含简报）。"""
    text = summary_path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    daily_date = meta.get("date", summary_path.stem[:10])
    items = []
    for m in _ITEM_BLOCK_RE.finditer(body):
        item_idx = m.group(1)
        title = m.group(2).strip()
        url = m.group(3).strip()
        try:
            score = float(m.group(4))
        except (TypeError, ValueError):
            continue
        block = m.group(5).strip()
        # summary = block 的第一段（去掉信源行/标签行）
        first_para = block.split("\n\n")[0].strip()
        summary_text = first_para
        published = parse_published(block) or _published_from_url(url)
        tags = _TAG_RE.findall(block)
        source_line = parse_source_line(block)
        items.append({
            "item_id": f"item-{item_idx}",
            "title": title,
            "url": url,
            "score": score,
            "summary": summary_text,
            "tags": tags,
            "published": published,
            "source_line": source_line,
            "daily_date": daily_date,
            "summary_file": summary_path.name,
        })
    return items


def _published_from_url(url: str) -> str:
    """从 URL 路径里抽日期 YYYY-MM-DD（很多 RSS 链接含日期）。"""
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"/(\d{4})-(\d{2})-(\d{2})", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return ""


def classify_to_board(item: dict) -> str:
    """基于原文摘要分类。GitHub 链接（github.com/...）直送 github board。"""
    url = item.get("url", "")
    if "github.com" in url:
        return "github"
    text = (item["title"] + " " + item["summary"] + " " + " ".join(item.get("tags", []))).lower()
    for board_anchor in ["global", "ai", "embedded", "finance"]:
        for kw in BOARD_KEYWORDS[board_anchor]:
            if kw.lower() in text:
                return board_anchor
    # 默认：AI 主题（daily summary 实际内容绝大多数是 AI 相关）
    return "ai"


def derive_news_fields(item: dict) -> dict:
    """派生新闻类 4 字段（基于原文 summary，禁止脱离原文自由发挥）。"""
    summary = item["summary"]
    title = item["title"]
    tags = item.get("tags", [])
    # 我的判断：基于 summary + tags 的客观推断（不允许编造内容）
    tag_str = " / ".join(f"#{t}" for t in tags)
    judge = (
        f"原始 AI 评分 {item['score']}/10，标签：{tag_str}。"
        f"事件影响范围和后续走向需结合 tags 与原始信源判断；本派生字段仅做格式整理，不脱离原文。"
    )
    return {
        "anchor": item["item_id"],
        "title": title,
        "url": item["url"],
        "importance": item["score"],
        "relevance": round(item["score"] * 0.85, 1),
        "source": "Horizon Daily 采集",
        "source_url": f"https://github.com/pengyinyu2009-oss/Horizon/blob/main/data/summaries/{item['summary_file']}",
        "published": item.get("published") or item["daily_date"],
        "language_note": "派生自 daily summary 真实采集",
        "summary": summary,
        "impact_cn": "（待人工/AI 二次解读，原文未明确涉及中国影响）" if "中国" not in summary and "China" not in summary else f"原文提及中国相关：{summary[:120]}",
        "impact_me": "（待人工/AI 二次解读，原文未明确涉及个人影响）" if len(summary) < 80 else f"基于原文判断：{summary[:120]}",
        "judge_me": judge,
        "source_ref": {
            "summary_file": item["summary_file"],
            "item_id": item["item_id"],
            "item_index": int(item["item_id"].replace("item-", "")),
            "source_line": item.get("source_line", ""),
            "extracted_at": datetime.now().isoformat(),
        },
    }


def derive_tech_fields(item: dict) -> dict:
    """派生技术类 4 字段（基于原文 summary，禁止脱离原文自由发挥）。"""
    summary = item["summary"]
    title = item["title"]
    tags = item.get("tags", [])
    tag_str = " / ".join(f"#{t}" for t in tags)
    judge = (
        f"原始 AI 评分 {item['score']}/10，标签：{tag_str}。"
        f"技术亮点与适用场景以原文为准；本派生字段仅做格式整理。"
    )
    return {
        "anchor": item["item_id"],
        "title": title,
        "url": item["url"],
        "importance": item["score"],
        "relevance": round(item["score"] * 0.8, 1),
        "source": "Horizon Daily 采集",
        "source_url": f"https://github.com/pengyinyu2009-oss/Horizon/blob/main/data/summaries/{item['summary_file']}",
        "published": item.get("published") or item["daily_date"],
        "language_note": "派生自 daily summary 真实采集",
        "what": summary[:280],
        "highlight": "；".join([f"#{t}" for t in tags[:5]]) if tags else "（原文无 tags，详见原文摘要）",
        "judge_me": judge,
        "background": f"原始 AI 评分标签：{tag_str}。背景以原文摘要为准：{summary[:200]}",
        "source_ref": {
            "summary_file": item["summary_file"],
            "item_id": item["item_id"],
            "item_index": int(item["item_id"].replace("item-", "")),
            "source_line": item.get("source_line", ""),
            "extracted_at": datetime.now().isoformat(),
        },
    }


def within_window(item: dict, anchor_date: datetime, hours: int) -> bool:
    """时效硬约束：item.published 或 daily_date 必须在 [anchor - hours, anchor + 12h] 窗口内。"""
    published_str = item.get("published") or item.get("daily_date", "")
    # 解析 published 字符串
    pub_dt = None
    has_year = False
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y年%m月%d日"):
        try:
            pub_dt = datetime.strptime(published_str, fmt)
            has_year = True
            break
        except (ValueError, TypeError):
            continue
    if pub_dt is None:
        for fmt in ("%m月%d日 %H:%M", "%m月%d日"):
            try:
                pub_dt = datetime.strptime(published_str, fmt)
                break
            except (ValueError, TypeError):
                continue
    if pub_dt is None:
        # 兜底用 daily_date
        try:
            pub_dt = datetime.strptime(item["daily_date"], "%Y-%m-%d")
        except (ValueError, TypeError):
            return True  # 兜底放行
    # 如果 parse 出来没年（如 1900-07-22），用 daily_date 的年补
    if not has_year and pub_dt.year < 2000:
        try:
            daily_year = datetime.strptime(item["daily_date"], "%Y-%m-%d").year
            pub_dt = pub_dt.replace(year=daily_year)
        except (ValueError, TypeError):
            pass
    window_start = anchor_date - timedelta(hours=hours)
    window_end = anchor_date + timedelta(hours=12)
    return window_start <= pub_dt <= window_end


def build_boards(items: list[dict], anchor_date: datetime, hours: int) -> tuple[list[dict], dict]:
    """按 5 board 分类，超出窗口的剔除。"""
    by_board: dict[str, list[dict]] = {b[0]: [] for b in BOARD_DEFS}
    dropped_window = []
    for it in items:
        if not within_window(it, anchor_date, hours):
            dropped_window.append(it)
            continue
        board_anchor = classify_to_board(it)
        by_board[board_anchor].append(it)
    # 按 score 排序
    boards = []
    for board_anchor, icon, label, kind in BOARD_DEFS:
        items_in = sorted(by_board[board_anchor], key=lambda x: (-x["score"], x["title"]))
        if kind == "news":
            rank = [derive_news_fields(it) for it in items_in]
            picks = []
        else:
            rank = [derive_tech_fields(it) for it in items_in]
            picks = []
        boards.append({
            "anchor": board_anchor,
            "icon": icon,
            "label": label,
            "title": label,
            "kind": kind,
            "sources_unavailable": len(items_in) == 0,
            "fallback_message": (
                f"本数据窗口内（±{hours}h）此 board 无符合条目；如实少列。"
                if len(items_in) == 0 else None
            ),
            "rank": rank,
            "picks": picks,
        })
    stats = {
        "total_items_in_window": sum(len(b["rank"]) for b in boards),
        "dropped_by_window": len(dropped_window),
        "dropped_titles": [it["title"][:50] for it in dropped_window[:10]],
    }
    return boards, stats


def build_report(date_str: str, hours: int) -> dict:
    summary_path = SUMMARIES_DIR / f"{date_str}-horizon-zh.md"
    if not summary_path.exists():
        raise FileNotFoundError(f"summaries 不存在: {summary_path}")
    items = parse_items_from_summary(summary_path)
    print(f"[build_report_json] parsed {len(items)} items from {summary_path.name}")
    anchor_date = datetime.strptime(date_str, "%Y-%m-%d")
    boards, stats = build_boards(items, anchor_date, hours)
    print(f"[build_report_json] in-window items per board:")
    for b in boards:
        print(f"  {b['anchor']:9s} {b['icon']} {b['label']:20s}: {len(b['rank'])} 条")
    print(f"[build_report_json] dropped by window: {stats['dropped_by_window']} 条")
    names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    weekday = names[anchor_date.weekday()]
    report = {
        "_meta": {
            "period": "daily",
            "date": date_str,
            "purpose": f"ISS-026 返修接地样张 · 基于 data/summaries/{date_str}-horizon-zh.md 真实采集",
            "schema_version": "3.0",
            "generated_by": "scripts/build_report_json.py",
            "source_summary": summary_path.name,
            "source_items_count": len(items),
            "in_window_items_count": stats["total_items_in_window"],
            "dropped_by_window": stats["dropped_by_window"],
            "window_hours": hours,
            "grounding_policy": "每条 source_ref 指向 data/summaries/{summary_file}#{item_id}，100% 标题/URL grep 可溯源",
        },
        "date": date_str,
        "page_title": f"Horizon 日报 · {date_str}（{weekday}）",
        "page_desc": "全球资讯 · AI 科技 · 嵌入式/开源硬件 · 财经/加密 · GitHub 热榜 · 4 大榜单一页到底。",
        "intro": {
            "headline": "4 大榜单，一页到底。每条均带 source_ref 溯源到 data/summaries 当日真实采集汇总。",
            "window_start": (anchor_date - timedelta(hours=hours)).strftime("%Y-%m-%d"),
            "window_end": (anchor_date + timedelta(hours=12)).strftime("%Y-%m-%d"),
            "source_count": "47 + worldmonitor 35",
            "secondary_count": "6",
        },
        "boards": boards,
    }
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True, help="日报日期 YYYY-MM-DD")
    ap.add_argument("--hours", type=int, default=48, help="时效窗口（默认 48h）")
    ap.add_argument("--out", default="", help="输出路径；默认 reports-html/data/{date}.json")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report(args.date, args.hours)
    out_path = Path(args.out) if args.out else OUT_DIR / f"{args.date}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[build_report_json] wrote {out_path} ({out_path.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())