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


def test_analyze_item_dual_prompt_pins_chinese_output_language():
    """The dual prompt must pin free-text fields to the report language —
    otherwise subjective_reason leaks English into the zh report (seen on
    the 2026-07-28 first run: "入选理由" rendered in English)."""
    response = json.dumps({
        "score": 8.0,
        "subjective_score": 6.5,
        "subjective_reason": "r",
        "reason": "r",
        "summary": "s",
        "tags": [],
    })

    async def completion(**_kwargs):
        completion.kwargs = _kwargs
        return response

    client = SimpleNamespace(
        complete=completion,
        config=SimpleNamespace(
            model="m", temperature=0.1, prompt_overrides={}, languages=["zh"]
        ),
    )
    analyzer = ContentAnalyzer(client, persona=_PERSONA)
    item = _make_item("rss:test:dual-lang")

    asyncio.run(analyzer._analyze_item(item))

    assert "Simplified Chinese" in completion.kwargs["user"]


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
    item.ai_reason = "重要版本发布。"
    item.metadata["china_impact_zh"] = "利好国产供应链。"
    item.metadata["local_impact_zh"] = "沈阳硬件社区可关注。"
    item.metadata["personal_relevance_zh"] = "可以复刻其开源方案。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-07-28", total_fetched=5, language="zh",
    ))

    assert "**对中国影响**: 利好国产供应链。" in md
    assert "**对沈阳影响**: 沈阳硬件社区可关注。" in md
    assert "**对我影响**: 可以复刻其开源方案。" in md
    assert "**入选理由**: 重要版本发布。" in md


def test_unified_layout_full_writeup_for_every_item():
    """2026-10-12: a sub-8.0 item renders the same full write-up as an 8+ one."""
    summarizer = DailySummarizer()
    low = _scored_item(1, objective=7.0, subjective=6.0)
    low.ai_reason = "增量更新但有参考价值。"
    low.metadata["background_zh"] = "该工具链的演进背景。"
    low.metadata["china_impact_zh"] = "国内同类项目可借鉴。"
    low.metadata["local_impact_zh"] = "对沈阳本地暂无直接影响。"
    low.metadata["personal_relevance_zh"] = "可纳入个人工具链评估。"

    md = asyncio.run(summarizer.generate_summary(
        [low], "2026-10-12", total_fetched=5, language="zh",
    ))

    # No brief-tier marker, full section header instead.
    assert "（简报）" not in md
    assert "## [Item rss:scored-1]" in md
    # All five fixed sections present for the low-score item.
    for label in ("入选理由", "背景", "对中国影响", "对沈阳影响", "对我影响"):
        assert f"**{label}**" in md
    # Header no longer promises a two-tier split.
    assert "8 分以上" not in md
    assert "统一版式" in md


def test_local_impact_label_follows_persona_location():
    summarizer = DailySummarizer.from_persona(
        PersonaConfig(enabled=True, description="d", location="大连")
    )
    item = _scored_item(1, objective=8.0, subjective=8.0)
    item.metadata["local_impact_zh"] = "大连本地暂无直接影响。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-10-12", total_fetched=5, language="zh",
    ))

    assert "**对大连影响**: 大连本地暂无直接影响。" in md
    assert "对沈阳影响" not in md


def test_pick_reason_uses_subjective_rationale():
    summarizer = DailySummarizer()
    item = _scored_item(1, objective=6.5, subjective=9.0)
    item.ai_reason = "客观分平平。"
    item.metadata["persona_pick"] = True

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-10-12", total_fetched=5, language="zh",
    ))

    # Picks cite the subjective rationale, not the objective one.
    assert "**入选理由**: reason 1" in md


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


# --- 2026-10-29: GitHub 热榜 项目用途 + 评星 + 必看标记 ---------------------


def _project_item(idx: int, objective: float, subjective: float) -> ContentItem:
    item = _make_item(f"github_trending:daily:owner/repo-{idx}")
    item.source_type = SourceType.GITHUB_TRENDING
    item.ai_score = objective
    item.subjective_score = subjective
    item.ai_summary = f"Repo summary {idx}."
    item.ai_reason = f"热度理由 {idx}。"
    item.subjective_reason = f"画像理由 {idx}。"
    item.metadata.update({
        "repo": f"owner/repo-{idx}",
        "period": "daily",
        "total_stars": 306000,
        "stars_gained": 617,
    })
    return item


def test_github_trending_item_renders_project_usage_and_star_rating():
    summarizer = DailySummarizer()
    item = _project_item(1, objective=8.5, subjective=8.0)
    item.metadata["project_usage_zh"] = "可以拿来给嵌入式项目做 AI 辅助固件测试。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-10-29", total_fetched=30, language="zh",
    ))

    # 项目用途栏目（条目正文里位于入选理由之前）
    assert "**对这个项目有什么用**: 可以拿来给嵌入式项目做 AI 辅助固件测试。" in md
    body = md[md.index(f'id="item-1"'):]
    assert body.index("对这个项目有什么用") < body.index("入选理由")
    # 评星：均分 8.25 → 4.1/5
    assert "推荐 ⭐" in md
    assert "4.1/5" in md
    # 仓库总星标进入信源行
    assert "⭐ 30.6万 总星标" in md
    # 4.1 >= 4.0 → 🔥 必看标记同时出现在目录和正文标题
    assert md.count("🔥") >= 2


def test_github_trending_low_rec_has_no_must_see_marker():
    summarizer = DailySummarizer()
    item = _project_item(1, objective=6.5, subjective=6.0)
    item.metadata["project_usage_zh"] = "可作为构建脚本参考。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-10-29", total_fetched=30, language="zh",
    ))

    assert "对这个项目有什么用" in md
    assert "3.1/5" in md
    assert "🔥" not in md


def test_non_project_items_have_no_star_rating_or_usage_section():
    summarizer = DailySummarizer()
    item = _scored_item(1, objective=9.0, subjective=9.0)
    item.metadata["project_usage_zh"] = "这条不该出现——新闻条目没有项目用途。"

    md = asyncio.run(summarizer.generate_summary(
        [item], "2026-10-29", total_fetched=30, language="zh",
    ))

    # 评星与项目用途只属于 GitHub 热榜条目
    assert "推荐 ⭐" not in md
    assert "对这个项目有什么用" not in md
    assert "🔥" not in md


# --- 2026-10-29: 参照项目（cw 私仓）注入 persona 段 -----------------------


def test_persona_section_includes_reference_project():
    persona = PersonaConfig(
        enabled=True,
        description="电子工程师/硬件开发者",
        location="沈阳",
        reference_project="CircuitWorkbench：KiCad 工程师的第二屏，Tauri+Rust。",
    )
    text = build_persona_section(persona)
    assert "CircuitWorkbench" in text
    assert "OWN project" in text
    assert "沈阳" in text


def test_persona_section_without_reference_project_stays_unchanged():
    text = build_persona_section(_PERSONA)
    assert "OWN project" not in text
    assert "电子工程师" in text


def test_enrichment_prompt_field9_targets_reference_project():
    from src.ai.prompts import CONTENT_ENRICHMENT_SYSTEM
    assert "project_usage" in CONTENT_ENRICHMENT_SYSTEM
    assert "reader's OWN project" in CONTENT_ENRICHMENT_SYSTEM
