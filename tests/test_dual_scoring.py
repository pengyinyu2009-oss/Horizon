"""Tests for 2026-07-28 dual scoring (objective + persona-subjective)."""

import asyncio
import json
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from tenacity import wait_none

from src.ai.analyzer import ContentAnalyzer
from src.ai.prompts import build_persona_section
from src.ai.summarizer import DailySummarizer, parse_daily_full_stories
from src.models import ContentItem, PersonaConfig, SourceType


def _make_item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url="https://example.com/item",
        published_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )


def _dual_client(response: str, persona=None):
    async def completion(**_kwargs):
        completion.kwargs = _kwargs
        return response

    return SimpleNamespace(
        complete=completion,
        config=SimpleNamespace(persona=persona),
    )


_PERSONA = PersonaConfig(
    enabled=True,
    description="电子工程师/硬件开发者，关注开源硬件与可复刻项目",
    keywords=["open hardware", "EDA", "RISC-V"],
)


# --- build_persona_section -------------------------------------------------


def test_persona_section_includes_description_and_keywords():
    text = build_persona_section(_PERSONA)
    assert "电子工程师" in text
    assert "RISC-V" in text


def test_persona_section_falls_back_when_missing_or_disabled():
    assert "No specific reader persona" in build_persona_section(None)
    disabled = PersonaConfig(enabled=False, description="ignored")
    assert "No specific reader persona" in build_persona_section(disabled)


# --- analyzer dual scoring ---------------------------------------------------


def test_analyze_item_dual_scores_and_injects_persona():
    response = json.dumps({
        "score": 8.5,
        "subjective_score": 9,
        "subjective_reason": "matches open-hardware interest",
        "reason": "major release",
        "summary": "s",
        "tags": ["t"],
    })
    client = _dual_client(response, persona=_PERSONA)
    analyzer = ContentAnalyzer(client)
    item = _make_item("rss:test:dual")

    asyncio.run(analyzer._analyze_item(item))

    assert item.ai_score == 8.5
    assert item.subjective_score == 9.0
    assert item.subjective_reason == "matches open-hardware interest"
    user_prompt = client.complete.kwargs["user"]
    assert "电子工程师" in user_prompt
    assert "subjective_score" in user_prompt


def test_analyze_item_dual_missing_subjective_falls_back_to_objective():
    response = json.dumps({
        "score": 7.5,
        "reason": "r",
        "summary": "s",
        "tags": [],
    })
    analyzer = ContentAnalyzer(_dual_client(response, persona=_PERSONA))
    item = _make_item("rss:test:dual-missing")

    asyncio.run(analyzer._analyze_item(item))

    assert item.ai_score == 7.5
    assert item.subjective_score == 7.5
    assert item.subjective_reason == ""


def test_analyze_item_dual_via_explicit_persona_with_ai_config_client():
    """Regression for the 2026-07-28 first-run bug: in production the
    client carries the *AIConfig* sub-model (no ``persona`` attribute),
    so dual scoring silently never ran until the orchestrator started
    passing the root-Config persona explicitly."""
    response = json.dumps({
        "score": 8.0,
        "subjective_score": 6.5,
        "reason": "r",
        "summary": "s",
        "tags": [],
    })

    async def completion(**_kwargs):
        completion.kwargs = _kwargs
        return response

    # AIConfig-shaped client: model/temperature/prompt_overrides, NO persona.
    client = SimpleNamespace(
        complete=completion,
        config=SimpleNamespace(model="m", temperature=0.1, prompt_overrides={}),
    )
    analyzer = ContentAnalyzer(client, persona=_PERSONA)
    item = _make_item("rss:test:dual-explicit")

    asyncio.run(analyzer._analyze_item(item))

    assert item.ai_score == 8.0
    assert item.subjective_score == 6.5
    assert "电子工程师" in completion.kwargs["user"]


@pytest.mark.parametrize("bad", ['{"score": 8, "subjective_score": 99}',
                                 '{"score": 8, "subjective_score": "high"}'])
def test_analyze_item_dual_rejects_invalid_subjective(monkeypatch, bad):
    attempts = 0

    async def completion(**_kwargs):
        nonlocal attempts
        attempts += 1
        return bad

    client = SimpleNamespace(
        complete=completion,
        config=SimpleNamespace(persona=_PERSONA),
    )
    analyzer = ContentAnalyzer(client)
    monkeypatch.setattr(ContentAnalyzer._analyze_item.retry, "wait", wait_none())

    with pytest.raises(ValueError, match="invalid analysis subjective_score"):
        asyncio.run(analyzer._analyze_item(_make_item("rss:test:bad-subjective")))

    assert attempts == 3


def test_analyze_item_without_persona_stays_single_score():
    response = json.dumps({
        "score": 8.0,
        "reason": "r",
        "summary": "s",
        "tags": [],
    })
    client = _dual_client(response, persona=None)
    analyzer = ContentAnalyzer(client)
    item = _make_item("rss:test:legacy")

    asyncio.run(analyzer._analyze_item(item))

    assert item.ai_score == 8.0
    assert item.subjective_score is None
    assert "subjective_score" not in client.complete.kwargs["user"]


def test_analyze_batch_failure_clears_subjective(monkeypatch):
    client = SimpleNamespace(config=SimpleNamespace(persona=_PERSONA))
    analyzer = ContentAnalyzer(client)
    item = _make_item("rss:test:batch-fail")

    async def fail(item):
        raise RuntimeError("boom")

    monkeypatch.setattr(analyzer, "_analyze_item", fail)
    [result] = asyncio.run(analyzer.analyze_batch([item]))
    assert result.metadata["analysis_status"] == "failed"
    assert result.subjective_score is None


