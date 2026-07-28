#!/usr/bin/env python3
"""把 reports/*.md 渲染成独立静态 HTML(无 JS 依赖,手机任何 webview 都能开)。

页面组织(2026-07-23 起改版,4 榜单一页;2026-07-28 换新四榜):
- 日报:一天一页,新格式 {date}-榜单汇总-zh.md,4 章节吸顶导航
  (全球新闻/Horizon 总榜/GitHub 热榜/电子工程师),每条双评分(客观+画像相关)。
  新格式日期同时输出 {date}.html 别名,供 latest/血缘/推送链路使用。
- 周报/月报/年报:{period}-周榜-zh.md / -月榜-zh.md / -年榜-zh.md,独立页。
- 兼容:旧格式 {date}-{sec}-zh.md 仍支持(2026-07-22 之前),每天 4 文件合并成
  {date}.html,锚点 horizon/ee/embedded/oshw,保证历史链接不 404。
"""
import argparse
import pathlib
import re
import markdown

parser = argparse.ArgumentParser(
    description="Render Horizon Markdown into a complete non-live output directory."
)
parser.add_argument(
    "--src",
    default="/var/www/horizon-site/reports",
    help="Markdown input directory",
)
parser.add_argument(
    "--dst",
    required=True,
    help="Staging output directory; the live reports-html path is rejected",
)
args = parser.parse_args()

SRC = pathlib.Path(args.src)
DST = pathlib.Path(args.dst)
LIVE_DST = pathlib.Path("/var/www/horizon-site/reports-html")
if DST.resolve() == LIVE_DST.resolve():
    parser.error("--dst must be a staging directory, not the live reports-html path")
DST.mkdir(parents=True, exist_ok=True)

# === 新格式(2026-07-23 起,1 文件 4 榜单)===
NEW_DAILY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-榜单汇总-zh$")
NEW_WEEKLY_RE = re.compile(r"^(\d{4})-W(\d{1,2})-周榜-zh$")
NEW_MONTHLY_RE = re.compile(r"^(\d{4})-(\d{2})-月榜-zh$")
NEW_YEARLY_RE = re.compile(r"^(\d{4})-年榜-zh$")

# 2026-07-28 四榜单改版:全球新闻 / Horizon 总榜 / GitHub 热榜(日周月子榜) / 电子工程师。
NAV_ORDER_NEW = ["global", "ai", "github", "ee"]
NAV_LABELS_NEW = {
    "global": "🌍 全球新闻",
    "ai": "🤖 Horizon 总榜",
    "github": "🔥 GitHub 热榜",
    "ee": "🔧 电子工程师",
}

# 旧分版锚点 → 新四榜锚点(新格式日期的跳转桩用)。
OLD_TO_NEW_ANCHOR = {
    "horizon": "sec-ai",
    "ee": "sec-ee",
    "embedded": "sec-ee",
    "oshw": "sec-github",
    "global": "sec-global",
}

# === 旧格式(2026-07-22 之前,1 天 4 文件)===
OLD_DAILY_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-([a-z]+)-zh$")
OLD_WEEKLY_RE = re.compile(r"^(\d{4})-W(\d{1,2})-.*-zh$")

