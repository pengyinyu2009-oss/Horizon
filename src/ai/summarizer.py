"""Daily / weekly / monthly / yearly summary generation — pure programmatic rendering.

All four roll-ups share a small helper layer (Pangu spacing, item
formatting, follow-up AI analysis). The daily summariser splits items
into two tiers: those at or above ``full_threshold`` get an expanded
section, those above the lower ``threshold`` but below
``full_threshold`` only appear in the table of contents.
"""

import json
import re
from typing import List, Dict, Optional, Tuple

from ..models import ContentItem


_CJK = r"[\u4e00-\u9fff\u3400-\u4dbf]"
_ASCII = r"[A-Za-z0-9]"


def _pangu(text: str) -> str:
    """Insert a space between CJK and ASCII letters/digits (Pangu spacing)."""
    text = re.sub(rf"({_CJK})({_ASCII})", r"\1 \2", text)
    text = re.sub(rf"({_ASCII})({_CJK})", r"\1 \2", text)
    return text


LABELS = {
    "en": {
        "header": "Horizon Daily",
        "source": "Source",
        "background": "Background",
        "discussion": "Discussion",
        "references": "References",
        "tags": "Tags",
        "selected_items": "From {total} items, {selected} important content pieces were selected",
        "empty_analyzed": "Analyzed {total} items, but none met the importance threshold.",
        "empty_body": (
            "No significant developments today. This might indicate:\n"
            "- A quiet day in your tracked sources\n"
            "- The AI score threshold is too high\n"
            "- Your information sources need expansion\n\n"
            "Consider:\n"
            "1. Lowering the `ai_score_threshold` in config.json\n"
            "2. Adding more diverse information sources\n"
            "3. Checking if the AI model is working correctly\n"
        ),
    },
    "zh": {
        "header": "Horizon 每日速递",
        "source": "来源",
        "background": "背景",
        "discussion": "社区讨论",
        "references": "参考链接",
        "tags": "标签",
        "selected_items": "从 {total} 条内容中筛选出 {selected} 条重要资讯。",
        "empty_analyzed": "已分析 {total} 条内容，但没有达到重要性阈值的条目。",
        "empty_body": (
            "今日暂无重要动态，可能原因：\n"
            "- 今天关注的信息源较平静\n"
            "- AI 评分阈值设置过高\n"
            "- 信息源种类有待扩充\n\n"
            "建议：\n"
            "1. 在 config.json 中降低 `ai_score_threshold`\n"
            "2. 添加更多多样化的信息源\n"
            "3. 检查 AI 模型是否正常工作\n"
        ),
    },
}


# --- Roll-up labels (weekly / monthly / yearly) ----------------------------

ROLLUP_LABELS = {
    "weekly": {
        "en": {
            "title": "Horizon Weekly",
            "intro": "This week's {n} most important stories, scored {lo}+ from the past {days} days.",
            "report_intro": "## Lead Story — must-read",
            "followup": "Follow-up & impact",
            "no_items": "No stories scored {lo}+ this week.",
        },
        "zh": {
            "title": "Horizon 上周总览",
            "intro": "本周 {days} 天内 {lo} 分以上 {n} 条要事速览。",
            "report_intro": "## 头条 — 必读",
            "followup": "后续与影响",
            "no_items": "本周暂无 {lo} 分以上的重要新闻。",
        },
    },
    "monthly": {
        "en": {
            "title": "Horizon Monthly",
            "intro": "This month's {n} most consequential stories, scored {lo}+ from the past {weeks} weeks.",
            "report_intro": "## Top {n} — monthly call-outs",
            "followup": "Follow-up & impact",
            "no_items": "No stories scored {lo}+ this month.",
        },
        "zh": {
            "title": "Horizon 上月总览",
            "intro": "本月 {weeks} 周内 {lo} 分以上 {n} 条要事速览。",
            "report_intro": "## 本月 Top {n}",
            "followup": "后续与影响",
            "no_items": "本月暂无 {lo} 分以上的重要新闻。",
        },
    },
    "yearly": {
        "en": {
            "title": "Horizon Yearly",
            "intro": "This year's {n} most consequential stories, scored {lo}+ from the past {months} months.",
            "report_intro": "## Top {n} — annual retrospective",
            "followup": "Long-term impact",
            "no_items": "No stories scored {lo}+ this year.",
        },
        "zh": {
            "title": "Horizon 本年总览",
            "intro": "本年 {months} 个月内 {lo} 分以上 {n} 条要事速览。",
            "report_intro": "## 年度 Top {n}",
            "followup": "长远影响",
            "no_items": "本年暂无 {lo} 分以上的重要新闻。",
        },
    },
}


