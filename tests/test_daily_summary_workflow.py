from pathlib import Path


def test_manual_dispatch_selects_exactly_one_rollup_mode():
    workflow = Path(".github/workflows/daily-summary.yml").read_text(
        encoding="utf-8"
    )

    assert "mode:" in workflow
    assert "- 'daily'" in workflow
    assert "- 'weekly'" in workflow
    assert "- 'monthly'" in workflow
    assert "- 'yearly'" in workflow
    for job, mode in (
        ("daily-summary", "daily"),
        ("weekly-summary", "weekly"),
        ("monthly-summary", "monthly"),
        ("yearly-summary", "yearly"),
    ):
        start = workflow.index(f"  {job}:")
        header = workflow[start : start + 300]
        assert f"inputs.mode == '{mode}'" in header

    deploy = workflow[workflow.index("- name: Deploy docs to master for Pages") :]
    for infix in ("horizon", "global", "github-trending", "ee", "榜单汇总"):
        assert f'${{DATE}}-{infix}-zh.md' in deploy


def test_secondary_board_runs_remove_shared_output_before_generation():
    workflow = Path(".github/workflows/daily-summary.yml").read_text(
        encoding="utf-8"
    )

    for step_name in (
        "Run Horizon (EE edition)",
        "Run Horizon (global news edition)",
        "Run Horizon (github-trending edition)",
    ):
        start = workflow.index(f"- name: {step_name}")
        step = workflow[start : start + 1300]
        assert 'rm -f "data/summaries/${DATE}-horizon-zh.md"' in step
