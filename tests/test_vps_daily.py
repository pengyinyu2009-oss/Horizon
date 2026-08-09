from __future__ import annotations

from pathlib import Path

import pytest

from scripts.vps_daily import (
    BOARD_CONFIGS,
    PipelineError,
    _publication_is_current,
    generate_boards,
)


def _prepare_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "Horizon"
    data = repo / "data"
    summaries = data / "summaries"
    scripts = repo / "scripts"
    summaries.mkdir(parents=True)
    scripts.mkdir()
    (scripts / "merge_boards.py").write_text("# fake merge script\n", encoding="utf-8")
    (data / "config.json").write_text("original-config", encoding="utf-8")
    for _, config_name in BOARD_CONFIGS:
        (data / config_name).write_text(config_name, encoding="utf-8")
    return repo


class FakeRunner:
    def __init__(self, repo: Path, date: str, fail_on: str | None = None):
        self.repo = repo
        self.date = date
        self.fail_on = fail_on
        self.calls: list[tuple[str, ...]] = []

    def run(self, args, *, cwd=None, env=None):
        call = tuple(str(arg) for arg in args)
        self.calls.append(call)
        config = (self.repo / "data/config.json").read_text(encoding="utf-8")
        if call[:4] == ("docker", "compose", "run", "--rm"):
            if self.fail_on and self.fail_on in config:
                raise RuntimeError(f"simulated failure for {config}")
            output = self.repo / "data/summaries" / f"{self.date}-horizon-zh.md"
            output.write_text(f"generated from {config}\n", encoding="utf-8")
        elif "merge_boards.py" in " ".join(call):
            staging = Path(call[call.index("--summaries-dir") + 1])
            (staging / f"{self.date}-榜单汇总-zh.md").write_text(
                "merged four boards\n", encoding="utf-8"
            )
        elif "check_four_board_lineage.py" in " ".join(call):
            output = Path(call[call.index("--json-out") + 1])
            output.write_text('{"passed": true}\n', encoding="utf-8")


def test_generate_boards_publishes_five_artifacts_only_after_all_succeed(tmp_path):
    repo = _prepare_repo(tmp_path)
    date = "2026-08-10"
    runner = FakeRunner(repo, date)

    artifacts = generate_boards(repo, date, hours=24, runner=runner)

    assert {path.name for path in artifacts} == {
        f"{date}-horizon-zh.md",
        f"{date}-global-zh.md",
        f"{date}-github-trending-zh.md",
        f"{date}-ee-zh.md",
        f"{date}-榜单汇总-zh.md",
    }
    for suffix, config_name in BOARD_CONFIGS:
        expected = repo / "data/summaries" / f"{date}-{suffix}-zh.md"
        assert config_name in expected.read_text(encoding="utf-8")
    assert (repo / "data/config.json").read_text(encoding="utf-8") == "original-config"
    assert (repo / "output/lineage" / f"{date}-lineage.json").is_file()


def test_generate_boards_keeps_previous_publication_when_one_board_fails(tmp_path):
    repo = _prepare_repo(tmp_path)
    date = "2026-08-10"
    summaries = repo / "data/summaries"
    previous = {}
    for suffix, _ in BOARD_CONFIGS:
        path = summaries / f"{date}-{suffix}-zh.md"
        path.write_text(f"previous-{suffix}\n", encoding="utf-8")
        previous[path] = path.read_text(encoding="utf-8")
    merged = summaries / f"{date}-榜单汇总-zh.md"
    merged.write_text("previous-merged\n", encoding="utf-8")
    previous[merged] = merged.read_text(encoding="utf-8")
    runner = FakeRunner(repo, date, fail_on="config.global.json")

    with pytest.raises(PipelineError, match="global"):
        generate_boards(repo, date, hours=24, runner=runner)

    assert {path: path.read_text(encoding="utf-8") for path in previous} == previous
    assert (repo / "data/config.json").read_text(encoding="utf-8") == "original-config"


def test_publication_is_current_requires_marker_html_and_passed_lineage(tmp_path, monkeypatch):
    repo = tmp_path / "Horizon"
    site = tmp_path / "site"
    date = "2026-08-10"
    (repo / "output").mkdir(parents=True)
    (site / "reports-html/data").mkdir(parents=True)
    (repo / "output/last-success.json").write_text(
        '{"date": "2026-08-10", "published": true}', encoding="utf-8"
    )
    (site / "reports-html" / f"{date}.html").write_text(date, encoding="utf-8")
    lineage = site / "reports-html/data" / f"{date}-lineage.json"
    lineage.write_text('{"date": "2026-08-10", "passed": true}', encoding="utf-8")
    monkeypatch.setenv("HORIZON_SITE_ROOT", str(site))

    assert _publication_is_current(repo, date) is True

    lineage.write_text('{"date": "2026-08-10", "passed": false}', encoding="utf-8")
    assert _publication_is_current(repo, date) is False
