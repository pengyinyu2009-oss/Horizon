import json
import os
import subprocess
import sys


def test_github_payload_marks_scoring_fault(tmp_path):
    post = tmp_path / "2026-07-28-horizon-zh.md"
    post.write_text(
        "# 【评分故障空报】Horizon 每日简报 - 2026-07-28\n\n"
        "生成失败：评分服务异常，不代表今日无重要动态。\n",
        encoding="utf-8",
    )
    env = os.environ | {
        "DATE_INPUT": "2026-07-28",
        "PAGES_BASE": "https://horizon.pyyaiai.com",
        "HIBOARD_AUTH_CODE": "test-auth",
    }

    proc = subprocess.run(
        [sys.executable, ".github/scripts/build_hiboard_payload.py", str(post)],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    item = json.loads(proc.stdout)["data"]["msgContent"][0]

    assert item["summary"] == "⚠️ Horizon 评分故障 2026-07-28"
    assert item["result"] == "生成失败：评分服务异常"
    assert "【评分故障空报】" in item["content"]
