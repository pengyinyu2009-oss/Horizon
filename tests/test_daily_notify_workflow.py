from pathlib import Path


def test_daily_notify_requires_public_lineage_before_normal_push():
    workflow = Path(".github/workflows/daily-notify.yml").read_text(encoding="utf-8")

    verify_at = workflow.index("- name: Verify dated report is publicly readable")
    push_at = workflow.index("- name: Push to hiboard")
    verify_step = workflow[verify_at:push_at]

    assert verify_at < push_at
    assert "lineage" in verify_step.lower()
    assert "passed" in verify_step
