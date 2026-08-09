#!/bin/bash
# VPS-owned daily pipeline: generate four boards, validate, then publish.
set -Eeuo pipefail

REPO=${HORIZON_REPO:-/home/pengyinyu/Horizon}
LOG=${HORIZON_RUN_LOG:-$REPO/data/cron.log}
PYTHON=${HORIZON_PYTHON:-$REPO/.venv/bin/python}

mkdir -p "$(dirname "$LOG")"
exec >> "$LOG" 2>&1

echo "===== $(date -Is) VPS four-board run start ====="
if [ ! -x "$PYTHON" ]; then
  PYTHON=$(command -v python3)
fi

set +e
"$PYTHON" "$REPO/scripts/vps_daily.py"
rc=$?
set -e

if [ "$rc" -eq 0 ]; then
  echo "===== $(date -Is) VPS four-board run done ====="
else
  echo "===== $(date -Is) VPS four-board run failed exit=$rc ====="
fi
exit "$rc"
