#!/bin/bash
# Horizon 每日跑批 + 负一屏推送
set -u
cd /home/pengyinyu/Horizon

LOG=/home/pengyinyu/Horizon/data/cron.log
echo "===== $(date) run start =====" >> "$LOG"

# 1) 生成日报（48h 窗口）
if docker compose run --rm horizon --hours 48 >> "$LOG" 2>&1; then
  echo "[$(date)] docker ok" >> "$LOG"
else
  echo "[$(date)] docker FAILED exit=$?" >> "$LOG"
fi

# 2) 负一屏推送（失败不影响本地生成）
TODAY=$(date +%F)
if [ -x /home/pengyinyu/Horizon/.venv/bin/python ]; then
  if /home/pengyinyu/Horizon/.venv/bin/python /home/pengyinyu/Horizon/scripts/push_hiboard_daily.py --date "$TODAY" >>"$LOG" 2>&1; then
    echo "[$(date)] hiboard push ok ($TODAY)" >> "$LOG"
  else
    echo "[$(date)] hiboard push FAILED ($TODAY) exit=$?" >> "$LOG"
  fi
else
  echo "[$(date)] hiboard push skipped: .venv missing" >> "$LOG"
fi

echo "===== $(date) run done =====" >> "$LOG"
