"""Tests for the PWA app feed builder."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_app_feed import build_feed  # noqa: E402


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def test_feed_parses_all_four_boards(tmp_path):
    d = tmp_path
    _write(d / "2026-11-04-global-zh.md", (
        "<a id=\"item-1\"></a>\n"
        "## [全球条目甲](https://e.com/1) ⭐️ 9.0/10 · 相关 5/10\n\n"
        "全球摘要。\n\n"
        "rss · X · 11月04日 09:00\n\n"
        "**入选理由**: 理由甲。\n\n"
        "**对中国影响**: 影响甲。\n\n"
        "**对沈阳影响**: 影响甲沈。\n\n"
        "**对我影响**: 影响甲我。\n\n---\n\n"
        "<a id=\"item-2\"></a>\n"
        "## [全球条目乙](https://e.com/2) ⭐️ 8.0/10\n\n"
        "全球摘要乙。\n\n"
        "rss · Y · 11月04日 08:00\n\n"
        "**入选理由**: 理由乙。\n\n---\n"
    ))
    _write(d / "2026-11-04-github-trending-zh.md", (
        "<a id=\"item-daily-1\"></a>\n"
        "## 🔥 [owner/repo A](https://github.com/a) ⭐️ 7.0/10 · 相关 8/10 · 推荐 ⭐️⭐️⭐️⭐️☆ 4.2/5\n\n"
        "摘要 A。\n\n"
        "github_trending · owner · 11月04日 09:00 · ⭐ 30.6万 总星标\n\n"
        "**对这个项目有什么用**: 可集成到 cw 的 agent-mcp 模块。\n\n"
        "**入选理由**: 热度高。\n\n---\n"
    ))

    feed = build_feed(d, "2026-11-04")

    assert feed["total"] == 3
    assert feed["boards_ok"] == 2
    assert feed["date"] == "2026-11-04"
    g = feed["boards"][0]
    assert g["id"] == "global" and len(g["items"]) == 2
    a = g["items"][0]
    assert a["sections"]["impact_cn"] == "影响甲。"
    assert a["sections"]["impact_local"] == "影响甲沈。"
    assert a["sections"]["impact_me"] == "影响甲我。"
    assert a["sections"]["pick_reason"] == "理由甲。"
    gh = feed["boards"][2]
    assert gh["id"] == "github-trending"
    item = gh["items"][0]
    assert item["must_see"] is True
    assert item["rec"] == 4.2 and item["rec_stars"] == 4
    assert item["stars"] == "30.6万"
    assert item["sections"]["project_usage"] == "可集成到 cw 的 agent-mcp 模块。"


def test_feed_missing_board_counts_ok(tmp_path):
    d = tmp_path
    _write(d / "2026-11-04-global-zh.md", (
        "<a id=\"item-1\"></a>\n"
        "## [甲](https://e.com/1) ⭐️ 8.0/10\n\n"
        "摘要。\n\n---\n"
    ))
    feed = build_feed(d, "2026-11-04")
    assert feed["boards_ok"] == 1
    assert feed["total"] == 1
    assert feed["boards"][1]["items"] == []
