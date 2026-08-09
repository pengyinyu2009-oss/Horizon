#!/usr/bin/env python3
"""VPS scheduler for the secret-backed GitHub daily workflow.

The VPS owns the 08:17 Beijing schedule. GitHub Actions owns AI generation so
production model credentials remain in GitHub Secrets. After a successful run,
the VPS immediately pulls and atomically publishes the generated reports.
"""

from __future__ import annotations

import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


def build_dispatch_payload(*, force: bool) -> dict:
    return {
        "ref": "main",
        "inputs": {"mode": "daily", "force": "true" if force else "false"},
    }


def _parse_github_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def select_dispatched_run(runs: list[dict], dispatched_at: datetime) -> dict | None:
    earliest = dispatched_at - timedelta(seconds=10)
    candidates = [
        run
        for run in runs
        if run.get("event") == "workflow_dispatch"
        and run.get("created_at")
        and _parse_github_time(run["created_at"]) >= earliest
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda run: _parse_github_time(run["created_at"]))


def _env_value(path: Path, name: str) -> str:
    if value := os.environ.get(name):
        return value
    if not path.is_file():
        return ""
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key.strip() == name:
            return value.strip().strip('"').strip("'")
    return ""


class GitHubAPI:
    def __init__(self, token: str, repository: str):
        self.token = token
        self.repository = repository
        self.base = f"https://api.github.com/repos/{repository}"

    def request(self, method: str, path: str, payload: dict | None = None):
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(
            f"{self.base}{path}",
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "horizon-vps-scheduler/1.0",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                body = response.read()
                return response.status, json.loads(body) if body else None
        except urllib.error.HTTPError as error:
            message = ""
            try:
                payload = json.loads(error.read())
                message = payload.get("message", "")
            except (ValueError, OSError):
                pass
            raise RuntimeError(
                f"GitHub API {method} {path} failed: HTTP {error.code} {message}"
            ) from error

    def path_exists(self, repository_path: str, ref: str) -> bool:
        path = urllib.parse.quote(repository_path, safe="/")
        try:
            status, _ = self.request("GET", f"/contents/{path}?ref={ref}")
            return status == 200
        except RuntimeError as error:
            if "HTTP 404" in str(error):
                return False
            raise


def _reports_exist(api: GitHubAPI, date: str) -> bool:
    base = "docs/_posts"
    return api.path_exists(f"{base}/{date}-horizon-zh.md", "master") and api.path_exists(
        f"{base}/{date}-榜单汇总-zh.md", "master"
    )


def _sync_site(repo: Path, date: str) -> None:
    sync_script = Path(
        os.environ.get(
            "HORIZON_SYNC_SCRIPT", "/home/pengyinyu/Horizon-posts/sync-posts.sh"
        )
    )
    environment = os.environ.copy()
    environment.update({"HORIZON_REPO": str(repo), "HORIZON_DATE": date})
    subprocess.run([sync_script], env=environment, check=True)


def main() -> int:
    repo = Path(os.environ.get("HORIZON_REPO", "/home/pengyinyu/Horizon"))
    repository = os.environ.get("HORIZON_GITHUB_REPOSITORY", "pengyinyu2009-oss/Horizon")
    token = _env_value(repo / ".env", "GITHUB_TOKEN")
    if not token:
        raise RuntimeError("GITHUB_TOKEN is missing from the VPS environment")
    api = GitHubAPI(token, repository)
    date = os.environ.get("HORIZON_DATE") or datetime.now(
        timezone(timedelta(hours=8))
    ).strftime("%Y-%m-%d")

    if _reports_exist(api, date):
        print(f"reports already exist on master for {date}; syncing site", flush=True)
        _sync_site(repo, date)
        return 0

    force = os.environ.get("HORIZON_GITHUB_FORCE", "true").lower() == "true"
    dispatched_at = datetime.now(timezone.utc)
    api.request(
        "POST",
        "/actions/workflows/daily-summary.yml/dispatches",
        build_dispatch_payload(force=force),
    )
    print(f"dispatched daily workflow for {date}", flush=True)

    poll_seconds = int(os.environ.get("HORIZON_GHA_POLL_SECONDS", "30"))
    timeout_seconds = int(os.environ.get("HORIZON_GHA_TIMEOUT_SECONDS", "7200"))
    deadline = time.monotonic() + timeout_seconds
    run = None
    while time.monotonic() < deadline and run is None:
        _, payload = api.request(
            "GET", "/actions/workflows/daily-summary.yml/runs?event=workflow_dispatch&per_page=20"
        )
        run = select_dispatched_run(payload.get("workflow_runs", []), dispatched_at)
        if run is None:
            time.sleep(min(poll_seconds, 10))
    if run is None:
        raise RuntimeError("dispatched workflow did not appear before timeout")

    run_id = run["id"]
    print(f"tracking workflow run id={run_id}", flush=True)
    last_status = None
    while time.monotonic() < deadline:
        _, run = api.request("GET", f"/actions/runs/{run_id}")
        status = run.get("status")
        if status != last_status:
            print(f"workflow run id={run_id} status={status}", flush=True)
            last_status = status
        if status == "completed":
            conclusion = run.get("conclusion")
            if conclusion != "success":
                raise RuntimeError(
                    f"workflow run id={run_id} completed with {conclusion}"
                )
            _sync_site(repo, date)
            print(f"workflow run id={run_id} published for {date}", flush=True)
            return 0
        time.sleep(poll_seconds)
    raise RuntimeError(f"workflow run id={run_id} exceeded {timeout_seconds}s timeout")


if __name__ == "__main__":
    raise SystemExit(main())
