from __future__ import annotations

from pathlib import Path
import fcntl
import json
import os
import shutil
import subprocess
from unittest.mock import Mock

import pytest

import scripts.vps_daily as vps_daily
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
        self.host_configs_seen: list[str] = []

    def run(self, args, *, cwd=None, env=None):
        call = tuple(str(arg) for arg in args)
        self.calls.append(call)
        if call[:3] == ("docker", "compose", "run"):
            host_config = (self.repo / "data/config.json").read_text(
                encoding="utf-8"
            )
            self.host_configs_seen.append(host_config)
            if "--volume" in call:
                volume = call[call.index("--volume") + 1]
                source = volume.removesuffix(":/app/data/config.json:ro")
                config = Path(source).read_text(encoding="utf-8")
            else:
                config = host_config
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


def test_generate_boards_mounts_each_config_without_mutating_host_config(tmp_path):
    repo = _prepare_repo(tmp_path)
    date = "2026-08-10"
    runner = FakeRunner(repo, date)

    generate_boards(repo, date, hours=24, runner=runner)

    assert runner.host_configs_seen == ["original-config"] * len(BOARD_CONFIGS)
    docker_calls = [
        call for call in runner.calls if call[:3] == ("docker", "compose", "run")
    ]
    mounted_sources = {
        call[call.index("--volume") + 1].removesuffix(
            ":/app/data/config.json:ro"
        )
        for call in docker_calls
    }
    assert mounted_sources == {
        str((repo / "data" / config_name).resolve())
        for _, config_name in BOARD_CONFIGS
    }


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


def test_local_wrapper_leaves_locking_to_python_pipeline(tmp_path):
    lock_path = tmp_path / "horizon.lock"
    log_path = tmp_path / "cron.log"
    with lock_path.open("w") as held_lock:
        fcntl.flock(held_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        environment = os.environ.copy()
        environment.update(
            {
                "HORIZON_REPO": str(tmp_path),
                "HORIZON_RUN_LOG": str(log_path),
                "HORIZON_RUN_LOCK": str(lock_path),
                "HORIZON_PYTHON": str(shutil.which("true")),
                "HORIZON_EXECUTION_MODE": "local",
            }
        )
        result = subprocess.run(
            ["bash", "run-daily.sh"],
            cwd=Path(__file__).resolve().parents[1],
            env=environment,
            check=False,
        )

    assert result.returncode == 0


def test_wrapper_defaults_to_vps_local_pipeline(tmp_path):
    log_path = tmp_path / "cron.log"
    capture_path = tmp_path / "script.txt"
    fake_python = tmp_path / "fake-python"
    fake_python.write_text(
        '#!/bin/sh\nprintf "%s" "$1" > "$HORIZON_SCRIPT_CAPTURE"\n',
        encoding="utf-8",
    )
    fake_python.chmod(0o755)
    environment = os.environ.copy()
    environment.update(
        {
            "HORIZON_REPO": str(tmp_path),
            "HORIZON_RUN_LOG": str(log_path),
            "HORIZON_RUN_LOCK": str(tmp_path / "horizon.lock"),
            "HORIZON_PYTHON": str(fake_python),
            "HORIZON_SCRIPT_CAPTURE": str(capture_path),
        }
    )
    environment.pop("HORIZON_EXECUTION_MODE", None)

    result = subprocess.run(
        ["bash", "run-daily.sh"],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        check=False,
    )

    assert result.returncode == 0
    assert capture_path.read_text(encoding="utf-8").endswith(
        "scripts/vps_daily.py"
    )


def test_failed_publish_is_resumed_without_regenerating_boards(tmp_path, monkeypatch):
    repo = _prepare_repo(tmp_path)
    posts_repo = tmp_path / "Horizon-posts"
    posts_repo.mkdir()
    date = "2026-08-10"
    summaries = repo / "data/summaries"
    artifacts = [
        summaries / f"{date}-{suffix}-zh.md" for suffix, _ in BOARD_CONFIGS
    ]
    artifacts.append(summaries / f"{date}-榜单汇总-zh.md")
    for artifact in artifacts:
        artifact.write_text("complete\n", encoding="utf-8")
    lineage = repo / "output/lineage" / f"{date}-lineage.json"
    lineage.parent.mkdir(parents=True)
    lineage.write_text(
        json.dumps({"date": date, "passed": True}), encoding="utf-8"
    )

    generate = Mock(return_value=artifacts)
    publish = Mock(side_effect=PipelineError("network down"))
    monkeypatch.setattr(vps_daily, "generate_boards", generate)
    monkeypatch.setattr(vps_daily, "publish_reports", publish)
    monkeypatch.setattr(vps_daily, "_publication_is_current", lambda *_: False)
    monkeypatch.setenv("HORIZON_REPO", str(repo))
    monkeypatch.setenv("HORIZON_POSTS_REPO", str(posts_repo))
    monkeypatch.setenv("HORIZON_DATE", date)
    monkeypatch.setenv("HORIZON_RUN_LOCK", str(tmp_path / "daily.lock"))
    monkeypatch.delenv("HORIZON_FORCE", raising=False)
    monkeypatch.delenv("HORIZON_PUBLISH_ONLY", raising=False)
    monkeypatch.delenv("HORIZON_SKIP_PUBLISH", raising=False)

    with pytest.raises(PipelineError, match="network down"):
        vps_daily.main()

    marker = json.loads(
        (repo / "output/last-success.json").read_text(encoding="utf-8")
    )
    assert marker["date"] == date
    assert marker["published"] is False

    publish.side_effect = None
    assert vps_daily.main() == 0

    assert generate.call_count == 1
    assert publish.call_count == 2
    marker = json.loads(
        (repo / "output/last-success.json").read_text(encoding="utf-8")
    )
    assert marker["published"] is True
