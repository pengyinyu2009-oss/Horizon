from datetime import datetime, timezone

from scripts.dispatch_daily_github import build_dispatch_payload, select_dispatched_run


def test_dispatch_payload_runs_daily_mode_only():
    assert build_dispatch_payload(force=True) == {
        "ref": "main",
        "inputs": {"mode": "daily", "force": "true"},
    }


def test_select_dispatched_run_ignores_older_manual_runs():
    dispatched_at = datetime(2026, 8, 9, 0, 17, tzinfo=timezone.utc)
    runs = [
        {
            "id": 1,
            "event": "workflow_dispatch",
            "created_at": "2026-08-08T09:23:26Z",
            "status": "completed",
        },
        {
            "id": 2,
            "event": "workflow_dispatch",
            "created_at": "2026-08-09T00:17:05Z",
            "status": "queued",
        },
    ]

    assert select_dispatched_run(runs, dispatched_at)["id"] == 2
