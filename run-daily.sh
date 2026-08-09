#!/bin/bash
# VPS-owned production scheduler. Local mode generates and atomically publishes
# all four boards and is the safe default. GitHub workflow dispatch is a manual
# recovery path only; select it explicitly with HORIZON_EXECUTION_MODE=github
# and provide a token that can dispatch Actions workflows.
set -Eeuo pipefail

REPO=${HORIZON_REPO:-/home/pengyinyu/Horizon}
LOG=${HORIZON_RUN_LOG:-$REPO/data/cron.log}
LOG_MAX_BYTES=${HORIZON_RUN_LOG_MAX_BYTES:-1048576}
PYTHON=${HORIZON_PYTHON:-$REPO/.venv/bin/python}
LOCK=${HORIZON_RUN_LOCK:-/home/pengyinyu/.horizon-run-daily.lock}

mkdir -p "$(dirname "$LOG")"
case "$LOG_MAX_BYTES" in
  ''|*[!0-9]*) LOG_MAX_BYTES=1048576 ;;
esac

trim_run_log() {
  [ -f "$LOG" ] || return 0
  local current_size temporary
  current_size=$(wc -c < "$LOG")
  [ "$current_size" -gt "$LOG_MAX_BYTES" ] || return 0
  temporary=$(mktemp "${LOG}.trim.XXXXXX")
  tail -c "$LOG_MAX_BYTES" "$LOG" > "$temporary"
  mv "$temporary" "$LOG"
}

if ! trim_run_log; then
  echo "[$(date -Is)] warning: could not trim Horizon run log" >&2
fi
exec >> "$LOG" 2>&1

echo "===== $(date -Is) VPS four-board run start ====="
if [ ! -x "$PYTHON" ]; then
  PYTHON=$(command -v python3)
fi

SCRIPT=$REPO/scripts/vps_daily.py
if [ "${HORIZON_EXECUTION_MODE:-local}" = "github" ]; then
  SCRIPT=$REPO/scripts/dispatch_daily_github.py
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
