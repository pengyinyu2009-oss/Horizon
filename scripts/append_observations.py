#!/usr/bin/env python3
"""Append cross-item observations to the OSHW daily edition.

Reads ``data/summaries/{date}-oshw-zh.md``, asks DeepSeek for (1) shared
trends across the listed projects and (2) persona-based takeaways, then
appends the two Markdown sections to the same file, separated by ``---``.

Fail-safe by design: a missing file, missing API key, empty response, or
API failure prints a message and exits 0 so the calling GitHub Actions
step (continue-on-error) never blocks the pipeline.

Usage:
    uv run python scripts/append_observations.py [--date YYYY-MM-DD]
"""

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

MAX_CONTENT_CHARS = 12000
SUMMARIES_DIR = Path("data") / "summaries"

SYSTEM_PROMPT = (
    "你是一位中文技术编辑，服务喜欢动手复刻开源项目的技术读者。"
    "你的输出会被直接追加到一篇 Markdown 日报末尾。"
)

USER_PROMPT_TEMPLATE = """以下是今天「开源硬件榜单」日报的 Markdown 内容（超长时已按条目截断为标题+首段）：

---
{content}
---

请通读后输出两段中文 Markdown，严格使用以下两个三级标题，且不要输出任何其他内容：

### 🧭 共性观察
用无序列表写 2-4 条这期榜单项目的共性趋势（每条 1-2 句话）。

### 💡 复刻与学习价值
用无序列表写 2-4 条这期项目/趋势对想动手复刻或学习新技术的读者的具体好处（从项目质量、学习曲线、可复刻性等角度自己判断，不预设读者背景）。"""


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
    parser = argparse.ArgumentParser(description="Append OSHW observations")
    parser.add_argument(
        "--date",
        default=None,
        help="Report date YYYY-MM-DD (default: today, Asia/Shanghai)",
    )
    args = parser.parse_args()

    date = args.date or datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")
    path = SUMMARIES_DIR / f"{date}-oshw-zh.md"
    if not path.exists():
        print(f"[append_observations] {path} not found, skipping.")
        return 0

    content = path.read_text(encoding="utf-8")
    if len(content) > MAX_CONTENT_CHARS:
        content = condense_markdown(content, MAX_CONTENT_CHARS)
        print(f"[append_observations] condensed report to {len(content)} chars")

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("[append_observations] DEEPSEEK_API_KEY not set, skipping.")
        return 0

    try:
        # NOTE: we deliberately use the plain OpenAI client instead of
        # src/ai/client.py — the shared OpenAIClient forces
        # response_format={"type": "json_object"} for deepseek, which would
        # corrupt this free-form Markdown output.
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": USER_PROMPT_TEMPLATE.format(content=content)},
            ],
            temperature=0.3,
            max_tokens=1500,
        )
        text = (resp.choices[0].message.content or "").strip()
    except Exception as exc:
        print(f"[append_observations] DeepSeek call failed: {exc}")
        return 0

    if not text:
        print("[append_observations] empty response, skipping.")
        return 0

    with path.open("a", encoding="utf-8") as f:
        f.write("\n\n---\n\n" + text + "\n")
    print(f"[append_observations] appended observations to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
