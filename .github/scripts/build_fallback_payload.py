#!/usr/bin/env python3
"""Build the hiboard payload for the daily-fallback workflow.

Differences from build_hiboard_payload.py:
- Handles the missing-post case (builds a failure notification).
- Prefixes the summary with a status icon so the user can tell
  at a glance whether the post was OK or rescued.

The output is a full hiboard-API-shaped envelope, ready to POST:
    { "data": { "authCode": ..., "msgContent": [{ ... }] } }

Required environment variables:
- DATE_INPUT      (optional) - YYYY-MM-DD; defaults to today Asia/Shanghai
- PAGES_BASE      - GitHub Pages URL prefix
- HIBOARD_AUTH_CODE - hiboard auth code (used in the payload body)

Positional args:
- post_path    - path to daily post on disk (master checkout). Pass any
                 non-existent path if the post is missing.

Writes the payload to /tmp/horizon-fallback-payload.json and prints
"ok" or "failed" to stdout.
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def beijing_today() -> str:
    out = subprocess.run(
        ["bash", "-c", "TZ=Asia/Shanghai date +'%Y-%m-%d'"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return out


def failure_payload(date: str, posts_dir: Path) -> dict:
    recent = []
    if posts_dir.exists():
        for p in sorted(posts_dir.glob("*.md")):
            recent.append("  " + p.name)
    recent_str = "\n".join(recent[-3:]) if recent else "  (空)"
    summary = f"\u274c Horizon 日报 {date} 兜底失败"
    content = (
        f"\u4eca\u65e5\u65e5\u62a5\u7f3a\u5931\u4e14 9:30 \u515c\u5e95\u8865\u6551\u672a\u6210\u529f,"
        f"\u8bf7\u68c0\u67e5 daily-summary workflow\u3002\n\n"
        f"\u6700\u8fd1 _posts:\n{recent_str}"
    )
    return {
        "data": {
            "authCode": os.environ["HIBOARD_AUTH_CODE"],
            "msgContent": [
                {
                    "msgId": f"horizon-fallback-{date}",
                    "scheduleTaskId": "horizon-fallback",
                    "scheduleTaskName": "Horizon 兜底推送",
                    "summary": summary,
                    "result": f"daily-summary {date} 兜底失败,需要手动补救",
                    "content": content,
                    "taskFinishTime": int(datetime.now().timestamp()),
                    "source": "horizon-fallback",
                }
            ],
        }
    }


def rescued_payload(envelope: dict) -> dict:
    """Take a successful build_hiboard_payload.py envelope and mark it as rescued."""
    item = envelope["data"]["msgContent"][0]
    item["summary"] = "\u26a0\ufe0f " + item["summary"] + " \u00b7 \u515c\u5e95\u8865\u6551"
    item["scheduleTaskId"] = "horizon-fallback"
    item["scheduleTaskName"] = "Horizon 兜底推送"
    item["source"] = "horizon-fallback"
    return envelope


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: build_fallback_payload.py <post_path>", file=sys.stderr)
        return 2

    post_path = Path(sys.argv[1])
    date_input = os.environ.get("DATE_INPUT", "").strip()
    auth_code = os.environ.get("HIBOARD_AUTH_CODE", "").strip()
    if not auth_code:
        print("::error::HIBOARD_AUTH_CODE not set in environment", file=sys.stderr)
        return 1

    date = date_input or beijing_today()

    if not post_path.exists():
        # Failure case: build a failure notification.
        payload = failure_payload(date, post_path.parent)
        status = "failed"
    else:
        # OK case: reuse the same payload builder as daily-notify.
        result = subprocess.run(
            ["python3", ".github/scripts/build_hiboard_payload.py", str(post_path)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            print(f"build_hiboard_payload.py failed: {result.stderr}", file=sys.stderr)
            return 1
        envelope = json.loads(result.stdout)
        payload = rescued_payload(envelope)
        status = "ok"

    out_path = Path("/tmp/horizon-fallback-payload.json")
    out_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    print(status)
    return 0


if __name__ == "__main__":
    sys.exit(main())
