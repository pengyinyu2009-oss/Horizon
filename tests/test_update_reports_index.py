import json

import pytest

from scripts.update_reports_index import (
    IndexUpdateError,
    _discover_period_reports,
    _missing_weekly_ids,
    update_reports_index,
)


OLD_INDEX = """---
layout: default
title: "Horizon · 4 榜单日报导航"
date: 2026-08-06
period: index
---

# 🌅 Horizon · 4 榜单日报导航

## 📅 最新日报（2026-08-06 周四）

[**2026-08-06 4 榜单汇总**](/reports-html/2026-08-06-榜单汇总-zh.html)
- 共 64+ 条，每条双评分 + 入选理由
- 数据窗口：旧窗口

---

## 📅 最新周报（2026-W31）

[**2026-W31 周榜汇总**](/reports-html/2026-W31-周榜-zh.html)
- 4 大榜单周维度聚合

---

## 🗂 最近日报

[08-06](/reports-html/2026-08-06.html)

---

## 🗓 周期报历史

- **周榜**：2026-W27 / W28 / W29 / W30 / W31
- **月榜**：待发布（每月 8 号）
- **年榜**：待发布（H1/H2）

---

## 🛠 数据流

- **发布**：每日 09:30 BJT 同步（GHA 自动），每周日同步周榜
"""


def _write_lineage(path, date="2026-08-10", passed=True, total_items=58):
    path.write_text(
        json.dumps(
            {
                "date": date,
                "passed": passed,
                "total_items": total_items,
                "boards": {
                    name: {"passed": True}
                    for name in ("global", "ai", "github", "ee")
                },
            }
        ),
        encoding="utf-8",
    )


def _write_reports(posts_dir, weeklies=(), monthlies=(), yearlies=(), dailies=()):
    """Materialise the report files the publish step copies next to the index."""
    for pid in weeklies:
        (posts_dir / f"{pid}-周榜-zh.md").write_text("weekly\n", encoding="utf-8")
    for pid in monthlies:
        (posts_dir / f"{pid}-月榜-zh.md").write_text("monthly\n", encoding="utf-8")
    for pid in yearlies:
        (posts_dir / f"{pid}-年榜-zh.md").write_text("yearly\n", encoding="utf-8")
    for day in dailies:
        (posts_dir / f"{day}-horizon-zh.md").write_text("daily\n", encoding="utf-8")


def test_update_reports_index_uses_current_lineage_and_vps_schedule(tmp_path):
    index = tmp_path / "index.md"
    lineage = tmp_path / "lineage.json"
    index.write_text(OLD_INDEX, encoding="utf-8")
    _write_lineage(lineage)

    update_reports_index(index, "2026-08-10", lineage)

    updated = index.read_text(encoding="utf-8")
    assert "date: 2026-08-10" in updated
    assert "最新日报（2026-08-10 周一）" in updated
    assert "/reports-html/2026-08-10.html" in updated
    assert "共 58 条" in updated
    assert "4/4 榜单 lineage 校验通过" in updated
    assert "VPS 08:17 BJT 主任务" in updated
    assert "10:30 / 21:17 幂等补偿" in updated
    assert "2026-08-06 4 榜单汇总" not in updated
    assert "GHA 自动" not in updated


