#!/usr/bin/env python3
"""Generate all four Horizon boards on the VPS and publish them atomically.

The GitHub repository remains a backup. Production generation is local to the
VPS, while the existing ``Horizon-posts/sync-posts.sh`` renderer is reused in a
temporary Git worktree so its deployment clone is never left dirty.
"""

from __future__ import annotations

import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BJT = ZoneInfo("Asia/Shanghai")

# (published filename infix, configuration filename)
BOARD_CONFIGS = (
    ("horizon", "config.github.json"),
    ("global", "config.global.json"),
    ("github-trending", "config.github-trending.json"),
    ("ee", "config.ee.json"),
)


class PipelineError(RuntimeError):
    """Raised when a board or the final publication cannot be verified."""


class CommandRunner:
    def run(self, args, *, cwd=None, env=None, check=True):
        return subprocess.run(
            [str(arg) for arg in args],
            cwd=cwd,
            env=env,
            check=check,
        )


def _atomic_copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.tmp.{os.getpid()}")
    shutil.copy2(source, temporary)
    os.replace(temporary, destination)


def _artifact_paths(directory: Path, date: str) -> list[Path]:
    paths = [directory / f"{date}-{suffix}-zh.md" for suffix, _ in BOARD_CONFIGS]
    paths.append(directory / f"{date}-榜单汇总-zh.md")
    return paths


def _restore_previous(previous_dir: Path, summaries_dir: Path, date: str) -> None:
    for destination in _artifact_paths(summaries_dir, date):
        backup = previous_dir / destination.name
        if backup.exists():
            _atomic_copy(backup, destination)
        else:
            destination.unlink(missing_ok=True)


def generate_boards(
    repo: Path,
    date: str,
    *,
    hours: int,
    runner: CommandRunner | None = None,
) -> list[Path]:
    """Generate four boards, merging and installing only a complete set."""
    runner = runner or CommandRunner()
    repo = repo.resolve()
    data_dir = repo / "data"
    summaries_dir = data_dir / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)

    run_root = repo / "output" / "runs"
    run_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f"{date}.", dir=run_root))
    previous = staging / "previous"
    previous.mkdir()
    for current in _artifact_paths(summaries_dir, date):
        if current.exists():
            shutil.copy2(current, previous / current.name)

    canonical = summaries_dir / f"{date}-horizon-zh.md"
    completed = False
    try:
        for suffix, config_name in BOARD_CONFIGS:
            board_config = data_dir / config_name
            if not board_config.is_file():
                raise PipelineError(f"board {suffix}: missing config {board_config}")
            canonical.unlink(missing_ok=True)
            try:
                # HORIZON_DATE pins the board's internal report date. Without
                # it a run that crosses midnight has its later boards write
                # the next day's filename while this loop still looks for the
                # pinned one, and the whole run fails at the artifact check.
                board_env = os.environ.copy()
                board_env["HORIZON_DATE"] = date
                runner.run(
                    [
                        "docker",
                        "compose",
                        "run",
                        "--rm",
                        "--volume",
                        f"{board_config.resolve()}:/app/data/config.json:ro",
                        "horizon",
                        "--hours",
                        str(hours),
                    ],
                    cwd=repo,
                    env=board_env,
                )
            except Exception as exc:
                raise PipelineError(f"board {suffix} generation failed: {exc}") from exc
            if not canonical.is_file() or canonical.stat().st_size == 0:
                raise PipelineError(
                    f"board {suffix} did not produce {canonical.name}"
                )
            os.replace(canonical, staging / f"{date}-{suffix}-zh.md")

        lineage_output = staging / f"{date}-four-board-lineage.json"
        try:
            runner.run(
                [
                    sys.executable,
                    repo / "scripts" / "merge_boards.py",
                    "--date",
                    date,
                    "--summaries-dir",
                    staging,
                ],
                cwd=repo,
            )
        except Exception as exc:
            raise PipelineError(f"four-board merge failed: {exc}") from exc

        try:
            runner.run(
                [
                    sys.executable,
                    repo / "scripts" / "check_four_board_lineage.py",
                    "--date",
                    date,
                    "--summaries-dir",
                    staging,
                    "--json-out",
                    lineage_output,
                ],
                cwd=repo,
            )
        except Exception as exc:
            raise PipelineError(f"four-board lineage check failed: {exc}") from exc
        if not lineage_output.is_file() or lineage_output.stat().st_size == 0:
            raise PipelineError("four-board lineage checker produced no result")

        staged_artifacts = _artifact_paths(staging, date)
        missing = [path.name for path in staged_artifacts if not path.is_file() or path.stat().st_size == 0]
        if missing:
            raise PipelineError(f"incomplete staged publication: {', '.join(missing)}")

        installed = []
        for source in staged_artifacts:
            destination = summaries_dir / source.name
            _atomic_copy(source, destination)
            installed.append(destination)
        lineage_destination = repo / "output" / "lineage" / f"{date}-lineage.json"
        _atomic_copy(lineage_output, lineage_destination)
        completed = True
        return installed
    finally:
        if not completed:
            canonical.unlink(missing_ok=True)
            _restore_previous(previous, summaries_dir, date)
        shutil.rmtree(staging, ignore_errors=True)


