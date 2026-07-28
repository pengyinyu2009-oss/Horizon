"""Tests for scripts/merge_boards.py (four-board daily merge)."""

import asyncio
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import merge_boards  # noqa: E402
from src.ai.summarizer import DailySummarizer  # noqa: E402
from src.models import ContentItem, SourceType  # noqa: E402

DATE = "2026-07-28"


def _item(idx: int, score: float = 8.5) -> ContentItem:
    item = ContentItem(
        id=f"rss:item-{idx}",
        source_type=SourceType.RSS,
        title=f"Board Item {idx}",
        url=f"https://example.com/items/{idx}",
        content="content",
        author="tester",
        published_at=datetime(2026, 7, 27, 8, 0, tzinfo=timezone.utc),
    )
    item.ai_score = score
    item.ai_summary = f"Summary {idx}."
    item.ai_tags = ["t"]
    return item


def _write_board(summaries_dir: Path, infix: str, items, front_matter: bool = True):
    md = asyncio.run(DailySummarizer().generate_summary(
        items, DATE, total_fetched=len(items), language="zh",
    ))
    if front_matter:
        md = f"---\nlayout: default\ndate: {DATE}\n---\n\n" + md
    (summaries_dir / f"{DATE}-{infix}-zh.md").write_text(md, encoding="utf-8")


def test_merge_four_boards(tmp_path):
    _write_board(tmp_path, "global", [_item(1), _item(2)])
    _write_board(tmp_path, "horizon", [_item(3)])
    _write_board(tmp_path, "github-trending", [_item(4)])
    _write_board(tmp_path, "ee", [_item(5)])

    merged, missing = merge_boards.merge_boards(DATE, tmp_path)

    assert missing == []
    # Sections and nav.
    for anchor, label in (("global", "🌍 全球新闻"), ("ai", "🤖 Horizon 总榜"),
                          ("github", "🔥 GitHub 热榜"), ("ee", "🔧 电子工程师")):
        assert f'<a id="sec-{anchor}"></a>' in merged
        assert f"## {label}" in merged
        assert f"[{label}](#sec-{anchor})" in merged
    # Board H1 dropped, merged H1 present exactly once.
    assert merged.count("# Horizon 每日速递") == 0
    assert merged.count("# Horizon 日报 · 2026-07-28") == 1
    # Anchors namespaced per board, TOC links follow.
    assert '<a id="item-global-1"></a>' in merged
    assert '<a id="item-ai-1"></a>' in merged
    assert "](#item-ee-1)" in merged
    # Headings demoted: board item headers are now h3.
    assert "### [Board Item 1](https://example.com/items/1)" in merged
    # Front matter of the merged file itself.
    assert merged.startswith("---\nlayout: default")
    assert 'title: "Horizon 日报(4 榜单):2026-07-28 (ZH)"' in merged
    # Item counts in section labels.
    assert "🌍 全球新闻（2 条）" in merged


def test_merge_missing_board_placeholder(tmp_path):
    _write_board(tmp_path, "horizon", [_item(1)])

    merged, missing = merge_boards.merge_boards(DATE, tmp_path)

    assert set(missing) == {"global", "github", "ee"}
    assert "⚠️ 今日该榜单未生成" in merged
    assert merged.count("⚠️ 今日该榜单未生成") == 3
    assert '<a id="item-ai-1"></a>' in merged


def test_merge_all_missing_returns_1(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["merge_boards.py", "--date", DATE,
                                      "--summaries-dir", str(tmp_path)])
    rc = merge_boards.main()
    assert rc == 1
    _, missing = merge_boards.merge_boards(DATE, tmp_path)
    assert len(missing) == 4


def test_scoring_failure_banner_kept(tmp_path):
    failure_md = (
        "---\nlayout: default\n---\n\n"
        f"# 【评分故障空报】Horizon 每日简报 - {DATE}\n\n"
        "> 评分服务故障：共抓取 10 条。\n"
    )
    (tmp_path / f"{DATE}-horizon-zh.md").write_text(failure_md, encoding="utf-8")

    merged, _ = merge_boards.merge_boards(DATE, tmp_path)

    assert "【评分故障空报】" in merged
    # Banner demoted from H1 to H2, not dropped.
    assert f"## 【评分故障空报】Horizon 每日简报 - {DATE}" in merged


def test_github_trending_grouped_board_namespaces_cleanly(tmp_path):
    items = []
    for period in ("daily", "weekly", "monthly"):
        for j in range(2):
            it = _item(j + 1)
            it.metadata["period"] = period
            items.append(it)
    _write_board(tmp_path, "github-trending", items)

    merged, _ = merge_boards.merge_boards(DATE, tmp_path)

    assert '<a id="item-github-daily-1"></a>' in merged
    assert "](#item-github-weekly-1)" in merged
    assert "📅 日榜" in merged
