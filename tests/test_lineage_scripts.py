from scripts.build_report_json import build_report, default_report_date
from scripts.check_lineage import check_lineage


# 2026-10-28 统一版式后的单条日报片段：五栏目齐全（入选理由/背景/
# 对中国影响/对沈阳影响/对我影响），回归测试必须覆盖带条目的路径——
# derive_news_fields 曾在空摘要用例下漏过一个 NameError。
_UNIFIED_ITEM_MD = """---
layout: default
title: "Horizon Daily: 2026-10-28 (ZH)"
date: 2026-10-28
lang: zh
period: daily
---

# Horizon 每日速递 - 2026-10-28

> 从 40 条内容中筛选出 2 条重要资讯。

---

1. [冒烟条目一](https://example.com/1) ⭐️ 8.5/10 · 相关 9/10
2. [冒烟条目二](https://example.com/2) ⭐️ 7.0/10 · 相关 6/10

---

<a id="item-1"></a>
## [冒烟条目一](https://example.com/1) ⭐️ 8.5/10 · 相关 9/10

这是条目一的详细摘要。

rss · unknown · 10月28日 09:00

**入选理由**: 重要版本发布。

**背景**: 条目一的背景知识。

**对中国影响**: 条目一对中国的影响。

**对沈阳影响**: 条目一对沈阳的影响。

**对我影响**: 条目一对我的影响。

---

<a id="item-2"></a>
## [冒烟条目二](https://example.com/2) ⭐️ 7.0/10 · 相关 6/10

这是条目二的详细摘要。

rss · unknown · 10月28日 09:00

**入选理由**: 增量更新但有参考价值。

**背景**: 条目二的背景知识。

**对中国影响**: 条目二对中国的影响。

**对沈阳影响**: 对沈阳本地暂无直接影响。

**对我影响**: 条目二对我的影响。

---
"""


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


def test_build_report_derives_unified_layout_fields(tmp_path):
    """统一版式五栏目必须被 derive_news_fields 完整派生（含 url）。"""
    summary = tmp_path / "2026-10-28-horizon-zh.md"
    summary.write_text(_UNIFIED_ITEM_MD, encoding="utf-8")

    report = build_report("2026-10-28", 48, summary_path=summary)

    assert report["_meta"]["source_items_count"] == 2
    derived = [
        item
        for board in report["boards"]
        for item in board["rank"] + board["picks"]
    ]
    assert len(derived) == 2
    for item in derived:
        assert item["url"].startswith("https://")
        assert item["impact_cn"], "对中国影响 missing"
        assert item["impact_local"], "对沈阳影响 missing"
        assert item["impact_me"], "对我影响 missing"
        assert item["pick_reason"], "入选理由 missing"


def test_build_report_lineage_passes_for_unified_layout(tmp_path):
    summary = tmp_path / "2026-10-28-horizon-zh.md"
    summary.write_text(_UNIFIED_ITEM_MD, encoding="utf-8")

    report = build_report("2026-10-28", 48, summary_path=summary)
    lineage = check_lineage(report, 48, summaries_dir=tmp_path)

    assert lineage["passed"] is True
    assert lineage["total_items"] == 2


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
    assert lineage["passed"] is True
