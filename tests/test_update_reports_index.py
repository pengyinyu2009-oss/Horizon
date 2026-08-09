import json

import pytest

from scripts.update_reports_index import IndexUpdateError, update_reports_index


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
