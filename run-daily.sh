#!/bin/bash
# VPS-owned scheduler. GitHub Actions generates with repository Secrets, then
# the VPS pulls and atomically publishes. Set HORIZON_EXECUTION_MODE=local to
# use scripts/vps_daily.py after installing a valid VPS model credential.
set -Eeuo pipefail

REPO=${HORIZON_REPO:-/home/pengyinyu/Horizon}
LOG=${HORIZON_RUN_LOG:-$REPO/data/cron.log}
PYTHON=${HORIZON_PYTHON:-$REPO/.venv/bin/python}
LOCK=${HORIZON_RUN_LOCK:-/home/pengyinyu/.horizon-run-daily.lock}

mkdir -p "$(dirname "$LOG")"
exec >> "$LOG" 2>&1

echo "===== $(date -Is) VPS four-board run start ====="
if [ ! -x "$PYTHON" ]; then
  PYTHON=$(command -v python3)
fi

SCRIPT=$REPO/scripts/dispatch_daily_github.py
if [ "${HORIZON_EXECUTION_MODE:-github}" = "local" ]; then
  SCRIPT=$REPO/scripts/vps_daily.py
else
  exec 9>"$LOCK"
  if ! flock -n 9; then
    echo "[$(date -Is)] run skipped: lock busy ($LOCK)"
    exit 75
  fi
fi

set +e
"$PYTHON" "$SCRIPT"
rc=$?
set -e

if [ "$rc" -eq 0 ]; then
  echo "===== $(date -Is) VPS four-board run done ====="
else
  echo "===== $(date -Is) VPS four-board run failed exit=$rc ====="
fi
exit "$rc"
