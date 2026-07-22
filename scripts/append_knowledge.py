#!/usr/bin/env python3
"""Append a beginner knowledge card to the EE / Embedded daily editions.

Reads ``data/summaries/{date}-{edition}-zh.md``, asks DeepSeek for ONE
foundational concept related to today's items — explained in plain,
beginner-friendly Chinese — and appends it as a 「📚 今日知识点」 section.

Idempotent: skips if the section is already present (safe under force
re-runs). Fail-safe: missing file, missing API key, empty response, or
API failure prints a message and exits 0 so the calling GitHub Actions
step (continue-on-error) never blocks the pipeline.

Usage:
    uv run python scripts/append_knowledge.py --edition ee [--date YYYY-MM-DD]
    uv run python scripts/append_knowledge.py --edition embedded
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAX_CONTENT_CHARS = 12000
SUMMARIES_DIR = Path("data") / "summaries"
KNOWLEDGE_HEADING = "### 📚 今日知识点"

EDITIONS = {
    "ee": "电源/电子工程（电路、元器件、电源设计、测量仪器）",
    "embedded": "嵌入式（单片机、固件、总线、RTOS、调试）",
}

SYSTEM_PROMPT = (
    "你是一位擅长给零基础读者讲解的技术科普作者。读者是{domain}领域的"
    "初学者（自称小白），目标是每天进步一点点。你的输出会被直接追加到"
    "一篇 Markdown 日报末尾。"
)

USER_PROMPT_TEMPLATE = """以下是今天「{domain}」日报的 Markdown 内容（超长时已按条目截断为标题+首段）：

---
{content}
---

请从今天的新闻里挑 1 个最基础、最值得初学者掌握的概念，用简体中文输出一段 Markdown，严格使用以下格式（一个三级标题 + 四个加粗小项），不要输出任何其他内容：

### 📚 今日知识点
**概念**：概念名称
**是什么**：3-5 句大白话解释，零基础也能看懂，可以带一个生活类比
**和今天新闻的关系**：1-2 句，点明它出现在今天哪条新闻里、起什么作用
**延伸关键词**：3-5 个方便自学的搜索关键词，用顿号隔开"""


def condense_markdown(text: str, max_chars: int = MAX_CONTENT_CHARS) -> str:
    """Shrink a long report to front matter + headings + first paragraphs.

    Keeps the Jekyll front matter block (if any), every heading line, and
    the first non-empty paragraph after each heading, so the model still
    sees every item's title and gist. Hard-truncates at max_chars.
    """
    lines = text.splitlines()
    out = []
    i = 0
    n = len(lines)
    # Preserve Jekyll front matter verbatim (--- ... ---).
    if lines and lines[0].strip() == "---":
        while i < n:
            out.append(lines[i])
            i += 1
            if i > 1 and lines[i - 1].strip() == "---":
                break
    while i < n:
        line = lines[i]
        if line.lstrip().startswith("#"):
            out.append(line)
            i += 1
            paragraph = []
            while i < n:
                nxt = lines[i]
                if nxt.strip() == "":
                    if paragraph:
                        break
                    i += 1
                    continue
                if nxt.lstrip().startswith("#"):
                    break
                paragraph.append(nxt)
                i += 1
            out.extend(paragraph)
            out.append("")
        else:
            i += 1
    return "\n".join(out)[:max_chars]


def main() -> int:
    parser = argparse.ArgumentParser(description="Append daily knowledge card")
    parser.add_argument("--edition", required=True, choices=sorted(EDITIONS))
    parser.add_argument(
        "--date",
        default=None,
        help="Report date YYYY-MM-DD (default: today, Asia/Shanghai)",
    )
    args = parser.parse_args()

    date = args.date or datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    path = SUMMARIES_DIR / f"{date}-{args.edition}-zh.md"
    if not path.exists():
        print(f"[append_knowledge] {path} not found, skipping.")
        return 0

    content = path.read_text(encoding="utf-8")
    if KNOWLEDGE_HEADING in content:
        print(f"[append_knowledge] knowledge card already present in {path}, skipping.")
        return 0
    if len(content) > MAX_CONTENT_CHARS:
        content = condense_markdown(content, MAX_CONTENT_CHARS)
        print(f"[append_knowledge] condensed report to {len(content)} chars")

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("[append_knowledge] DEEPSEEK_API_KEY not set, skipping.")
        return 0

    domain = EDITIONS[args.edition]
    try:
        # NOTE: plain OpenAI client on purpose — src/ai/client.py forces
        # response_format={"type": "json_object"} for deepseek, which would
        # corrupt this free-form Markdown output.
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT.format(domain=domain)},
                {
                    "role": "user",
                    "content": USER_PROMPT_TEMPLATE.format(domain=domain, content=content),
                },
            ],
            temperature=0.4,
            max_tokens=900,
        )
        text = (resp.choices[0].message.content or "").strip()
    except Exception as exc:
        print(f"[append_knowledge] DeepSeek call failed: {exc}")
        return 0

    if not text or KNOWLEDGE_HEADING not in text:
        print("[append_knowledge] empty or malformed response, skipping.")
        return 0

    with path.open("a", encoding="utf-8") as f:
        f.write("\n\n---\n\n" + text + "\n")
    print(f"[append_knowledge] appended knowledge card to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