NAV_ORDER_OLD = ["horizon", "ee", "embedded", "oshw"]
NAV_LABELS_OLD = {
    "horizon": "📰 总览",
    "ee": "⚡ 电源/EE",
    "embedded": "🔩 嵌入式",
    "oshw": "🔥 GitHub热榜",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  body {{ font-family: -apple-system, "PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", sans-serif;
         max-width: 760px; margin: 0 auto; padding: 16px; line-height: 1.85; color: #222;
         word-wrap: break-word; font-size: 16px; }}
  h1 {{ font-size: 1.5em; border-bottom: 2px solid #e8e8e8; padding-bottom: .3em; }}
  h2 {{ font-size: 1.2em; margin-top: 1.6em; border-left: 4px solid #4a90d9; padding-left: .5em; }}
  h3 {{ font-size: 1.05em; }}
  a {{ color: #1a6fc4; text-decoration: none; }}
  a:active {{ opacity: .6; }}
  img, video {{ max-width: 100%; height: auto; }}
  code {{ background: #f3f3f3; padding: 2px 5px; border-radius: 4px; font-size: .9em; }}
  pre {{ background: #f6f8fa; padding: 12px; border-radius: 8px; overflow-x: auto; }}
  blockquote {{ margin: 0; padding: 0 1em; color: #666; border-left: 4px solid #dfe2e5; }}
  details {{ background: #fafafa; border-radius: 8px; padding: 8px 12px; margin: 8px 0; }}
  summary {{ font-weight: 600; cursor: pointer; }}
  hr {{ border: none; border-top: 1px solid #e8e8e8; margin: 1.5em 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 1em 0; font-size: .9em; }}
  th, td {{ border: 1px solid #e0e0e0; padding: 6px 8px; text-align: left; }}
  th {{ background: #f5f7fa; font-weight: 600; }}
  .src {{ color: #999; font-size: .8em; text-align: center; margin-top: 2em; }}
  .secnav {{ position: sticky; top: 0; background: #fff; display: flex; gap: 6px;
             padding: 8px 0; border-bottom: 1px solid #eee; margin-bottom: 14px; z-index: 9; }}
  .secnav a {{ flex: 1; text-align: center; padding: 7px 2px; border-radius: 8px;
             font-size: .82em; background: #f3f6fa; color: #1a6fc4; white-space: nowrap; }}
  .daynav {{ display: flex; justify-content: space-between; gap: 8px;
             border-top: 1px solid #eee; margin-top: 2em; padding-top: 12px; font-size: .9em; }}
  .daynav a {{ color: #1a6fc4; }}
  .sec-anchor {{ display: block; position: relative; top: -52px; visibility: hidden; }}
</style>
</head>
<body>
{nav}
{body}
{footer}
<p class="src">Horizon 每日速递 · horizon.pyyaiai.com</p>
</body>
</html>
"""

REDIRECT = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url={target}">
<title>跳转中…</title></head>
<body style="font-family:sans-serif;text-align:center;padding-top:3em">
<p>已合并为每日一页,正在跳转…</p>
<p><a href="{target}">点这里立即打开</a></p>
</body></html>
"""


def render_md(md_file: pathlib.Path) -> str:
    return markdown.markdown(
        md_file.read_text(encoding="utf-8"),
        extensions=["extra", "sane_lists", "smarty", "tables"],
        output_format="html5",
    )


# ---- 归类源文件 ----
new_daily: dict[str, pathlib.Path] = {}  # date -> md (新格式)
old_daily: dict[str, dict[str, pathlib.Path]] = {}  # date -> {sec: md} (旧格式)
period: dict[str, pathlib.Path] = {}     # stem -> md (周报/月报/年报/其他)
period_kind: dict[str, str] = {}         # stem -> kind ("weekly"|"monthly"|"yearly"|"other")

for md_file in sorted(SRC.glob("*.md")):
    stem = md_file.stem
    m = NEW_DAILY_RE.match(stem)
    if m:
        new_daily[m.group(1)] = md_file
        continue
    m = OLD_DAILY_RE.match(stem)
    if m:
        date, sec = m.groups()
        old_daily.setdefault(date, {})[sec] = md_file
        continue
    m = NEW_WEEKLY_RE.match(stem)
    if m:
        period[stem] = md_file
        period_kind[stem] = "weekly"
        continue
    m = NEW_MONTHLY_RE.match(stem)
    if m:
        period[stem] = md_file
        period_kind[stem] = "monthly"
        continue
    m = NEW_YEARLY_RE.match(stem)
    if m:
        period[stem] = md_file
        period_kind[stem] = "yearly"
        continue
    m = OLD_WEEKLY_RE.match(stem)
    if m:
        period[stem] = md_file
        period_kind[stem] = "weekly_old"
        continue
    # 其他(README/index 等)直接渲染
    period[stem] = md_file
    period_kind[stem] = "other"


def period_label(stem: str) -> str:
    kind = period_kind.get(stem, "other")
    m = NEW_WEEKLY_RE.match(stem)
    if m:
        return f"📅 {m.group(1)}-W{int(m.group(2)):02d} 周榜"
    m = NEW_MONTHLY_RE.match(stem)
    if m:
        return f"🗓 {m.group(1)}-{m.group(2)} 月榜"
    m = NEW_YEARLY_RE.match(stem)
    if m:
        return f"📆 {m.group(1)} 年榜"
    m = OLD_WEEKLY_RE.match(stem)
    if m:
        return f"📅 {m.group(1)}-W{int(m.group(2)):02d} 周报"
    return f"📄 {stem}"


# 全量重建输出目录
for old in DST.glob("*.html"):
    old.unlink()

count = 0

# === 新格式日报:一天一页,4 榜单吸顶导航(输出文件名 = md stem,sidebar 链接直接命中) ===
new_dates = sorted(new_daily)
all_old_dates = sorted(old_daily)
all_period_dates = sorted(new_daily) + all_old_dates  # 给 daynav 找"前后一天"用

for i, date in enumerate(new_dates):
    body = render_md(new_daily[date])
    md_stem = new_daily[date].stem  # "2026-07-23-榜单汇总-zh"

    # 4 榜单吸顶导航(锚点 sec-global/ai/embedded/finance)
    nav_items = [f'<a href="#sec-{s}">{NAV_LABELS_NEW[s]}</a>' for s in NAV_ORDER_NEW]
    nav = f'<nav class="secnav">{"".join(nav_items)}</nav>'

    # 底部:同格式前后天(按 stem)+ 周期报
    foot = ['<div class="daynav">']
    prev_stem = new_daily[new_dates[i-1]].stem if i > 0 else None
    next_stem = new_daily[new_dates[i+1]].stem if i < len(new_dates) - 1 else None
    foot.append(
        f'<a href="{prev_stem}.html">← {new_dates[i-1]}</a>' if prev_stem else "<span></span>"
    )
    if period:
        latest_period = sorted(period)[-1]
        foot.append(f'<a href="{latest_period}.html">{period_label(latest_period)}</a>')
    foot.append(
        f'<a href="{next_stem}.html">{new_dates[i+1]} →</a>' if next_stem else "<span></span>"
    )
    foot.append("</div>")

    # 输出文件名 = md stem(保持原名,sidebar 链接直接命中)
    page_html = TEMPLATE.format(
        title=f"{date} 4 榜单速览", nav=nav, body=body, footer="".join(foot)
    )
    (DST / f"{md_stem}.html").write_text(page_html, encoding="utf-8")
    count += 1
    # 2026-07-28:latest 更新、血缘门禁、Hiboard 推送都认 YYYY-MM-DD.html。
    # 新格式日期补一份同内容别名;旧格式循环会跳过这些日期(见下),
    # 不会被 horizon/ee/global 分版文件拼出的旧式页面覆盖。
    (DST / f"{date}.html").write_text(page_html, encoding="utf-8")
    count += 1

# === 旧格式日报:一天一页,4 旧榜单吸顶导航(兼容历史) ===
for date, secs in old_daily.items():
    if date in new_daily:
        # 新格式日期:horizon/ee/global 分版 md 仍在(供 rollup 与血缘门禁
        # 消费),但页面以榜单汇总为准。只生成旧分版链接的跳转桩,
        # 锚点映射到新四榜。
        for s in secs:
            target = OLD_TO_NEW_ANCHOR.get(s, "")
            suffix = f"#{target}" if target else ""
            (DST / f"{date}-{s}-zh.html").write_text(
                REDIRECT.format(target=f"{date}.html{suffix}"), encoding="utf-8"
            )
        continue
    present = [s for s in NAV_ORDER_OLD if s in secs]
    nav = ""
    if len(present) > 1:
        items = [f'<a href="#{s}">{NAV_LABELS_OLD[s]}</a>' for s in present]
        nav = f'<nav class="secnav">{"".join(items)}</nav>'

    parts = []
    for s in present:
        parts.append(f'<span class="sec-anchor" id="{s}"></span>')
        parts.append(render_md(secs[s]))
        if s != present[-1]:
            parts.append("<hr>")
    body = "\n".join(parts)

    # 底部:旧格式前后天(按字母序)
    idx = all_old_dates.index(date)
    foot = ['<div class="daynav">']
    foot.append(
        f'<a href="{all_old_dates[idx-1]}.html">← {all_old_dates[idx-1]}</a>' if idx > 0 else "<span></span>"
    )
    foot.append('<a href="index.html">🏠 导航</a>')
    foot.append(
        f'<a href="{all_old_dates[idx+1]}.html">{all_old_dates[idx+1]} →</a>' if idx < len(all_old_dates) - 1 else "<span></span>"
    )
    foot.append("</div>")

    (DST / f"{date}.html").write_text(
        TEMPLATE.format(title=f"{date} 每日简报", nav=nav, body=body, footer="".join(foot)),
        encoding="utf-8",
    )
    count += 1

    # 旧分版页 → 跳转桩(保证负一屏旧链接不 404)
    for s in present:
        (DST / f"{date}-{s}-zh.html").write_text(
            REDIRECT.format(target=f"{date}.html#{s}"), encoding="utf-8"
        )

# === 周期报:独立页(周报/月报/年报,文件名 = md stem) ===
for stem, md_file in sorted(period.items()):
    kind = period_kind.get(stem, "other")
    body = render_md(md_file)
    # 周报/月报/年报(新格式)加 4 榜单吸顶导航
    nav = ""
    if kind in ("weekly", "monthly", "yearly"):
        nav_items = [f'<a href="#sec-{s}">{NAV_LABELS_NEW[s]}</a>' for s in NAV_ORDER_NEW]
        nav = f'<nav class="secnav">{"".join(nav_items)}</nav>'

    (DST / f"{stem}.html").write_text(
        TEMPLATE.format(title=period_label(stem), nav=nav, body=body, footer=""),
        encoding="utf-8",
    )
    count += 1

print(f"rendered {count} pages (+{sum(len(v) for v in old_daily.values())} redirect stubs)")
