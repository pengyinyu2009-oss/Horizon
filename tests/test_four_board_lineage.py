from pathlib import Path

from scripts.check_four_board_lineage import verify_four_board_lineage


BOARD_FILES = {
    "global": "global",
    "ai": "horizon",
    "github": "github-trending",
    "ee": "ee",
}


def _item(index: int, title: str) -> str:
    return (
        f'<a id="item-{index}"></a>\n'
        f'## [{title}](https://example.com/{index}) ⭐️ 8.0/10\n\n'
        "summary\n\n---\n"
    )


def _write_complete_report(root: Path, date: str) -> None:
    for anchor, infix in BOARD_FILES.items():
        (root / f"{date}-{infix}-zh.md").write_text(
            _item(1, f"{anchor} story"), encoding="utf-8"
        )
    merged = "\n".join(
        f'<a id="sec-{anchor}"></a>\n<a id="item-{anchor}-1"></a>'
        for anchor in BOARD_FILES
    )
    (root / f"{date}-榜单汇总-zh.md").write_text(merged, encoding="utf-8")


def test_final_lineage_validates_all_four_sources_and_merged_page(tmp_path):
    date = "2026-08-10"
    _write_complete_report(tmp_path, date)

    result = verify_four_board_lineage(tmp_path, date)

    assert result["passed"] is True
    assert result["total_items"] == 4
    assert set(result["boards"]) == set(BOARD_FILES)


def test_final_lineage_fails_when_merged_page_drops_a_board_item(tmp_path):
    date = "2026-08-10"
    _write_complete_report(tmp_path, date)
    merged = tmp_path / f"{date}-榜单汇总-zh.md"
    merged.write_text(
        merged.read_text(encoding="utf-8").replace(
            '<a id="item-ee-1"></a>', ""
        ),
        encoding="utf-8",
    )

    result = verify_four_board_lineage(tmp_path, date)

    assert result["passed"] is False
    assert result["boards"]["ee"]["source_items"] == 1
    assert result["boards"]["ee"]["merged_items"] == 0


def test_final_lineage_maps_github_subboard_item_anchors(tmp_path):
    date = "2026-08-10"
    _write_complete_report(tmp_path, date)
    github = tmp_path / f"{date}-github-trending-zh.md"
    github.write_text(
        '<a id="item-daily-1"></a>\n'
        '## [daily](https://example.com/daily) ⭐️ 8.0/10\n\n'
        '<a id="item-weekly-1"></a>\n'
        '## [weekly](https://example.com/weekly) ⭐️ 8.0/10\n\n'
        '<a id="item-monthly-1"></a>\n'
        '## [monthly](https://example.com/monthly) ⭐️ 8.0/10\n',
        encoding="utf-8",
    )
    merged = tmp_path / f"{date}-榜单汇总-zh.md"
    merged.write_text(
        merged.read_text(encoding="utf-8").replace(
            '<a id="item-github-1"></a>',
            '\n'.join(
                [
                    '<a id="item-github-daily-1"></a>',
                    '<a id="item-github-weekly-1"></a>',
                    '<a id="item-github-monthly-1"></a>',
                ]
            ),
        ),
        encoding="utf-8",
    )

    result = verify_four_board_lineage(tmp_path, date)

    assert result["passed"] is True
    assert result["boards"]["github"]["source_items"] == 3
    assert result["boards"]["github"]["valid_items"] == 3
    assert result["boards"]["github"]["merged_items"] == 3


def test_final_lineage_rejects_an_empty_board(tmp_path):
    date = "2026-08-10"
    _write_complete_report(tmp_path, date)
    (tmp_path / f"{date}-github-trending-zh.md").write_text(
        "## GitHub trending\n\nNo items today.\n", encoding="utf-8"
    )
    merged = tmp_path / f"{date}-榜单汇总-zh.md"
    merged.write_text(
        merged.read_text(encoding="utf-8").replace(
            '<a id="item-github-1"></a>', ""
        ),
        encoding="utf-8",
    )

    result = verify_four_board_lineage(tmp_path, date)

    assert result["passed"] is False
    assert result["boards"]["github"]["source_items"] == 0
