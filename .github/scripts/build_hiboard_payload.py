#!/usr/bin/env python3
"""Build the hiboard payload for the daily Horizon digest.

Reads the just-deployed daily post (master branch), extracts 8+ story
headlines, and prints a JSON payload to stdout ready to POST to hiboard.

Required environment variables (set by the calling workflow):
- DATE_INPUT   (optional) - YYYY-MM-DD; defaults to today (UTC)
- PAGES_BASE   - GitHub Pages URL prefix, e.g.
                https://pengyinyu2009-oss.github.io/Horizon
- HIBOARD_AUTH_CODE - auth code for hiboard

Usage:
    python3 build_hiboard_payload.py <path-to-daily-post.md>
"""

import json
import os
import re
import sys
from datetime import datetime


def main():
    if len(sys.argv) < 2:
        print("usage: build_hiboard_payload.py <daily-post.md>", file=sys.stderr)
        sys.exit(2)

    post_path = sys.argv[1]
    date_input = os.environ.get("DATE_INPUT", "").strip()
    date = date_input or datetime.now().strftime("%Y-%m-%d")
    pages_base = os.environ.get(
        "PAGES_BASE", "https://pengyinyu2009-oss.github.io/Horizon"
    )
    with open(post_path, encoding="utf-8") as f:
        text = f.read()

    # Strip Jekyll front matter if present.
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5:]

    # 完整简报为「一天一页」的合并静态页：总览/电源EE/嵌入式/GitHub热榜
    # 全部在 {date}.html 里，顶部锚点导航切换（2026-07-22 起由 4 个独立
    # 分版页合并而来，避免页面太多）。负一屏卡片只放这一个链接。
    digest_url = f"{pages_base}/reports-html/{date}.html"

    # Pull out headlines in the form:
    #   ## [title](url) ⭐ 8.5/10
    headlines = re.findall(
        r"^##\s+\[([^\]]+)\]\(([^)]+)\)\s*\u2b50\ufe0f\s*([\d.]+)/10",
        text,
        re.MULTILINE,
    )

    # CJK Unified Ideographs (basic block + ext A); matches any Chinese / Japanese
    # kanji / Korean hanja character. We only push a headline if its title
    # contains at least one such character — otherwise the zh-version post
    # would still surface an English headline (since AI enrichment's
    # `_translate_item` fallback silently no-ops on parse failure), which the
    # user explicitly does not want on the 负一屏 推送 channel.
    _CJK_RE = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf]")

    def has_cjk(title: str) -> bool:
        return bool(_CJK_RE.search(title))

    seen, top = set(), []
    skipped = 0
    for title, url, score in headlines:
        try:
            s = float(score)
        except ValueError:
            continue
        if s < 8.0:
            continue
        if url in seen:
            continue
        if not has_cjk(title):
            skipped += 1
            continue
        seen.add(url)
        top.append((s, title.strip(), url.strip()))

    top.sort(reverse=True)
    top = top[:12]

    # Build the markdown body that hiboard will display.
    lines = [
        f"🌅 Horizon 每日速递 · {date}",
        "",
        f"{len(top)} 条 8 分以上要事：",
        "",
    ]
    for s, t, u in top:
        lines.append(f"{s:.1f} 分｜{t}")
    lines += [
        "",
        "📖 今日完整简报（总览/电源EE/嵌入式/GitHub热榜，一页看全）：",
        # NOTE: hiboard 卡片不支持 markdown 链接语法 —— [文字](url) 会显示成
        # 纯文本且不可点击。平台只把裸 URL 自动识别为超链接，所以这里必须
        # 输出纯文本 URL。
        digest_url,
    ]
    content = "\n".join(lines)

    summary = f"🌅 Horizon 每日速递 {date} · {len(top)} 条 8+"
    if skipped and not top:
        result = f"{date} 暂无中文标题要事（{skipped} 条仅英文标题已跳过）"
    elif skipped:
        result = f"daily-summary {date} 已生成（{skipped} 条英文标题已跳过）"
    else:
        result = f"daily-summary {date} 已生成"

    # msgId 必须每次推送唯一：华为侧按 msgId 去重，同一天重推（force）
    # 若 msgId 不变会被当成重复卡片丢弃，手机上看不到更新。
    msg_id = f"horizon-daily-{date}-{datetime.now().strftime('%H%M%S')}"

    payload = {
        "data": {
            "authCode": os.environ["HIBOARD_AUTH_CODE"],
            "msgContent": [
                {
                    "msgId": msg_id,
                    "scheduleTaskId": "horizon-daily",
                    "scheduleTaskName": "Horizon 每日速递",
                    "summary": summary,
                    "result": result,
                    "content": content,
                    "taskFinishTime": int(datetime.now().timestamp()),
                    "source": "horizon",
                }
            ],
        },
    }

    json.dump(payload, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()