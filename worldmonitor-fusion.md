---
layout: default
title: worldmonitor 信源融合（数据层）
---

# worldmonitor 信源融合（数据层）

> 2026-07-24 起，Horizon 的 RSS 采集流水线接入了 [koala73/worldmonitor](https://github.com/koala73/worldmonitor) 的全球资讯信源层（A 方案：取数据层，不复制前端）。

## 为什么做这件事

世界资讯（global-news）板块过去只能用通用 RSS（Simon Willison、LWN 等），覆盖偏开发者社区，地缘新闻、央行决议、智库分析、联合国机构等内容缺口大。worldmonitor v2.10.0 维护了一个按 region 分组的全球 RSS 列表，覆盖 8 个地区分组 30+ 信源——这正好补齐我们的全球资讯板块。

A 方案只取数据层（信源 URL + 地区分类），不引入 worldmonitor 的整个前端、Tauri 桌面端或 Convex 数据栈——这与 Horizon 的『小而美、可独立部署』原则保持一致。

## 数据结构

`data/worldmonitor_sources.json` 是信源融合表的真相源（source of truth），结构：

```json
{
  "regions": {
    "americas": { "label": "美洲", "sources": [...] },
    "europe":   { "label": "欧洲", "sources": [...] },
    "middleeast": { "label": "中东", "sources": [...] },
    "asia":     { "label": "亚太", "sources": [...] },
    "latam":    { "label": "拉美", "sources": [...] },
    "africa":   { "label": "非洲", "sources": [...] },
    "thinktanks": { "label": "智库/分析", "sources": [...] },
    "un_orgs":  { "label": "联合国/政府", "sources": [...] }
  }
}
```

每个 source 包含 `name`、`url`、`tier`（1 = 核心，2 = 补充）。`_upstream` 字段记录 worldmonitor 版本，方便后续同步。

## 如何激活

把信源融合表注入 Horizon 的 RSS 采集流水线（`data/config.json`，**注意此文件在 .gitignore 里**，每个 ops 各自维护）：

```python
import json
cfg = json.load(open('data/config.json'))
wm  = json.load(open('data/worldmonitor_sources.json'))
for region in wm['regions'].values():
    for s in region['sources']:
        cfg['sources']['rss'].append({
            'name': s['name'], 'url': s['url'], 'enabled': True,
            'category': 'global-news', 'group': 'global-news',
        })
json.dump(cfg, open('data/config.json','w'), ensure_ascii=False, indent=2)
```

激活后，所有 35 条信源会被 `RSSScraper` 拉取，metadata.group 字段被透传到 item，落地到 `global-news` 板块。

## 降级渲染

`RSSScraper` 在网络失败 / 抓取超时时静默丢弃当批 item，不阻塞整次 run。reports-html 渲染器在 `board.sources_unavailable=true` 时会插入降级 banner：

```
⚠ 今日信源不可用（抓取失败/超时），板块已降级渲染。
```

这保证日报不会因为上游故障而缺席。

## 与 worldmonitor 上游同步

worldmonitor 上游活跃，建议每月人工同步一次 `src/config/feeds.ts` 的 RSS 列表到 `data/worldmonitor_sources.json`。同步操作脚本（建议但本仓尚未固化）：

```bash
# 1. 浅克隆 worldmonitor 到 /tmp
git clone --depth 1 https://github.com/koala73/worldmonitor.git /tmp/worldmonitor

# 2. 用 jq / Python 抽取 FULL_FEEDS 与 CANONICAL_FEEDS
# 3. 重新跑上面的"如何激活"步骤把新的 sources 灌入 data/config.json
```

## 信源清单

总计 **35 个 RSS 信源，跨 8 个地区分组**：

| 地区 | 信源数 | 核心示例 |
|---|---|---|
| 美洲 | 6 | Reuters US, NPR News, AP News, WSJ |
| 欧洲 | 7 | BBC World, Guardian, France 24, DW News, Le Monde |
| 中东 | 5 | Al Jazeera, BBC Middle East, Iran International |
| 亚太 | 6 | BBC Asia, SCMP, Nikkei Asia, The Diplomat |
| 拉美 | 2 | BBC Latin America, Reuters LatAm |
| 非洲 | 2 | BBC Africa, Africa News |
| 智库/分析 | 4 | Foreign Policy, Atlantic Council, Crisis Group, Brookings |
| 联合国/政府 | 3 | UN News, WHO, IAEA |

## 与 Horizon 主结构的衔接

| 字段 | worldmonitor 上游 | Horizon 落地 |
|---|---|---|
| `name` | feed 名字 | RSSSourceConfig.name |
| `url` | feed URL（经 rssProxyUrl 包裹） | RSSSourceConfig.url |
| 地区分组 | `region` 字段 | RSSSourceConfig.group = "global-news" |
| `tier` | 1 = 核心、2 = 补充 | 暂未在 RSSSourceConfig 暴露，未来用于打分加权 |
| `lang` | feed 语言 | RSSSourceConfig 没有语言字段，保留多语言原生支持 |

## 验证样张

`reports-html/2026-07-24.html` 是按新结构（5 大榜单 × 13 条 × 4 字段）生成的验收样张。生成命令：

```bash
.venv/bin/python scripts/build_reports_html.py
```

详见 `scripts/build_reports_html.py` 与 `reports-html/data/2026-07-24.json`。