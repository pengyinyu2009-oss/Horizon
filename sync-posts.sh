#!/bin/bash
# Horizon 日报发布：GitHub master → staging 渲染/校验 → 原子切换 → 血缘门禁 → latest
set -Eeuo pipefail

REPO_DIR=${HORIZON_POSTS_REPO:-/home/pengyinyu/Horizon-posts}
HORIZON_REPO=${HORIZON_REPO:-/home/pengyinyu/Horizon}
ROOT=${HORIZON_SITE_ROOT:-/var/www/horizon-site}
STAGING_ROOT=${HORIZON_STAGING_ROOT:-/home/pengyinyu/.horizon-publish-staging}
LOG=${HORIZON_SYNC_LOG:-/home/pengyinyu/Horizon-posts/sync.log}
LOCK=${HORIZON_SYNC_LOCK:-/home/pengyinyu/Horizon-posts/.sync-posts.lock}
TODAY=${HORIZON_DATE:-$(TZ=Asia/Shanghai date +%F)}
MIN_HTML_PAGES=${HORIZON_MIN_HTML_PAGES:-20}
SRC="$REPO_DIR/docs/_posts"
DST="$ROOT/reports"
LIVE_HTML="$ROOT/reports-html"
STAGING_DIR=""
LINEAGE_OK=1
LINEAGE_REASON=""

cleanup_staging() {
  if [ -n "$STAGING_DIR" ]; then
    case "$STAGING_DIR" in
      "$STAGING_ROOT"/reports-html.*)
        rm -rf -- "$STAGING_DIR"
        ;;
      *)
        echo "cleanup refused unexpected staging path: $STAGING_DIR" >> "$LOG"
        ;;
    esac
  fi
}

on_error() {
  rc=$?
  echo "FAILED: $(date -Is) line=$1 exit=$rc" >> "$LOG"
  exit "$rc"
}

send_publish_alert() {
  message=$1
  result=$2
  if [ "${HORIZON_DISABLE_ALERTS:-0}" = "1" ]; then
    echo "alert disabled for dry-run: result=$result message=$message" >> "$LOG"
    return 0
  fi
  python_bin="$HORIZON_REPO/.venv/bin/python"
  push_script="$HORIZON_REPO/scripts/push_hiboard_daily.py"
  if [ ! -x "$python_bin" ] || [ ! -f "$push_script" ]; then
    echo "ALERT FAILED: Hiboard adapter unavailable: $python_bin $push_script" >> "$LOG"
    return 1
  fi
  if "$python_bin" "$push_script" \
      --date "$TODAY" \
      --alert-content "$message" \
      --alert-result "$result" >> "$LOG" 2>&1; then
    echo "alert sent: $result" >> "$LOG"
  else
    rc=$?
    echo "ALERT FAILED: Hiboard push exit=$rc result=$result" >> "$LOG"
    return "$rc"
  fi
}

trap cleanup_staging EXIT
trap 'on_error "$LINENO"' ERR

mkdir -p "$(dirname "$LOG")" "$(dirname "$LOCK")"
exec 9>"$LOCK"
if ! flock -n 9; then
  echo "[$(date -Is)] sync skipped: lock busy ($LOCK)" >> "$LOG"
  exit 75
fi

echo "===== $(date) sync date=$TODAY =====" >> "$LOG"
cd "$REPO_DIR"
if [ "${HORIZON_SKIP_GIT_PULL:-0}" != "1" ]; then
  git pull --ff-only origin master >> "$LOG" 2>&1
fi

mkdir -p "$DST" "$LIVE_HTML" "$STAGING_ROOT"

