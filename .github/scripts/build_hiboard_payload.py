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
    post_url = (
        f"{pages_base}/{date[0:4]}/{date[5:7]}/{date[8:10]}/horizon-zh.html"
    )
    home_url = f"{pages_base}/"

    with open(post_path, encoding="utf-8") as f:
        text = f.read()

    # Strip Jekyll front matter if present.
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            text = text[end + 5:]

    # Pull out headlines in the form:
    #   ## [title](url) ⭐ 8.5/10
    headlines = re.findall(
        r"^##\s+\[([^\]]+)\]\(([^)]+)\)\s*\u2b50\ufe0f\s*([\d.]+)/10",
        text,
        re.MULTILINE,
    )

    seen, top = set(), []
    for title, url, score in headlines:
        try:
            s = float(score)
        except ValueError:
            continue
        if s < 8.0:
            continue
        if url in seen:
            continue
        seen.add(url)
        top.append((s, title.strip(), url.strip()))

    top.sort(reverse=True)
    top = top[:12]

    # Build the markdown body that hiboard will display.
    lines = [
        f"## 🌅 Horizon 每日速递 · {date}",
        "",
        f"**{len(top)} 条 8 分以上要事**",
        "",
    ]
    for s, t, u in top:
        lines.append(f"- ⭐ **{s:.1f}** [{t}]({u})")
    lines += [
        "",
        "---",
        "",
        f"📖 [完整简报]({post_url})",
        "",
        f"🏠 [首页]({home_url})",
    ]
    content = "\n".join(lines)

    summary = f"🌅 Horizon 每日速递 {date} · {len(top)} 条 8+"
    result = f"daily-summary {date} 已生成"

    payload = {
        "data": {
            "authCode": os.environ["HIBOARD_AUTH_CODE"],
            "msgContent": [
                {
                    "msgId": f"horizon-daily-{date}",
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