# --- Follow-up analysis prompt --------------------------------------------

_FOLLOWUP_SYSTEM_ZH = """你是一位资深科技/产业分析师，正在做一份滚动回顾报告。
你的任务是基于原始新闻内容，撰写一段"后续与影响"分析，涵盖：
- 后续事件：这条新闻发布之后，是否有新的进展、回应、相关发布？
- 行业影响：对从业者、用户、生态可能产生的中长期影响是什么？
- 持续关注点：还有什么值得持续观察的关键节点？

要求：
- 用中文，200-400 字
- 直接给出结论性观点，不要"我们先来看看..."这种客套
- 不要重复新闻正文里已经讲过的内容
- 用简洁段落，不分小标题"""

_FOLLOWUP_SYSTEM_EN = """You are a senior tech/industry analyst preparing a retrospective.
Write a 'Follow-up & Impact' analysis covering:
- Subsequent events: any new developments, replies, related releases after this story broke?
- Industry impact: medium- and long-term consequences for practitioners, users, ecosystem?
- Watch list: what to keep tracking?

Constraints:
- 200-400 words
- Opinionated and direct, no preamble like "Let's first look at..."
- Don't repeat what the article already says
- One or two concise paragraphs, no sub-headings"""

_FOLLOWUP_USER_TEMPLATE_ZH = """原始新闻:
标题: {title}
来源: {source}
日期: {date}
正文摘要: {summary}

请基于以上信息，撰写一段"后续与影响"分析。"""

_FOLLOWUP_USER_TEMPLATE_EN = """Original story:
Title: {title}
Source: {source}
Date: {date}
Summary: {summary}

Write the Follow-up & Impact analysis now."""


def _format_followup_prompt(item: ContentItem, language: str) -> Tuple[str, str]:
    """Return (system_prompt, user_prompt) for the follow-up AI call."""
    if language == "zh":
        system = _FOLLOWUP_SYSTEM_ZH
        user_tmpl = _FOLLOWUP_USER_TEMPLATE_ZH
    else:
        system = _FOLLOWUP_SYSTEM_EN
        user_tmpl = _FOLLOWUP_USER_TEMPLATE_EN

    title = item.metadata.get(f"title_{language}") or item.title
    summary = (
        item.metadata.get(f"detailed_summary_{language}")
        or item.metadata.get("detailed_summary")
        or item.ai_summary
        or ""
    )
    source = item.metadata.get("feed_name") or item.source_type.value
    date = item.published_at.strftime("%Y-%m-%d") if item.published_at else "?"
    user = user_tmpl.format(title=title, source=source, date=date, summary=summary)
    return system, user


# --- DailySummarizer ------------------------------------------------------


