#!/usr/bin/env python3
"""Build the hiboard payload for the daily-fallback workflow.

Differences from build_hiboard_payload.py:
- Handles the missing-post case (builds a failure notification).
- Prefixes the summary with a status icon so the user can tell
  at a glance whether the post was OK or rescued.

Required environment variables:
- DATE_INPUT   (optional) - YYYY-MM-DD; defaults to today Asia/Shanghai
- PAGES_BASE   - GitHub Pages URL prefix

Positional args:
- post_path    - path to daily post on disk (master checkout). Pass empty
                 string "" if the post is missing.

Writes the payload JSON to /tmp/horizon-fallback-payload.json and prints
"ok" or "failed" to stdout (the calling workflow reads the status from
${{ steps.<id>.outputs.status }} via a separate echo).
"""

import datetime
import json
import os
import subprocess
import sys
from pathlib import Path


def beijing_today() -> str:
    # Cross-platform: use the same TZ trick the workflow uses.
    out = subprocess.run(
        ["bash", "-c", "TZ=Asia/Shanghai date +'%Y-%m-%d'"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out


def stories_in_post(path: Path) -> int:
    if not path.exists():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            n += 1
    return n


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: build_fallback_payload.py <post_path>", file=sys.stderr)
        return 2

    post_path = Path(sys.argv[1])
    date_input = os.environ.get("DATE_INPUT", "").strip()
    pages_base = os.environ.get("PAGES_BASE", "https://pengyinyu2009-oss.github.io/Horizon").rstrip("/")

    date = date_input or beijing_today()

    if not post_path.exists():
        # Failure case: post still missing after rescue attempt.
        recent = []
        posts_dir = post_path.parent
        if posts_dir.exists():
            for p in sorted(posts_dir.glob("*.md")):
                recent.append("  " + p.name)
        recent_str = "\n".join(recent[-3:]) if recent else "  (空)"
        payload = {
            "summary": f"\u274c Horizon 日报 {date} 兜底失败",
            "content": (
                f"\u4eca\u65e5\u65e5\u62a5\u7f3a\u5931\u4e14 9:30 \u5151\u5e95\u8865\u655d\u672a\u6210\u529f,"
                f"\u8bf7\u68c0\u67e5 daily-summary workflow\u3002\n\n"
                f"\u6700\u8fd1 _posts:\n{recent_str}"
            ),
            "stories": [],
        }
    else:
        # OK case: reuse the same payload builder as daily-notify.
        result = subprocess.run(
            ["python3", ".github/scripts/build_hiboard_payload.py", str(post_path)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"build_hiboard_payload.py failed: {result.stderr}", file=sys.stderr)
            return 1
        payload = json.loads(result.stdout)
        # Mark this as a fallback-rescued delivery.
        payload["summary"] = "\u26a0\ufe0f " + payload["summary"] + " \u00b7 \u5151\u5e95\u8865\u655d"

    out_path = Path("/tmp/horizon-fallback-payload.json")
    out_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print("ok" if post_path.exists() else "failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