def test_period_sections_follow_the_files_that_actually_exist(tmp_path):
    """周报/月报/年报/最近日报必须从同目录真实文件推导，不再写死。"""
    index = tmp_path / "index.md"
    lineage = tmp_path / "lineage.json"
    index.write_text(OLD_INDEX, encoding="utf-8")
    _write_lineage(lineage, date="2026-11-01", total_items=55)
    _write_reports(
        tmp_path,
        weeklies=["2026-W42", "2026-W43"],
        monthlies=["2026-08"],
        dailies=["2026-10-26", "2026-10-27", "2026-11-01"],
    )

    update_reports_index(index, "2026-11-01", lineage)

    updated = index.read_text(encoding="utf-8")
    # 最新周报指向真实存在的最新周报
    assert "最新周报（2026-W43）" in updated
    assert "[**2026-W43 周榜汇总**](/reports-html/2026-W43-周榜-zh.html)" in updated
    # 周期报历史是可点击链接，且月报不再说"待发布"
    assert "[2026-W42](/reports-html/2026-W42-周榜-zh.html)" in updated
    assert "[2026-08](/reports-html/2026-08-月榜-zh.html)" in updated
    assert "月榜**：待发布" not in updated
    # 最近日报取真实日期
    assert "[11-01](/reports-html/2026-11-01.html)" in updated
    assert "[10-26](/reports-html/2026-10-26.html)" in updated
    assert "08-06" not in updated
    # 旧的写死文本被替换
    assert "2026-W27 / W28" not in updated


def test_period_history_reports_weekly_gaps(tmp_path):
    """周报缺口要如实写出来（停更周没有数据来源，月报/年报链会跳过）。"""
    index = tmp_path / "index.md"
    lineage = tmp_path / "lineage.json"
    index.write_text(OLD_INDEX, encoding="utf-8")
    _write_lineage(lineage, date="2026-11-01")
    _write_reports(
        tmp_path,
        weeklies=["2026-W37", "2026-W42", "2026-W43"],
        monthlies=["2026-08"],
    )

    update_reports_index(index, "2026-11-01", lineage)

    updated = index.read_text(encoding="utf-8")
    assert "缺口" in updated
    for missing in ("2026-W38", "2026-W39", "2026-W40", "2026-W41"):
        assert missing in updated


def test_period_sections_degrade_when_nothing_exists(tmp_path):
    index = tmp_path / "index.md"
    lineage = tmp_path / "lineage.json"
    index.write_text(OLD_INDEX, encoding="utf-8")
    _write_lineage(lineage, date="2026-08-10")

    update_reports_index(index, "2026-08-10", lineage)

    updated = index.read_text(encoding="utf-8")
    assert "最新周报（待发布）" in updated
    assert "暂无日报" in updated
    assert "年榜**：待发布" in updated


def test_missing_weekly_ids_detects_holes_only_between_extremes():
    assert _missing_weekly_ids(["2026-W37", "2026-W42", "2026-W43"]) == [
        "2026-W38",
        "2026-W39",
        "2026-W40",
        "2026-W41",
    ]
    assert _missing_weekly_ids(["2026-W42", "2026-W43"]) == []
    assert _missing_weekly_ids(["2026-W42"]) == []


def test_discover_ignores_per_board_fragments(tmp_path):
    """只有 -周榜-zh.md 之类的汇总文件算周期报；分榜碎片不算。"""
    _write_reports(
        tmp_path,
        weeklies=["2026-W43"],
        dailies=["2026-11-01"],
    )
    (tmp_path / "2026-W28-horizon-zh.md").write_text("fragment\n", encoding="utf-8")
    (tmp_path / "index.md").write_text("index\n", encoding="utf-8")

    found = _discover_period_reports(tmp_path)

    assert found["weeklies"] == ["2026-W43"]
    assert found["dailies"] == ["2026-11-01"]
    assert found["monthlies"] == []
    assert found["yearlies"] == []


@pytest.mark.parametrize(
    ("lineage_date", "passed"),
    [("2026-08-09", True), ("2026-08-10", False)],
)
def test_update_reports_index_rejects_unverified_lineage(
    tmp_path, lineage_date, passed
):
    index = tmp_path / "index.md"
    lineage = tmp_path / "lineage.json"
    index.write_text(OLD_INDEX, encoding="utf-8")
    _write_lineage(lineage, date=lineage_date, passed=passed)

    with pytest.raises(IndexUpdateError):
        update_reports_index(index, "2026-08-10", lineage)

    assert index.read_text(encoding="utf-8") == OLD_INDEX