# --- summarizer: top10+3 selection and dual rendering ------------------------


def _scored_item(idx: int, objective: float, subjective=None) -> ContentItem:
    item = _make_item(f"rss:scored-{idx}")
    item.ai_score = objective
    item.ai_summary = f"Summary {idx}."
    item.ai_tags = ["t"]
    if subjective is not None:
        item.subjective_score = subjective
        item.subjective_reason = f"reason {idx}"
    return item


def test_top10_plus_3_selection():
    summarizer = DailySummarizer()
    items = [_scored_item(i, objective=9.0 - i * 0.1, subjective=1.0)
             for i in range(14)]
    # Off-list items 10..13; give #13 the highest subjective score.
    items[13].subjective_score = 9.5
    items[12].subjective_score = 9.0
    items[11].subjective_score = 8.5

    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=40, language="zh",
    ))

    # Main list capped at 10; items 10..13 excluded from the ranking.
    assert "[Item rss:scored-10]" not in md
    assert "🎯 猜你感兴趣" in md
    # Top-3 subjective off-list picks appear, worst one does not.
    assert "[Item rss:scored-13]" in md
    assert "[Item rss:scored-12]" in md
    assert "[Item rss:scored-11]" in md
    assert "[Item rss:scored-10]" not in md


def test_persona_pick_flag_forces_picks_section():
    summarizer = DailySummarizer()
    items = [_scored_item(i, objective=9.0 - i * 0.1, subjective=2.0)
             for i in range(5)]
    pick = _scored_item(99, objective=6.0, subjective=9.8)
    pick.metadata["persona_pick"] = True
    items.append(pick)

    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=20, language="zh",
    ))

    assert "🎯 猜你感兴趣" in md
    assert "rss:scored-99" in md
    # The pick is excluded from the objective ranking positions.
    assert "1. [Item rss:scored-99]" not in md
    assert "🎯 [Item rss:scored-99]" in md


def test_dual_score_rendered_in_header_and_toc():
    summarizer = DailySummarizer()
    items = [_scored_item(1, objective=8.5, subjective=9.0)]

    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=5, language="zh",
    ))

    assert "⭐️ 8.5/10 · 相关 9/10" in md


def test_single_score_render_unchanged_when_no_subjective():
    summarizer = DailySummarizer()
    items = [_scored_item(1, objective=8.5)]

    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=5, language="zh",
    ))

    assert "⭐️ 8.5/10" in md
    assert "相关" not in md
    assert "🎯" not in md


def test_enrichment_impact_fields_render():
    summarizer = DailySummarizer()
    item = _scored_item(1, objective=8.5, subjective=9.0)
    item.metadata["china_impact_zh"] = "利好国产供应链。"
    item.metadata["personal_relevance_zh"] = "可以复刻其开源方案。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-07-28", total_fetched=5, language="zh",
    ))

    assert "**对中国影响**: 利好国产供应链。" in md
    assert "**对我有什么用**: 可以复刻其开源方案。" in md


# --- parser roundtrip --------------------------------------------------------


def test_parse_daily_full_stories_reads_dual_scores():
    summarizer = DailySummarizer()
    items = [
        _scored_item(1, objective=8.5, subjective=9.5),
        _scored_item(2, objective=8.0, subjective=7.0),
    ]
    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=5, language="zh",
    ))

    stories = parse_daily_full_stories(md, language="zh")

    assert len(stories) == 2
    assert stories[0].score == 8.5
    assert stories[0].subjective_score == 9.5
    assert stories[1].subjective_score == 7.0


def test_parse_daily_full_stories_legacy_single_score():
    legacy_md = (
        '<a id="item-1"></a>\n'
        '## [Old Title](https://example.com/old) ⭐️ 8.5/10\n\n'
        'Old summary paragraph.\n\n---\n'
    )
    stories = parse_daily_full_stories(legacy_md, language="zh")
    assert len(stories) == 1
    assert stories[0].score == 8.5
    assert stories[0].subjective_score == 0.0


# --- period-grouped (GitHub 热榜) rendering ---------------------------------


def _trending_item(idx: int, period: str, objective: float, subjective=None) -> ContentItem:
    item = _scored_item(idx, objective, subjective)
    item.metadata["period"] = period
    return item


def test_period_grouped_summary_renders_three_subboards():
    summarizer = DailySummarizer()
    items = []
    i = 0
    for period, base in (("daily", 9.0), ("weekly", 8.5), ("monthly", 8.0)):
        for j in range(12):
            i += 1
            items.append(_trending_item(i, period, objective=base - j * 0.1,
                                        subjective=float(j)))
    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=36, language="zh",
    ))

    assert "📅 日榜" in md and "📆 周榜" in md and "🗓 月榜" in md
    # Namespaced anchors per sub-board.
    assert '<a id="item-daily-1"></a>' in md
    assert '<a id="item-weekly-1"></a>' in md
    assert '<a id="item-monthly-1"></a>' in md
    # Each sub-board capped at 10 + up to 3 picks.
    assert '<a id="item-daily-11"></a>' in md   # pick
    assert '<a id="item-daily-14"></a>' not in md
    # TOC links point at the namespaced anchors.
    assert "](#item-weekly-1)" in md


def test_period_grouped_not_triggered_for_mixed_items():
    summarizer = DailySummarizer()
    items = [_trending_item(1, "daily", 9.0), _scored_item(2, 8.5)]
    md = asyncio.run(summarizer.generate_summary(
        items, "2026-07-28", total_fetched=2, language="zh",
    ))
    # Mixed content falls back to the flat layout.
    assert '<a id="item-1"></a>' in md
    assert "日榜" not in md
