"""Tests for Phase 5: per-board rollups, period merge, 我必看 section."""

import asyncio
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from src.ai.summarizer import (
    WeeklySummarizer,
    merge_period_reports,
    period_file_label,
)
from src.models import Story
from src.orchestrator import HorizonOrchestrator
from src.storage.manager import StorageManager


def _story(idx: int, score: float, subjective: float = 0.0) -> Story:
    return Story(
        title=f"Story {idx}",
        url=f"https://example.com/s{idx}",
        score=score,
        summary=f"Summary of story {idx}.",
        source_date="2026-07-28",
        subjective_score=subjective,
    )


def _weekly_report(board: str) -> str:
    stories = [_story(1, 9.0, 9.5), _story(2, 8.5, 7.0)]
    return asyncio.run(
        WeeklySummarizer(ai_client=None).generate_report(
            stories=stories,
            period_id="2026-W31",
            language="zh",
            threshold=8.0,
            report_threshold=9.0,
            top_n_report=1,
            lookback_label="过去 7 天",
            related_by_index={},
        )
    )


# --- merge_period_reports ----------------------------------------------------


def test_merge_period_reports_namespaces_and_demotes():
    reports = {"horizon": _weekly_report("horizon"), "global": _weekly_report("global")}

    merged = merge_period_reports("weekly", "2026-W31", "zh", reports)

    assert merged.startswith("# Horizon 周榜 · 2026-W31")
    assert '<a id="sec-ai"></a>' in merged
    assert '<a id="sec-global"></a>' in merged
    # Roll-up anchors namespaced per board.
    assert '<a id="weekly-horizon-item-1"></a>' in merged
    assert '<a id="weekly-global-item-1"></a>' in merged
    assert "](#weekly-horizon-item-1)" in merged
    # Per-board H1 dropped, section headers present.
    assert "Horizon 上周总览" not in merged
    assert "## 🤖 Horizon 总榜" in merged
    assert "## 🌍 全球新闻" in merged
    # Callout headings demoted from ### to ####.
    assert "#### [Story 1](https://example.com/s1)" in merged
    # No must-see section for weekly.
    assert "我必看" not in merged


def test_merge_period_reports_with_must_see():
    reports = {"horizon": _weekly_report("horizon")}
    must_see = "## ⭐ 我必看\n\n> 精选。\n\n1. **[Story 1](https://example.com/s1)**：建议复刻。\n"

    merged = merge_period_reports("monthly", "2026-07", "zh", reports, must_see_md=must_see)

    assert "## ⭐ 我必看" in merged
    # Must-see sits before the first board section.
    assert merged.index("我必看") < merged.index('<a id="sec-ai"></a>')
    assert period_file_label("monthly") == "月榜"
    assert period_file_label("weekly") == "周榜"
    assert period_file_label("yearly") == "年榜"


# --- storage board suffix -----------------------------------------------------


def test_storage_list_and_save_per_board(tmp_path):
    storage = StorageManager(data_dir=tmp_path)
    storage.save_weekly_summary("2026-W31", "# W\n", language="zh", board="global")
    storage.save_weekly_summary("2026-W31", "# W\n", language="zh")  # horizon default

    horizon = storage.list_recent_summaries("weekly", "zh")
    glob = storage.list_recent_summaries("weekly", "zh", board="global")
    ee = storage.list_recent_summaries("weekly", "zh", board="ee")

    assert [p.name for p in horizon] == ["2026-W31-horizon-zh.md"]
    assert [p.name for p in glob] == ["2026-W31-global-zh.md"]
    assert ee == []


# --- 我必看 section ------------------------------------------------------------


def _make_orchestrator_for_must_see(tmp_path) -> HorizonOrchestrator:
    from rich.console import Console
    config = SimpleNamespace(
        persona=SimpleNamespace(enabled=True, description="电子工程师", keywords=["开源硬件"]),
    )
    orch = HorizonOrchestrator.__new__(HorizonOrchestrator)
    orch.config = config
    orch.console = Console(quiet=True)
    return orch


def test_must_see_fallback_listing_without_ai(tmp_path):
    orch = _make_orchestrator_for_must_see(tmp_path)
    stories = [_story(1, 9.0, 9.5), _story(2, 8.0, 8.5), _story(3, 7.0, 0.0)]

    md = asyncio.run(orch._build_must_see_section("monthly", stories, "zh", None))

    assert "## ⭐ 我必看" in md
    assert "[Story 1](https://example.com/s1)" in md
    assert "相关 9.5/10" in md
    # Zero-subjective stories never appear.
    assert "Story 3" not in md


def test_must_see_ai_advice_with_persona(tmp_path):
    orch = _make_orchestrator_for_must_see(tmp_path)
    stories = [_story(1, 9.0, 9.5)]

    captured = {}

    class FakeClient:
        async def complete(self, system=None, user=None, **_kw):
            captured["system"] = system
            captured["user"] = user
            return "1. **[Story 1](https://example.com/s1)**：推荐本月复刻，需准备 KiCad 与一块 STM32 板。"

    md = asyncio.run(orch._build_must_see_section("yearly", stories, "zh", FakeClient()))

    assert "推荐本月复刻" in md
    assert "电子工程师" in captured["system"]  # persona injected
    assert "相关分: 9.5" in captured["user"]
    assert "半年" in captured["user"]  # yearly label


def test_must_see_empty_without_subjective_scores(tmp_path):
    orch = _make_orchestrator_for_must_see(tmp_path)
    stories = [_story(1, 9.0), _story(2, 8.0)]
    md = asyncio.run(orch._build_must_see_section("monthly", stories, "zh", None))
    assert md == ""


# --- per-board prereq gate ----------------------------------------------------


def test_prereq_gate_is_per_board(tmp_path):
    from rich.console import Console

    storage = StorageManager(data_dir=tmp_path)
    # Horizon has the full week; global has only 3 days.
    for day in range(27, 31):  # 07-27..07-30 (4 days)
        for board in ("horizon", "global"):
            (storage.summaries_dir / f"2026-07-{day:02d}-{board}-zh.md").write_text("x")
    for day in (31,):
        (storage.summaries_dir / f"2026-07-{day:02d}-horizon-zh.md").write_text("x")
    for day in (1, 2):
        (storage.summaries_dir / f"2026-08-{day:02d}-horizon-zh.md").write_text("x")

    orch = HorizonOrchestrator.__new__(HorizonOrchestrator)
    orch.console = Console(quiet=True)
    orch.storage = storage

    # W31 = 2026-07-27..08-02: horizon incomplete (missing 07-31? no—present),
    # check: horizon has 07-27..31 + 08-01..02 = all 7 ✓; global only 4 ✗
    assert orch._check_prerequisites("weekly", "2026-W31", "zh", board="horizon") is True
    assert orch._check_prerequisites("weekly", "2026-W31", "zh", board="global") is False
