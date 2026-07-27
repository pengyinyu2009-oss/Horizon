#!/bin/bash
# Horizon 日报同步:GitHub master → 去 Jekyll front matter → 发布到 horizon.pyyaiai.com
LOG=/home/pengyinyu/Horizon-posts/sync.log
echo "===== $(date) sync =====" >> "$LOG"

cd /home/pengyinyu/Horizon-posts && git pull --ff-only >> "$LOG" 2>&1

SRC=/home/pengyinyu/Horizon-posts/docs/_posts
DST=/var/www/horizon-site/reports
mkdir -p "$DST"

for f in "$SRC"/*.md; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  awk 'NR==1 && $0=="---" {infm=1; next} infm==1 && $0=="---" {infm=0; next} infm==0 {print}' "$f" > "$DST/$b"
done

for f in "$DST"/*.md; do
  [ -e "$f" ] || continue
  b=$(basename "$f")
  [ -f "$SRC/$b" ] || rm -f "$f"
done

# 侧边栏:链接到 reports-html/ 下的渲染好的 .html(手机无 JS 也能看,不被 docsify 拦截)
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
} > /var/www/horizon-site/_sidebar.md

echo "done: $(ls "$DST" | wc -l) reports" >> "$LOG"

# 渲染静态 HTML(手机负一屏 webview 免 JS 可读)
python3 /home/pengyinyu/Horizon-posts/render-html.py >> "$LOG" 2>&1

# ===== 兼容链接发布(2026-07-23 新增)=====
# 1) 旧负一屏链接 /YYYY/MM/DD/<sec>-zh.html → reports-html 跳转桩(保留锚点)
ROOT=/var/www/horizon-site
for f in "$ROOT/reports-html"/????-??-??-*-zh.html; do
  [ -e "$f" ] || continue
  b=$(basename "$f" .html)          # 2026-07-22-horizon-zh
  y=${b:0:4}; m=${b:5:2}; d=${b:8:2}; sec=${b:11}
  sec=${sec%-zh}                     # horizon
  date=${b:0:10}
  dir="$ROOT/$y/$m/$d"
  mkdir -p "$dir"
  # 生成绝对地址跳转桩(软链会让 stub 里的相对路径解析到错误位置)
  printf '%s\n' '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">' \
    "<meta http-equiv=\"refresh\" content=\"0; url=/reports-html/$date.html#$sec\">" \
    '<title>跳转中…</title></head>' \
    '<body style="font-family:sans-serif;text-align:center;padding-top:3em">' \
    "<p><a href=\"/reports-html/$date.html#$sec\">点这里立即打开</a></p>" \
    '</body></html>' > "$dir/$sec-zh.html"
done
# 2) 旧 docsify 链接 /_posts/*.md → reports/*.md
mkdir -p "$ROOT/_posts"
for f in "$ROOT/reports"/*.md; do
  [ -e "$f" ] || continue
  ln -sf "$f" "$ROOT/_posts/$(basename "$f")"
done
echo "compat links done" >> "$LOG"