# 同步 Markdown 真相源，保留 fail-fast 与旧输入清理。
for f in "$SRC"/*.md; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  awk 'NR==1 && $0=="---" {infm=1; next} infm==1 && $0=="---" {infm=0; next} infm==0 {print}' "$f" > "$DST/$b"
done
for f in "$DST"/*.md; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  [ -f "$SRC/$b" ] || rm -f -- "$f"
done

# 侧边栏先写临时文件，再原子替换。
sidebar_tmp="$ROOT/.sidebar.tmp.$$"
{
  echo "* [🏠 首页](reports-html/index.html)"
  echo "* [📑 5 榜单导航](reports-html/index.html)"
  echo ""
  echo "**📅 日报 / 周报(新→旧)**"
  echo ""
  find "$DST" -maxdepth 1 -name '*.md' -printf '%f\n' | sort -r | while read -r f; do
    b="${f%.md}"
    echo "* [$b](reports-html/$b.html)"
  done
} > "$sidebar_tmp"
mv -f -- "$sidebar_tmp" "$ROOT/_sidebar.md"

# renderer 永远只写 web root 外的 staging。
STAGING_DIR=$(mktemp -d "$STAGING_ROOT/reports-html.${TODAY}.XXXXXX")
if [ -d "$LIVE_HTML/data" ]; then
  cp -a "$LIVE_HTML/data" "$STAGING_DIR/data"
fi
python3 "$REPO_DIR/render-html.py" \
  --src "$DST" \
  --dst "$STAGING_DIR" >> "$LOG" 2>&1
# mktemp creates the staging root as 0700. The directory becomes nginx's
# live reports-html after exchange, so make every directory traversable and
# every artifact readable before it can enter the web root.
chmod -R a+rX "$STAGING_DIR"

# 在切换前保留旧 latest 目标。血缘失败时它继续指向旧业务日期。
previous_latest=""
if [ -L "$LIVE_HTML/latest.html" ]; then
  previous_latest=$(basename "$(readlink "$LIVE_HTML/latest.html")")
elif [ -f "$LIVE_HTML/latest.html" ]; then
  previous_latest=$(
    find "$LIVE_HTML" -maxdepth 1 -type f -name '????-??-??.html' -printf '%f\n' \
      | LC_ALL=C sort \
      | tail -n 1
  )
fi
if [[ "$previous_latest" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.html$ ]] \
    && [ -f "$STAGING_DIR/$previous_latest" ]; then
  ln -s "$previous_latest" "$STAGING_DIR/latest.html"
fi

# staging 验收：页数阈值、当日页、日期正文、非 Docsify 壳、主日报输入。
page_count=$(find "$STAGING_DIR" -maxdepth 1 -type f -name '*.html' | wc -l | tr -d ' ')
if [ "$page_count" -lt "$MIN_HTML_PAGES" ]; then
  echo "FAILED: staging page count $page_count < $MIN_HTML_PAGES" >> "$LOG"
  exit 1
fi
if [ ! -f "$SRC/${TODAY}-horizon-zh.md" ]; then
  echo "FAILED: published source missing: $SRC/${TODAY}-horizon-zh.md" >> "$LOG"
  exit 1
fi
if [ ! -f "$STAGING_DIR/${TODAY}.html" ]; then
  echo "FAILED: staging dated page missing: ${TODAY}.html" >> "$LOG"
  exit 1
fi
if ! grep -Fq "$TODAY" "$STAGING_DIR/${TODAY}.html"; then
  echo "FAILED: staging dated page does not contain $TODAY" >> "$LOG"
  exit 1
fi
if grep -Fq '<div id="app">加载中' "$STAGING_DIR/${TODAY}.html"; then
  echo "FAILED: staging dated page is Docsify shell" >> "$LOG"
  exit 1
fi
echo "staging verified: pages=$page_count dated=${TODAY}.html" >> "$LOG"

# 同文件系统目录原子交换。交换后新日期页立即可见，旧站暂存于 STAGING_DIR。
python3 "$REPO_DIR/atomic-swap.py" "$LIVE_HTML" "$STAGING_DIR"
echo "atomic publish complete: dated=${TODAY}.html" >> "$LOG"

# 血缘检查在页面可见之后、latest 更新之前执行。
mkdir -p "$LIVE_HTML/data"
report_json="$LIVE_HTML/data/${TODAY}.json"
lineage_json="$LIVE_HTML/data/${TODAY}-lineage.json"
horizon_python="$HORIZON_REPO/.venv/bin/python"
if [ ! -x "$horizon_python" ]; then
  LINEAGE_OK=0
  LINEAGE_REASON="Horizon Python 环境不可用"
elif ! "$horizon_python" "$HORIZON_REPO/scripts/build_report_json.py" \
    --date "$TODAY" \
    --hours 48 \
    --summary "$SRC/${TODAY}-horizon-zh.md" \
    --out "$report_json" >> "$LOG" 2>&1; then
  LINEAGE_OK=0
  LINEAGE_REASON="日报血缘 JSON 构建失败"
elif ! "$horizon_python" "$HORIZON_REPO/scripts/check_lineage.py" \
    --date "$TODAY" \
    --hours 48 \
    --report "$report_json" \
    --summaries-dir "$SRC" \
    --json-out "$lineage_json" >> "$LOG" 2>&1; then
  LINEAGE_OK=0
  LINEAGE_REASON="血缘自检未达 100%"
fi

if [ "$LINEAGE_OK" -eq 1 ]; then
  latest_tmp="$LIVE_HTML/.latest.html.$$"
  ln -s "${TODAY}.html" "$latest_tmp"
  mv -Tf -- "$latest_tmp" "$LIVE_HTML/latest.html"
  latest_html="${TODAY}.html"
  echo "lineage passed; latest updated: $latest_html" >> "$LOG"
else
  latest_html=${previous_latest:-unchanged}
  echo "LINEAGE FAILED: $LINEAGE_REASON; latest retained: $latest_html" >> "$LOG"
  send_publish_alert \
    "$LINEAGE_REASON；当日页面已发布，但 latest 保留旧页面。" \
    "生成失败：血缘自检异常" || true
fi

# ===== 兼容链接发布 =====
for f in "$LIVE_HTML"/????-??-??-*-zh.html; do
  [ -e "$f" ] || continue
  b=$(basename "$f" .html)
  y=${b:0:4}; m=${b:5:2}; d=${b:8:2}; sec=${b:11}
  sec=${sec%-zh}
  date=${b:0:10}
  dir="$ROOT/$y/$m/$d"
  mkdir -p "$dir"
  printf '%s\n' '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">' \
    "<meta http-equiv=\"refresh\" content=\"0; url=/reports-html/$date.html#$sec\">" \
    '<title>跳转中…</title></head>' \
    '<body style="font-family:sans-serif;text-align:center;padding-top:3em">' \
    "<p><a href=\"/reports-html/$date.html#$sec\">点这里立即打开</a></p>" \
    '</body></html>' > "$dir/$sec-zh.html"
done

# 保留 dangling 清理逻辑，再重建 docsify 兼容链接。
mkdir -p "$ROOT/_posts"
find "$ROOT/_posts" -maxdepth 1 -xtype l -delete
for f in "$ROOT/reports"/*.md; do
  [ -e "$f" ] || continue
  ln -sf "$f" "$ROOT/_posts/$(basename "$f")"
done

report_count=$(find "$DST" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')
deploy_sha=$(git rev-parse HEAD)
echo "done: $report_count reports" >> "$LOG"
echo "compat links done" >> "$LOG"
echo "deployed: sha=$deploy_sha dated=${TODAY}.html latest=$latest_html lineage=$LINEAGE_OK at=$(date -Is)" >> "$LOG"

if [ "$LINEAGE_OK" -ne 1 ]; then
  exit 1
fi
