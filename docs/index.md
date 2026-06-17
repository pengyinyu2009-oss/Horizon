---
layout: default
title: Home
---

# Horizon

<div id="lang-zh" class="lang-section" markdown="1">

欢迎来到 [Horizon](https://github.com/thysrael/Horizon)，一个 AI 驱动的信息聚合系统。

## 文档

- [配置指南](configuration) — AI 提供商、信息源、过滤规则与环境变量替换
- [信息源采集器](scrapers) — Horizon 如何从 GitHub、Hacker News、RSS、Reddit 采集内容
- [评分系统](scoring) — 基于 AI 的内容分析与 0-10 评分体系

{% assign now_zh = site.time %}
{% assign this_month_zh = now_zh | date: "%Y-%m" %}
{% assign two_months_ago_zh = now_zh | date: "%s" | minus: 5184000 | date: "%Y-%m-%d" %}
{% assign two_years_ago_zh = now_zh | date: "%s" | minus: 63072000 | date: "%Y-%m-%d" %}

## 每日速递 <a class="rss-icon" href="{{ '/feed-zh.xml' | relative_url }}" aria-label="订阅中文"><svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"></path></svg></a>

{% assign daily_zh = site.posts | where: "lang", "zh" | where: "period", "daily" | where_exp: "post", "post.date | slice: 0, 7 == this_month_zh" | sort: "date" | reverse %}
{% assign daily_zh_count = daily_zh | size %}
{% if daily_zh_count == 0 %}
*本月暂无速递*
{% else %}
<ul>
{% for post in daily_zh limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
{% if daily_zh_count > 5 %}
<details>
<summary>展开剩余 {{ daily_zh_count | minus: 5 }} 个</summary>
<ul>
{% for post in daily_zh offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 上周总览

{% assign weekly_zh = site.posts | where: "lang", "zh" | where: "period", "weekly" | where_exp: "post", "post.date >= two_months_ago_zh" | sort: "date" | reverse %}
{% assign weekly_zh_count = weekly_zh | size %}
{% if weekly_zh_count == 0 %}
*近两个月暂无周报*
{% else %}
<ul>
{% for post in weekly_zh limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
{% if weekly_zh_count > 5 %}
<details>
<summary>展开剩余 {{ weekly_zh_count | minus: 5 }} 个</summary>
<ul>
{% for post in weekly_zh offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 上月总览

{% assign monthly_zh = site.posts | where: "lang", "zh" | where: "period", "monthly" | where_exp: "post", "post.date >= two_years_ago_zh" | sort: "date" | reverse %}
{% assign monthly_zh_count = monthly_zh | size %}
{% if monthly_zh_count == 0 %}
*近两年暂无月报*
{% else %}
<ul>
{% for post in monthly_zh limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a>
  </li>
{% endfor %}
</ul>
{% if monthly_zh_count > 5 %}
<details>
<summary>展开剩余 {{ monthly_zh_count | minus: 5 }} 个</summary>
<ul>
{% for post in monthly_zh offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 本年总览

{% assign yearly_zh = site.posts | where: "lang", "zh" | where: "period", "yearly" | sort: "date" | reverse %}
{% assign yearly_zh_count = yearly_zh | size %}
{% if yearly_zh_count == 0 %}
*暂无年报*
{% else %}
<ul>
{% for post in yearly_zh limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a>
  </li>
{% endfor %}
</ul>
{% if yearly_zh_count > 5 %}
<details>
<summary>展开剩余 {{ yearly_zh_count | minus: 5 }} 个</summary>
<ul>
{% for post in yearly_zh offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

</div>

<div id="lang-en" class="lang-section" markdown="1">

Welcome to [Horizon](https://github.com/thysrael/Horizon), an AI-driven information aggregation system.

## Documentation

- [Configuration Guide](configuration) — AI providers, information sources, filtering, and environment variable substitution
- [Source Scrapers](scrapers) — How Horizon collects content from GitHub, Hacker News, RSS, and Reddit
- [Scoring System](scoring) — AI-based content analysis and the 0-10 scoring scale

{% assign now_en = site.time %}
{% assign this_month_en = now_en | date: "%Y-%m" %}
{% assign two_months_ago_en = now_en | date: "%s" | minus: 5184000 | date: "%Y-%m-%d" %}
{% assign two_years_ago_en = now_en | date: "%s" | minus: 63072000 | date: "%Y-%m-%d" %}

## Daily Digest <a class="rss-icon" href="{{ '/feed-en.xml' | relative_url }}" aria-label="Subscribe English"><svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"></path></svg></a>

{% assign daily_en = site.posts | where: "lang", "en" | where: "period", "daily" | where_exp: "post", "post.date | slice: 0, 7 == this_month_en" | sort: "date" | reverse %}
{% assign daily_en_count = daily_en | size %}
{% if daily_en_count == 0 %}
*No digests this month*
{% else %}
<ul>
{% for post in daily_en limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
{% if daily_en_count > 5 %}
<details>
<summary>Show {{ daily_en_count | minus: 5 }} more</summary>
<ul>
{% for post in daily_en offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## Weekly Digest

{% assign weekly_en = site.posts | where: "lang", "en" | where: "period", "weekly" | where_exp: "post", "post.date >= two_months_ago_en" | sort: "date" | reverse %}
{% assign weekly_en_count = weekly_en | size %}
{% if weekly_en_count == 0 %}
*No weekly digests in the past 2 months*
{% else %}
<ul>
{% for post in weekly_en limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
{% if weekly_en_count > 5 %}
<details>
<summary>Show {{ weekly_en_count | minus: 5 }} more</summary>
<ul>
{% for post in weekly_en offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## Monthly Digest

{% assign monthly_en = site.posts | where: "lang", "en" | where: "period", "monthly" | where_exp: "post", "post.date >= two_years_ago_en" | sort: "date" | reverse %}
{% assign monthly_en_count = monthly_en | size %}
{% if monthly_en_count == 0 %}
*No monthly digests in the past 2 years*
{% else %}
<ul>
{% for post in monthly_en limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a>
  </li>
{% endfor %}
</ul>
{% if monthly_en_count > 5 %}
<details>
<summary>Show {{ monthly_en_count | minus: 5 }} more</summary>
<ul>
{% for post in monthly_en offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## Yearly Digest

{% assign yearly_en = site.posts | where: "lang", "en" | where: "period", "yearly" | sort: "date" | reverse %}
{% assign yearly_en_count = yearly_en | size %}
{% if yearly_en_count == 0 %}
*No yearly digests yet*
{% else %}
<ul>
{% for post in yearly_en limit:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a>
  </li>
{% endfor %}
</ul>
{% if yearly_en_count > 5 %}
<details>
<summary>Show {{ yearly_en_count | minus: 5 }} more</summary>
<ul>
{% for post in yearly_en offset:5 %}
  <li>
    <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a>
  </li>
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

</div>
