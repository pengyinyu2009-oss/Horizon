#!/bin/bash
# Horizon 本地每日跑批。正常 Hiboard 推送由 GitHub Actions 在发布验证后负责。
set -Eeuo pipefail
LOG=/home/pengyinyu/Horizon/data/cron.log
LOCK=/home/pengyinyu/Horizon/.run-daily.lock

exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date)] run skipped: lock busy ($LOCK)" >> "$LOG"
  exit 75
fi

cd /home/pengyinyu/Horizon
echo "===== $(date) run start =====" >> "$LOG"

# 生成日报（48h 窗口）。评分故障会在落盘故障空报后返回非零。
if docker compose run --rm horizon --hours 48 >> "$LOG" 2>&1; then
  echo "[$(date)] docker ok" >> "$LOG"
else
  rc=$?
  echo "[$(date)] docker FAILED exit=$rc" >> "$LOG"
  echo "===== $(date) run failed =====" >> "$LOG"
  exit "$rc"
fi

echo "===== $(date) run done =====" >> "$LOG"
