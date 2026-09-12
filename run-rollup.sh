#!/bin/bash
# VPS-owned production scheduler for the weekly / monthly / yearly rollups.
# Complements run-daily.sh (daily four-board pipeline).
#
# The hard prerequisite gate stays ON for scheduled runs: never set
# HORIZON_ROLLUP_ALLOW_PARTIAL here — it is a manual backfill-only escape
# hatch for windows whose upstream reports can no longer be complete
# (e.g. the 2026-08-03..08-08 daily gap).
#
# Period targets (all "most recently completed", matching the original
# GitHub Actions schedule that was disabled on 2026-08-08):
#   weekly  — Monday after the daily pipeline has settled
#   monthly — 8th, after the touching weeks' weeklies exist
#   yearly  — 15 Jul (H1) and 15 Jan (H2)
set -Eeuo pipefail

MODE=${1:?usage: run-rollup.sh weekly|monthly|yearly [extra src.main args]}
case "$MODE" in
  weekly|monthly|yearly) ;;
  *) echo "unknown rollup mode: $MODE" >&2; exit 2 ;;
esac
# Extra args (e.g. --period-id 2026-W32) are forwarded to ``python -m src.main``.

REPO=${HORIZON_REPO:-/home/pengyinyu/Horizon}
LOG=${HORIZON_ROLLUP_LOG:-$REPO/data/cron-rollup-$MODE.log}
LOG_MAX_BYTES=${HORIZON_ROLLUP_LOG_MAX_BYTES:-1048576}
PYTHON=${HORIZON_PYTHON:-$REPO/.venv/bin/python}
LOCK=${HORIZON_ROLLUP_LOCK:-/home/pengyinyu/.horizon-run-rollup-$MODE.lock}

mkdir -p "$(dirname "$LOG")" "$(dirname "$LOCK")"
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
  echo "[$(date -Is)] warning: could not trim Horizon rollup log" >&2
fi
exec >> "$LOG" 2>&1

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date -Is)] run skipped: lock busy ($LOCK)"
  exit 75
fi

cd "$REPO"
echo "===== $(date -Is) rollup $MODE start ====="
if [ ! -x "$PYTHON" ]; then
  PYTHON=$(command -v python3)
fi

set +e
"$PYTHON" -m src.main "$MODE" "${@:2}"
rc=$?
set -e

if [ "$rc" -eq 0 ]; then
  echo "===== $(date -Is) rollup $MODE done ====="
else
  echo "===== $(date -Is) rollup $MODE failed exit=$rc ====="
fi
exit "$rc"