class DailySummarizer:
    """Generates daily Markdown summaries from pre-analyzed content items.

    Two-tier output:
    - items scored >= ``threshold`` (default 7.0) appear in the TOC
    - items scored >= ``full_threshold`` (default 8.0) also get their
      own expanded section with summary / background / discussion / tags
    """

    def __init__(self):
        pass

    async def generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
        full_threshold: float = 8.0,
    ) -> str:
        """Generate daily summary in Markdown format.

        Items are rendered in score-descending order (already sorted by orchestrator).
        """
        labels = LABELS.get(language, LABELS["en"])

        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        sorted_items = sorted(items, key=lambda x: x.ai_score or 0, reverse=True)
        full_items = [it for it in sorted_items if (it.ai_score or 0) >= full_threshold]
        brief_items = [
            it for it in sorted_items
            if (it.ai_score or 0) < full_threshold
        ]

        n_total = len(sorted_items)
        n_full = len(full_items)
        if language == "zh":
            subline = (
                f"其中 **{n_full} 条 8 分以上**展开详细简报，其余 {n_total - n_full} 条"
                f"仅列于索引。"
            )
        else:
            subline = (
                f"**{n_full} items at 8+** get full write-ups; the other "
                f"{n_total - n_full} are listed in the index only."
            )

        header = (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['selected_items'].format(total=total_fetched, selected=n_total)}\n\n"
            f"{subline}\n\n"
            "---\n\n"
        )

        # TOC uses display order (full first, then brief)
        toc_entries: List[str] = []
        for display_idx, item in enumerate(full_items + brief_items, start=1):
            _t = item.metadata.get(f"title_{language}") or item.title
            t = str(_t).replace("[", "(").replace("]", ")")
            if language == "zh":
                t = _pangu(t)
            score = item.ai_score or "?"
            toc_entries.append(
                f"{display_idx}. [{t}](#item-{display_idx}) \u2b50\ufe0f {score}/10"
            )
        toc = "\n".join(toc_entries) + "\n\n---\n\n"

        body_parts: List[str] = []
        for display_idx, item in enumerate(full_items + brief_items, start=1):
            is_full = (item.ai_score or 0) >= full_threshold
            if is_full:
                body_parts.append(self._format_item(item, labels, language, display_idx))
            else:
                body_parts.append(self._format_brief_item(item, labels, language, display_idx))

        return header + toc + "".join(body_parts)

    def generate_webhook_overview(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate a compact overview for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        if not items:
            return self._generate_empty_summary(date, total_fetched, labels)

        if language == "zh":
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> 从 {total_fetched} 条内容中筛选出 {len(items)} 条重要资讯。\n\n"
                "下面会按新闻逐条发送详情，你可以只看感兴趣的标题。\n\n"
            )
        else:
            header = (
                f"# {labels['header']} - {date}\n\n"
                f"> Selected {len(items)} important items from {total_fetched} fetched items.\n\n"
                "Details will be sent item by item so you can read only the topics you care about.\n\n"
            )

        entries = []
        for i, item in enumerate(items, start=1):
            title = str(item.metadata.get(f"title_{language}") or item.title).replace("[", "(").replace("]", ")")
            if language == "zh":
                title = _pangu(title)
            score = item.ai_score or "?"
            entries.append(f"{i}. [{title}]({item.url}) \u2b50\ufe0f {score}/10")

        return header + "\n".join(entries)

    def generate_webhook_item(
        self,
        item: ContentItem,
        language: str,
        index: int,
        total: int,
    ) -> str:
        """Generate one item message for multi-message webhook delivery."""
        labels = LABELS.get(language, LABELS["en"])
        prefix = f"第 {index}/{total} 条\n\n" if language == "zh" else f"Item {index}/{total}\n\n"
        return prefix + self._format_item(item, labels, language, index).rstrip("-\n ")

    def _format_item(self, item: ContentItem, labels: dict, language: str, index: int) -> str:
        """Format a single ContentItem into Markdown (full write-up)."""
        _title = item.metadata.get(f"title_{language}") or item.title
        title = str(_title).replace("[", "(").replace("]", ")")
        url = str(item.url)
        score = item.ai_score or "?"
        meta = item.metadata

        summary = (
            meta.get(f"detailed_summary_{language}")
            or meta.get("detailed_summary")
            or item.ai_summary
            or ""
        )
        background = meta.get(f"background_{language}") or meta.get("background") or ""
        discussion = (
            meta.get(f"community_discussion_{language}")
            or meta.get("community_discussion")
            or ""
        )

        if language == "zh":
            title = _pangu(title)
            summary = _pangu(summary)
            background = _pangu(background)
            discussion = _pangu(discussion)

        source_type = item.source_type.value
        source_parts = [source_type]
        if meta.get("subreddit"):
            source_parts.append(f"r/{meta['subreddit']}")
        if meta.get("feed_name"):
            source_parts.append(meta["feed_name"])
        else:
            source_parts.append(item.author or "unknown")
        if item.published_at:
            if language == "zh":
                source_parts.append(
                    f"{item.published_at.month}月{item.published_at.day}日 "
                    f"{item.published_at:%H:%M}"
                )
            else:
                day = item.published_at.strftime("%d").lstrip("0")
                source_parts.append(item.published_at.strftime(f"%b {day}, %H:%M"))
        source_line = " \u00b7 ".join(source_parts)  # ·

        discussion_url = meta.get("discussion_url")
        if discussion_url:
            discussion_url = str(discussion_url)
            if discussion_url != url:
                source_line += f' · [{labels["discussion"]}]({discussion_url})'

        lines = [
            f'<a id="item-{index}"></a>',
            f"## [{title}]({url}) \u2b50\ufe0f {score}/10",  # ⭐️
            "",
            summary,
            "",
            source_line,
        ]

        if background:
            lines.append("")
            lines.append(f"**{labels['background']}**: {background}")

        sources = meta.get("sources") or []
        if sources:
            items_html = "".join(f'<li><a href="{s["url"]}">{s["title"]}</a></li>\n' for s in sources)
            lines += [
                "",
                f'<details><summary>{labels["references"]}</summary>\n<ul>\n{items_html}\n</ul>\n</details>',
            ]

        if discussion:
            lines.append("")
            lines.append(f"**{labels['discussion']}**: {discussion}")

        if item.ai_tags:
            tags_str = ", ".join([f"`#{t}`" for t in item.ai_tags])
            lines.append("")
            lines.append(f"**{labels['tags']}**: {tags_str}")

        lines.append("")
        lines.append("---")

        return "\n".join(lines) + "\n\n"

    def _format_brief_item(
        self, item: ContentItem, labels: dict, language: str, index: int
    ) -> str:
        """Format a sub-full-threshold item as a one-paragraph note.

        The item is already in the TOC; this is just a short reference so
        the page reads top-to-bottom without losing context. ``background``
        and ``discussion`` are dropped to keep the file short.
        """
        _title = item.metadata.get(f"title_{language}") or item.title
        title = str(_title).replace("[", "(").replace("]", ")")
        url = str(item.url)
        score = item.ai_score or "?"
        meta = item.metadata

        summary = (
            meta.get(f"detailed_summary_{language}")
            or meta.get("detailed_summary")
            or item.ai_summary
            or ""
        )
        if language == "zh":
            title = _pangu(title)
            summary = _pangu(summary)

        if language == "zh":
            note = "*（简报）*"
        else:
            note = "*(brief)*"

        return (
            f'<a id="item-{index}"></a>\n'
            f"### {note} [{title}]({url}) \u2b50\ufe0f {score}/10\n\n"
            f"{summary}\n\n"
            "---\n\n"
        )

    def _generate_empty_summary(self, date: str, total_fetched: int, labels: dict) -> str:
        """Generate summary when no high-scoring items were found."""
        return (
            f"# {labels['header']} - {date}\n\n"
            f"> {labels['empty_analyzed'].format(total=total_fetched)}\n\n"
            + labels["empty_body"]
        )


