"""Tests for the GitHub Trending board scraper (2026-07-28)."""

import asyncio
from datetime import datetime, timezone
from pathlib import Path

import httpx
import pytest

from src.models import ContentItem, GitHubTrendingConfig, SourceType
from src.scrapers.github_trending import GitHubTrendingScraper

FIXTURE = (
    Path(__file__).parent / "fixtures" / "github_trending.html"
).read_text(encoding="utf-8")


def _scraper(**overrides) -> GitHubTrendingScraper:
    cfg = GitHubTrendingConfig(enabled=True, **overrides)
    client = httpx.AsyncClient()
    return GitHubTrendingScraper(cfg, client)


# --- pure HTML parsing -------------------------------------------------------


def test_parse_trending_html_extracts_all_fields():
    rows = GitHubTrendingScraper.parse_trending_html(FIXTURE, "daily")

    assert len(rows) == 3
    repo, desc, lang, url, stars, forks, gained = rows[0]
    assert repo == "astral-sh/uv"
    assert "extremely fast Python" in desc
    assert lang == "Rust"
    assert url == "https://github.com/astral-sh/uv"
    assert stars == 62134
    assert forks == 1823
    assert gained == 1024

    # Second row: weekly increment label parsed the same way.
    assert rows[1][6] == 356
    # Third row: no description / no language — still parsed.
    assert rows[2][0] == "sindresorhus/awesome"
    assert rows[2][1] == ""
    assert rows[2][2] == ""
    assert rows[2][6] == 2468


def test_parse_trending_html_handles_garbage():
    assert GitHubTrendingScraper.parse_trending_html("<html></html>", "daily") == []
    assert GitHubTrendingScraper.parse_trending_html("not html", "daily") == []


# --- fetch orchestration ------------------------------------------------------


def _mock_fetch_board(rows_by_period):
    async def fake(self, period, language):
        return rows_by_period.get(period, [])
    return fake


def test_fetch_all_three_periods(monkeypatch):
    rows = GitHubTrendingScraper.parse_trending_html(FIXTURE, "daily")
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board",
        _mock_fetch_board({"daily": rows, "weekly": rows, "monthly": rows}),
    )
    scraper = _scraper()

    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    periods = {it.metadata["period"] for it in items}
    assert periods == {"daily", "weekly", "monthly"}
    assert len(items) == 9
    first = items[0]
    assert first.source_type == SourceType.GITHUB_TRENDING
    assert first.title == "astral-sh/uv (+1024⭐ today)"
    assert "Total stars: 62134" in first.content
    asyncio.run(scraper.client.aclose())


def test_fetch_caps_per_period(monkeypatch):
    rows = GitHubTrendingScraper.parse_trending_html(FIXTURE, "daily")
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board",
        _mock_fetch_board({"daily": rows}),
    )
    scraper = _scraper(periods=["daily"], max_items=2)

    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    assert len(items) == 2
    assert items[0].metadata["repo"] == "astral-sh/uv"  # page order = ranking
    asyncio.run(scraper.client.aclose())


def test_min_stars_and_keyword_filters(monkeypatch):
    rows = GitHubTrendingScraper.parse_trending_html(FIXTURE, "daily")
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board", _mock_fetch_board({"daily": rows}),
    )
    scraper = _scraper(periods=["daily"], min_stars=10000, keywords=["risc-v"])

    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    # awesome (350k stars, no keyword) filtered by keyword;
    # cva6 (2.7k stars, keyword hit) filtered by min_stars;
    # uv has stars but no keyword → nothing passes both.
    assert items == []

    scraper2 = _scraper(periods=["daily"], keywords=["risc-v"])
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board", _mock_fetch_board({"daily": rows}),
    )
    items2 = asyncio.run(scraper2.fetch(datetime.now(timezone.utc)))
    assert [it.metadata["repo"] for it in items2] == ["openhwgroup/cva6"]
    asyncio.run(scraper.client.aclose())
    asyncio.run(scraper2.client.aclose())


def test_fallback_to_ossinsight_when_html_empty(monkeypatch):
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board", _mock_fetch_board({})
    )

    oss_item = ContentItem(
        id="ossinsight:trending:123",
        source_type=SourceType.OSSINSIGHT,
        title="openhwgroup/cva6 (+99⭐ past_24_hours)",
        url="https://github.com/openhwgroup/cva6",
        content="fallback row",
        author="openhwgroup",
        published_at=datetime.now(timezone.utc),
        metadata={"repo": "openhwgroup/cva6", "stars_gained": 99,
                  "primary_language": "SystemVerilog"},
    )

    async def fake_oss_fetch(self, since):
        return [oss_item]

    monkeypatch.setattr(
        "src.scrapers.ossinsight.OSSInsightScraper.fetch", fake_oss_fetch
    )

    scraper = _scraper(periods=["daily"])
    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    assert len(items) == 1
    item = items[0]
    assert item.source_type == SourceType.GITHUB_TRENDING
    assert item.metadata["period"] == "daily"
    assert item.metadata["fallback"] == "ossinsight"
    assert item.title == "openhwgroup/cva6 (+99⭐ today)"
    assert item.id == "github_trending:daily:openhwgroup/cva6"
    asyncio.run(scraper.client.aclose())


def test_alert_when_everything_empty(monkeypatch, capsys):
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board", _mock_fetch_board({})
    )

    async def empty_oss(self, since):
        return []

    monkeypatch.setattr(
        "src.scrapers.ossinsight.OSSInsightScraper.fetch", empty_oss
    )

    scraper = _scraper(periods=["daily"])
    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    assert items == []
    out = capsys.readouterr().out
    assert "falling back to OSS Insight" in out
    assert "ALERT github_trending_empty" in out
    asyncio.run(scraper.client.aclose())


def test_no_fallback_when_disabled(monkeypatch, capsys):
    monkeypatch.setattr(
        GitHubTrendingScraper, "_fetch_board", _mock_fetch_board({})
    )
    scraper = _scraper(periods=["daily"], fallback_to_ossinsight=False)

    items = asyncio.run(scraper.fetch(datetime.now(timezone.utc)))

    assert items == []
    assert "falling back" not in capsys.readouterr().out
    asyncio.run(scraper.client.aclose())


def test_disabled_config_fetches_nothing():
    cfg = GitHubTrendingConfig(enabled=False)
    scraper = GitHubTrendingScraper(cfg, httpx.AsyncClient())
    assert asyncio.run(scraper.fetch(datetime.now(timezone.utc))) == []
    asyncio.run(scraper.client.aclose())
