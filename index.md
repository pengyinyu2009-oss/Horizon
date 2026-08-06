---
layout: default
title: Home
---

# Horizon

<div id="lang-zh" class="lang-section" markdown="1">

欢迎来到 [Horizon](https://github.com/thysrael/Horizon)，一个 AI 驱动的信息聚合系统。

## 文档

- [配置指南](configuration) — AI 提供商、信息源、过滤规则与环境变量替换
- [GitHub 热榜](github-trending) — 每天 / 每周 / 每月 GitHub 热门仓库榜单
- [信息源采集器](scrapers) — Horizon 如何从 GitHub、Hacker News、RSS、Reddit 采集内容
- [评分系统](scoring) — 基于 AI 的内容分析与 0-10 评分体系

{% assign this_month_zh = site.time | date: "%Y-%m" %}
{% assign two_months_ago_zh = site.time | minus: 5184000 %}
{% assign two_years_ago_zh = site.time | minus: 63072000 %}

## 每日速递 <a class="rss-icon" href="{{ '/feed-zh.xml' | relative_url }}" aria-label="订阅中文"><svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"></path></svg></a>

{% assign daily_zh_total = 0 %}
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "daily" and post.date | date: '%Y-%m' == this_month_zh %}
    {% assign daily_zh_total = daily_zh_total | plus: 1 %}
  {% endif %}
{% endfor %}

{% if daily_zh_total == 0 %}
*本月暂无速递*
{% else %}
{% assign daily_zh_shown = 0 %}
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "daily" and post.date | date: '%Y-%m' == this_month_zh and daily_zh_shown < 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a></li>
    {% assign daily_zh_shown = daily_zh_shown | plus: 1 %}
  {% endif %}
{% endfor %}
</ul>
{% if daily_zh_total > 5 %}
<details>
<summary>展开剩余 {{ daily_zh_total | minus: 5 }} 个</summary>
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "daily" and post.date | date: '%Y-%m' == this_month_zh and daily_zh_shown >= 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a></li>
  {% endif %}
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 上周总览

{% assign weekly_zh_total = 0 %}
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "weekly" and post.date >= two_months_ago_zh %}
    {% assign weekly_zh_total = weekly_zh_total | plus: 1 %}
  {% endif %}
{% endfor %}

{% if weekly_zh_total == 0 %}
*近两个月暂无周报*
{% else %}
{% assign weekly_zh_shown = 0 %}
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "weekly" and post.date >= two_months_ago_zh and weekly_zh_shown < 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a></li>
    {% assign weekly_zh_shown = weekly_zh_shown | plus: 1 %}
  {% endif %}
{% endfor %}
</ul>
{% if weekly_zh_total > 5 %}
<details>
<summary>展开剩余 {{ weekly_zh_total | minus: 5 }} 个</summary>
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "weekly" and post.date >= two_months_ago_zh and weekly_zh_shown >= 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a></li>
  {% endif %}
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 上月总览

{% assign monthly_zh_total = 0 %}
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "monthly" and post.date >= two_years_ago_zh %}
    {% assign monthly_zh_total = monthly_zh_total | plus: 1 %}
  {% endif %}
{% endfor %}

{% if monthly_zh_total == 0 %}
*近两年暂无月报*
{% else %}
{% assign monthly_zh_shown = 0 %}
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "monthly" and post.date >= two_years_ago_zh and monthly_zh_shown < 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a></li>
    {% assign monthly_zh_shown = monthly_zh_shown | plus: 1 %}
  {% endif %}
{% endfor %}
</ul>
{% if monthly_zh_total > 5 %}
<details>
<summary>展开剩余 {{ monthly_zh_total | minus: 5 }} 个</summary>
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "monthly" and post.date >= two_years_ago_zh and monthly_zh_shown >= 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m" }}</a></li>
  {% endif %}
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

## 本年总览

{% assign yearly_zh_total = 0 %}
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "yearly" %}
    {% assign yearly_zh_total = yearly_zh_total | plus: 1 %}
  {% endif %}
{% endfor %}

{% if yearly_zh_total == 0 %}
*暂无年报*
{% else %}
{% assign yearly_zh_shown = 0 %}
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "yearly" and yearly_zh_shown < 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a></li>
    {% assign yearly_zh_shown = yearly_zh_shown | plus: 1 %}
  {% endif %}
{% endfor %}
</ul>
{% if yearly_zh_total > 5 %}
<details>
<summary>展开剩余 {{ yearly_zh_total | minus: 5 }} 个</summary>
<ul>
{% for post in site.posts %}
  {% if post.lang == "zh" and post.period == "yearly" and yearly_zh_shown >= 5 %}
    <li><a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y" }}</a></li>
  {% endif %}
{% endfor %}
</ul>
</details>
{% endif %}
{% endif %}

</div>
