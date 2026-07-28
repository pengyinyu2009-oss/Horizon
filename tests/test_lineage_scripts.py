from scripts.build_report_json import build_report, default_report_date
from scripts.check_lineage import check_lineage


def test_build_report_accepts_published_summary_path(tmp_path):
    summary = tmp_path / "2026-07-28-horizon-zh.md"
    summary.write_text(
        "# Horizon 每日简报 - 2026-07-28\n\n"
        "> 已分析 12 条内容，但没有达到重要性阈值的条目。\n",
        encoding="utf-8",
    )

    report = build_report("2026-07-28", 48, summary_path=summary)

    assert report["_meta"]["source_summary"] == summary.name
    assert report["_meta"]["source_items_count"] == 0
    assert default_report_date().count("-") == 2


def test_empty_but_valid_report_has_complete_vacuous_lineage(tmp_path):
    summary = tmp_path / "2026-07-28-horizon-zh.md"
    summary.write_text("# Horizon 每日简报 - 2026-07-28\n", encoding="utf-8")
    report = {
        "date": "2026-07-28",
        "_meta": {"source_summary": summary.name},
        "boards": [{"anchor": "global", "rank": [], "picks": []}],
    }

    lineage = check_lineage(report, 48, summaries_dir=tmp_path)

    assert lineage["total_items"] == 0
    assert lineage["title_lineage_pct"] == 100
    assert lineage["url_lineage_pct"] == 100
    assert lineage["anchor_lineage_pct"] == 100