def publish_reports(
    repo: Path,
    posts_repo: Path,
    date: str,
    *,
    runner: CommandRunner | None = None,
) -> None:
    """Overlay local reports on a clean master worktree and publish the site."""
    runner = runner or CommandRunner()
    repo = repo.resolve()
    posts_repo = posts_repo.resolve()
    sync_script = Path(
        os.environ.get("HORIZON_SYNC_SCRIPT", posts_repo / "sync-posts.sh")
    ).resolve()
    if not sync_script.is_file():
        raise PipelineError(f"publish script missing: {sync_script}")

    runner.run(["git", "-C", posts_repo, "fetch", "origin", "master"], cwd=repo)
    worktree_root = repo / "output" / "publish-worktrees"
    worktree_root.mkdir(parents=True, exist_ok=True)
    worktree = Path(tempfile.mkdtemp(prefix=f"{date}.", dir=worktree_root))
    worktree.rmdir()
    attached = False
    try:
        runner.run(
            ["git", "-C", posts_repo, "worktree", "add", "--detach", worktree, "origin/master"],
            cwd=repo,
        )
        attached = True
        posts = worktree / "docs" / "_posts"
        posts.mkdir(parents=True, exist_ok=True)
        for summary in sorted((repo / "data" / "summaries").glob("*.md")):
            shutil.copy2(summary, posts / summary.name)

        merged = posts / f"{date}-榜单汇总-zh.md"
        if not merged.is_file() or merged.stat().st_size == 0:
            raise PipelineError(f"final merged report missing from publish overlay: {merged}")

        final_lineage = repo / "output" / "lineage" / f"{date}-lineage.json"
        if not final_lineage.is_file():
            raise PipelineError(f"final lineage result missing: {final_lineage}")
        index_path = posts / "index.md"
        index_updater = repo / "scripts" / "update_reports_index.py"
        if not index_path.is_file() or not index_updater.is_file():
            raise PipelineError(
                f"reports index updater inputs missing: {index_path} {index_updater}"
            )
        try:
            runner.run(
                [
                    sys.executable,
                    index_updater,
                    "--index",
                    index_path,
                    "--date",
                    date,
                    "--lineage",
                    final_lineage,
                ],
                cwd=repo,
            )
        except Exception as exc:
            raise PipelineError(f"reports navigation index update failed: {exc}") from exc
        index_text = index_path.read_text(encoding="utf-8")
        if (
            f"最新日报（{date}" not in index_text
            or f"/reports-html/{date}.html" not in index_text
        ):
            raise PipelineError(f"reports navigation index is stale for {date}")

        publish_env = os.environ.copy()
        publish_env.update(
            {
                "HORIZON_POSTS_REPO": str(worktree),
                "HORIZON_REPO": str(repo),
                "HORIZON_SKIP_GIT_PULL": "1",
                "HORIZON_DATE": date,
            }
        )
        runner.run([sync_script], cwd=posts_repo, env=publish_env)

        site_root = Path(
            os.environ.get("HORIZON_SITE_ROOT", "/var/www/horizon-site")
        )
        public_lineage = (
            site_root / "reports-html" / "data" / f"{date}-lineage.json"
        )
        _atomic_copy(final_lineage, public_lineage)
    except Exception as exc:
        if isinstance(exc, PipelineError):
            raise
        raise PipelineError(f"site publication failed: {exc}") from exc
    finally:
        if attached:
            runner.run(
                ["git", "-C", posts_repo, "worktree", "remove", "--force", worktree],
                cwd=repo,
                check=False,
            )
        shutil.rmtree(worktree, ignore_errors=True)


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}