# --- Roll-up summarisers (weekly / monthly / yearly) ---------------------


class _RollupSummarizerBase:
    """Shared logic for weekly / monthly / yearly roll-ups.

    Each tier refetches the relevant time window, runs the same
    analysis pipeline as the daily run, and then asks the AI one more
    time to write a "Follow-up & Impact" paragraph for every item above
    the report threshold. The top N by score get a headline call-out
    block at the top of the report.
    """

    period: str = ""  # subclass sets: "weekly" / "monthly" / "yearly"

    def __init__(self, ai_client=None):
        # ai_client is optional so unit tests can construct without one
        self.ai_client = ai_client

    async def _ai_followup(
        self, item: ContentItem, language: str
    ) -> str:
        """Call the AI for a follow-up paragraph. Empty string on failure."""
        if not self.ai_client:
            return ""
        system, user = _format_followup_prompt(item, language)
        try:
            response = await self.ai_client.complete(
                system=system,
                user=user,
                temperature=0.4,
            )
            return (response or "").strip()
        except Exception:
            return ""

    async def generate_report(
        self,
        items: List[ContentItem],
        period_id: str,
        total_fetched: int,
        language: str,
        threshold: float,
        report_threshold: float,
        top_n_report: int,
        lookback_label: str,
    ) -> str:
        """Build the roll-up markdown.

        Args:
            items: Already-analyzed ContentItems from the lookback window.
            period_id: Display id for the report (e.g. ``2026-W25``,
                ``2026-06``, ``2026``).
            total_fetched: Total items the daily-equivalent pass picked up.
            language: ``en`` / ``zh``.
            threshold: Minimum score to appear in the TOC.
            report_threshold: Minimum score for the headline call-out.
            top_n_report: How many top items get a full follow-up block.
            lookback_label: Human-readable span used in the intro
                (e.g. ``7 days`` / ``5 weeks`` / ``12 months``).
        """
        labels = ROLLUP_LABELS[self.period][language]
        selected = sorted(
            [it for it in items if (it.ai_score or 0) >= threshold],
            key=lambda x: x.ai_score or 0,
            reverse=True,
        )
        if not selected:
            return self._empty_report(period_id, total_fetched, labels, language, threshold)

        n = len(selected)
        intro = labels["intro"].format(
            n=n, lo=threshold, days=lookback_label, weeks=lookback_label, months=lookback_label,
        )

        header = (
            f"# {labels['title']} — {period_id}\n\n"
            f"> {intro}\n\n"
            "---\n\n"
        )

        callout_items = [it for it in selected if (it.ai_score or 0) >= report_threshold]
        callout_items = callout_items[: max(top_n_report, 1)]
        callout_blocks: List[str] = []
        if callout_items:
            callout_intro = labels["report_intro"].format(n=len(callout_items))
            callout_blocks.append(f"## {callout_intro.lstrip('# ').strip()}\n")
            for i, item in enumerate(callout_items, start=1):
                followup = await self._ai_followup(item, language)
                callout_blocks.append(
                    self._format_callout(item, language, i, followup, labels)
                )
            callout_blocks.append("\n---\n\n")

        toc_lines = [f"## {'索引' if language == 'zh' else 'Index'}\n"]
        for i, item in enumerate(selected, start=1):
            t = item.metadata.get(f"title_{language}") or item.title
            t = str(t).replace("[", "(").replace("]", ")")
            if language == "zh":
                t = _pangu(t)
            score = item.ai_score or "?"
            toc_lines.append(f"{i}. [{t}](#{self.period}-item-{i}) \u2b50\ufe0f {score}/10")
        toc = "\n".join(toc_lines) + "\n\n---\n\n"

        body_parts: List[str] = []
        for i, item in enumerate(selected, start=1):
            body_parts.append(self._format_brief(item, language, i))
        body = "".join(body_parts)

        return header + "".join(callout_blocks) + toc + body

    def _format_callout(
        self,
        item: ContentItem,
        language: str,
        index: int,
        followup_text: str,
        labels: dict,
    ) -> str:
        title = item.metadata.get(f"title_{language}") or item.title
        title = str(title).replace("[", "(").replace("]", ")")
        if language == "zh":
            title = _pangu(title)
        score = item.ai_score or "?"
        url = str(item.url)
        summary = (
            item.metadata.get(f"detailed_summary_{language}")
            or item.metadata.get("detailed_summary")
            or item.ai_summary
            or ""
        )
        if language == "zh":
            summary = _pangu(summary)

        if language == "zh":
            source = f"来源 · {item.source_type.value}"
            if item.published_at:
                source += f" · {item.published_at.month}月{item.published_at.day}日"
        else:
            source = f"Source · {item.source_type.value}"
            if item.published_at:
                day = item.published_at.strftime("%d").lstrip("0")
                source += f" · {item.published_at.strftime(f'%b {day}')}"
        tags_str = (
            " · ".join(f"`#{t}`" for t in item.ai_tags)
            if item.ai_tags else ""
        )

        lines = [
            f"### [{title}]({url}) \u2b50\ufe0f {score}/10",
            "",
            summary,
            "",
            source,
        ]
        if tags_str:
            lines += ["", tags_str]
        if followup_text:
            head = f"**{labels['followup']}**:"
            lines += ["", head, "", followup_text]
        return "\n".join(lines) + "\n\n"

    def _format_brief(self, item: ContentItem, language: str, index: int) -> str:
        title = item.metadata.get(f"title_{language}") or item.title
        title = str(title).replace("[", "(").replace("]", ")")
        if language == "zh":
            title = _pangu(title)
        score = item.ai_score or "?"
        url = str(item.url)
        return (
            f'<a id="{self.period}-item-{index}"></a>\n'
            f"- [{title}]({url}) \u2b50\ufe0f {score}/10\n"
        )

    def _empty_report(
        self,
        period_id: str,
        total_fetched: int,
        labels: dict,
        language: str,
        threshold: float,
    ) -> str:
        return (
            f"# {labels['title']} — {period_id}\n\n"
            f"> {labels['no_items'].format(lo=threshold)}\n\n"
            f"_Total items scored this period: {total_fetched}._"
        )


class WeeklySummarizer(_RollupSummarizerBase):
    period = "weekly"


class MonthlySummarizer(_RollupSummarizerBase):
    period = "monthly"


class YearlySummarizer(_RollupSummarizerBase):
    period = "yearly"
