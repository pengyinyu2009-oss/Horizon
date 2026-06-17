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

## 每日速递 <a class="rss-icon" href="{{ '/feed-zh.xml' | relative_url }}" aria-label="订阅中文"><svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"></path></svg></a>

<ul>
  {% assign daily_zh = site.posts | where: "lang", "zh" | where: "period", "daily" %}
  {% for post in daily_zh limit:30 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
    </li>
  {% else %}
    <li><em>暂无内容</em></li>
  {% endfor %}
</ul>

## 上周总览

<ul>
  {% assign weekly_zh = site.posts | where: "lang", "zh" | where: "period", "weekly" %}
  {% for post in weekly_zh limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>暂无内容</em></li>
  {% endfor %}
</ul>

## 上月总览

<ul>
  {% assign monthly_zh = site.posts | where: "lang", "zh" | where: "period", "monthly" %}
  {% for post in monthly_zh limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>暂无内容</em></li>
  {% endfor %}
</ul>

## 本年总览

<ul>
  {% assign yearly_zh = site.posts | where: "lang", "zh" | where: "period", "yearly" %}
  {% for post in yearly_zh limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>暂无内容</em></li>
  {% endfor %}
</ul>

</div>

<div id="lang-en" class="lang-section" markdown="1">

Welcome to [Horizon](https://github.com/thysrael/Horizon), an AI-driven information aggregation system.

## Documentation

- [Configuration Guide](configuration) — AI providers, information sources, filtering, and environment variable substitution
- [Source Scrapers](scrapers) — How Horizon collects content from GitHub, Hacker News, RSS, and Reddit
- [Scoring System](scoring) — AI-based content analysis and the 0-10 scoring scale

## Daily Digest <a class="rss-icon" href="{{ '/feed-en.xml' | relative_url }}" aria-label="Subscribe English"><svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M128.081 415.959c0 35.369-28.672 64.041-64.041 64.041S0 451.328 0 415.959s28.672-64.041 64.041-64.041 64.04 28.673 64.04 64.041zm175.66 47.25c-8.354-154.6-132.185-278.587-286.95-286.95C7.656 175.765 0 183.105 0 192.253v48.069c0 8.415 6.49 15.472 14.887 16.018 111.832 7.284 201.473 96.702 208.772 208.772.547 8.397 7.604 14.887 16.018 14.887h48.069c9.149.001 16.489-7.655 15.995-16.79zm144.249.288C439.596 229.677 251.465 40.445 16.503 32.01 7.473 31.686 0 38.981 0 48.016v48.068c0 8.625 6.835 15.645 15.453 15.999 191.179 7.839 344.627 161.316 352.465 352.465.353 8.618 7.373 15.453 15.999 15.453h48.068c9.034-.001 16.329-7.474 16.005-16.504z"></path></svg></a>

<ul>
  {% assign daily_en = site.posts | where: "lang", "en" | where: "period", "daily" %}
  {% for post in daily_en limit:30 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date | date: "%Y-%m-%d" }}</a>
    </li>
  {% else %}
    <li><em>No posts yet</em></li>
  {% endfor %}
</ul>

## Weekly Digest

<ul>
  {% assign weekly_en = site.posts | where: "lang", "en" | where: "period", "weekly" %}
  {% for post in weekly_en limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>No posts yet</em></li>
  {% endfor %}
</ul>

## Monthly Digest

<ul>
  {% assign monthly_en = site.posts | where: "lang", "en" | where: "period", "monthly" %}
  {% for post in monthly_en limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>No posts yet</em></li>
  {% endfor %}
</ul>

## Yearly Digest

<ul>
  {% assign yearly_en = site.posts | where: "lang", "en" | where: "period", "yearly" %}
  {% for post in yearly_en limit:20 %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.period_id | default: post.date }}</a>
    </li>
  {% else %}
    <li><em>No posts yet</em></li>
  {% endfor %}
</ul>

</div>