def _publication_is_current(repo: Path, date: str) -> bool:
    marker = _read_json(repo / "output" / "last-success.json")
    site_root = Path(os.environ.get("HORIZON_SITE_ROOT", "/var/www/horizon-site"))
    html = site_root / "reports-html" / f"{date}.html"
    lineage = _read_json(
        site_root / "reports-html" / "data" / f"{date}-lineage.json"
    )
    return (
        marker.get("date") == date
        and marker.get("published") is True
        and html.is_file()
        and lineage.get("date") == date
        and lineage.get("passed") is True
    )


def _existing_artifacts(repo: Path, date: str) -> list[Path]:
    artifacts = _artifact_paths(repo / "data" / "summaries", date)
    missing = [path.name for path in artifacts if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise PipelineError(f"publish retry has incomplete artifacts: {', '.join(missing)}")
    lineage = _read_json(repo / "output" / "lineage" / f"{date}-lineage.json")
    if lineage.get("date") != date or lineage.get("passed") is not True:
        raise PipelineError("publish retry has no passed four-board lineage result")
    return artifacts


def _pending_publication_artifacts(repo: Path, date: str) -> list[Path] | None:
    """Return a complete generated set awaiting publication, if one exists."""
    marker = _read_json(repo / "output" / "last-success.json")
    if marker.get("date") != date or marker.get("published") is not False:
        return None
    try:
        return _existing_artifacts(repo, date)
    except PipelineError as exc:
        print(
            f"Horizon VPS daily pending publication is invalid; regenerating: {exc}",
            flush=True,
        )
        return None


def _write_success_marker(
    repo: Path,
    date: str,
    artifacts: list[Path],
    *,
    published: bool,
) -> None:
    marker = repo / "output" / "last-success.json"
    marker.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "date": date,
        "completed_at": datetime.now(BJT).isoformat(),
        "artifacts": [path.name for path in artifacts],
        "published": published,
    }
    temporary = marker.with_name(f".{marker.name}.tmp.{os.getpid()}")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(temporary, marker)


def main() -> int:
    repo = Path(os.environ.get("HORIZON_REPO", "/home/pengyinyu/Horizon"))
    posts_repo = Path(
        os.environ.get("HORIZON_POSTS_REPO", "/home/pengyinyu/Horizon-posts")
    )
    date = os.environ.get("HORIZON_DATE") or datetime.now(BJT).strftime("%Y-%m-%d")
    hours = int(os.environ.get("HORIZON_HOURS", "24"))
    lock_path = Path(
        os.environ.get("HORIZON_RUN_LOCK", "/home/pengyinyu/.horizon-run-daily.lock")
    )
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    with lock_path.open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(f"run skipped: lock busy ({lock_path})", flush=True)
            return 75

        print(f"Horizon VPS daily start date={date} hours={hours}", flush=True)
        if os.environ.get("HORIZON_FORCE") != "1" and _publication_is_current(repo, date):
            print(f"Horizon VPS daily skip: {date} is already published", flush=True)
            return 0

        publish_only = os.environ.get("HORIZON_PUBLISH_ONLY") == "1"
        pending_artifacts = None
        if os.environ.get("HORIZON_FORCE") != "1" and not publish_only:
            pending_artifacts = _pending_publication_artifacts(repo, date)

        if publish_only:
            artifacts = _existing_artifacts(repo, date)
        elif pending_artifacts is not None:
            artifacts = pending_artifacts
            print(
                f"Horizon VPS daily resume publication date={date}", flush=True
            )
        else:
            artifacts = generate_boards(repo, date, hours=hours)
            _write_success_marker(repo, date, artifacts, published=False)

        should_publish = os.environ.get("HORIZON_SKIP_PUBLISH") != "1"
        if should_publish:
            publish_reports(repo, posts_repo, date)
        _write_success_marker(
            repo,
            date,
            artifacts,
            published=should_publish,
        )
        print(f"Horizon VPS daily complete date={date} artifacts={len(artifacts)}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"Horizon VPS daily FAILED: {type(error).__name__}: {error}", file=sys.stderr)
        raise
