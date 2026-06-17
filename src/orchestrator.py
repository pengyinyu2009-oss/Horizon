"""Main orchestrator coordinating the entire workflow."""

import asyncio
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from urllib.parse import urlparse
import httpx
from rich.console import Console

from .models import Config, ContentItem, Story
from .storage.manager import StorageManager
from .services.email import EmailManager
from .services.webhook import WebhookNotifier
from .scrapers.github import GitHubScraper
from .scrapers.hackernews import HackerNewsScraper
from .scrapers.rss import RSSScraper
from .scrapers.reddit import RedditScraper
from .scrapers.telegram import TelegramScraper
from .scrapers.twitter import TwitterScraper
from .scrapers.openbb import OpenBBScraper
from .scrapers.ossinsight import OSSInsightScraper
from .ai.client import create_ai_client
from .ai.analyzer import ContentAnalyzer
from .ai.summarizer import (
    DailySummarizer,
    WeeklySummarizer,
    MonthlySummarizer,
    YearlySummarizer,
)
from .ai.enricher import ContentEnricher
from .ai.tokens import get_usage_snapshot


class HorizonOrchestrator:
    """Orchestrates the complete workflow for content aggregation and analysis."""

    def __init__(self, config: Config, storage: StorageManager):
        """Initialize orchestrator.

        Args:
            config: Application configuration
            storage: Storage manager
        """
        self.config = config
        self.storage = storage
        self.console = Console()
        self.email_manager = EmailManager(config.email, console=self.console) if config.email else None
        self.webhook_notifier = (
            WebhookNotifier(config.webhook, console=self.console)
            if config.webhook and config.webhook.enabled
            else None
        )

    async def run(self, force_hours: int = None) -> None:
        """Execute the complete workflow.

        Args:
            force_hours: Optional override for time window in hours
        """
        self.console.print("[bold cyan]🌅 Horizon - Starting aggregation...[/bold cyan]\n")

        # Check email subscriptions if configured
        if (
            self.email_manager
            and self.config.email
            and self.config.email.enabled
            and self.config.email.imap_enabled
        ):
            self.console.print("📧 Checking for new email subscriptions...")
            self.email_manager.check_subscriptions(self.storage)

        try:
            # 1. Determine time window
            since = self._determine_time_window(force_hours)
            self.console.print(f"📅 Fetching content since: {since.strftime('%Y-%m-%d %H:%M:%S')}\n")

            # 2. Fetch content from all sources
            all_items = await self.fetch_all_sources(since)
            self.console.print(f"📥 Fetched {len(all_items)} items from all sources\n")

            if not all_items:
                self.console.print("[yellow]No new content found. Exiting.[/yellow]")
                return

            # 3. Merge cross-source duplicates (same URL from different sources)
            merged_items = self.merge_cross_source_duplicates(all_items)
            if len(merged_items) < len(all_items):
                self.console.print(
                    f"🔗 Merged {len(all_items) - len(merged_items)} cross-source duplicates "
                    f"→ {len(merged_items)} unique items\n"
                )

            # 4. Analyze with AI
            analyzed_items = await self._analyze_content(merged_items)
            self.console.print(f"🤖 Analyzed {len(analyzed_items)} items with AI\n")

            # 5. Filter by score threshold
            threshold = self.config.filtering.ai_score_threshold
            important_items = [
                item for item in analyzed_items
                if item.ai_score and item.ai_score >= threshold
            ]
            important_items.sort(key=lambda x: x.ai_score or 0, reverse=True)

            self.console.print(
                f"⭐️ {len(important_items)} items scored ≥ {threshold}\n"
            )

            # 5.5 Semantic deduplication: drop items covering the same topic
            deduped_items = await self.merge_topic_duplicates(important_items)
            if len(deduped_items) < len(important_items):
                self.console.print(
                    f"🧹 Removed {len(important_items) - len(deduped_items)} topic duplicates "
                    f"→ {len(deduped_items)} unique items\n"
                )
            important_items = deduped_items

            # 5.6 Optional second-stage Twitter reply expansion + targeted re-analysis
            await self._expand_twitter_discussion(important_items)

            # Show per-sub-source selection breakdown
            selected_counts: Dict[str, int] = defaultdict(int)
            for item in important_items:
                key = f"{item.source_type.value}/{self._sub_source_label(item)}"
                selected_counts[key] += 1
            for source_key, count in sorted(selected_counts.items()):
                self.console.print(f"      • {source_key}: {count}")
            self.console.print("")

            # 6. Search related stories + enrich with background knowledge (2nd AI pass)
            # skipped: enrich blocked by sandbox network; go direct to summarize

            # 7. Generate and save daily summaries for each configured language
            today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            full_threshold = self.config.filtering.ai_score_full_threshold
            for lang in self.config.ai.languages:
                summarizer = DailySummarizer()
                summary = await summarizer.generate_summary(
                    important_items,
                    today,
                    len(all_items),
                    language=lang,
                    full_threshold=full_threshold,
                )

                # Save to data/summaries/
                summary_path = self.storage.save_daily_summary(today, summary, language=lang)
                self.console.print(f"💾 Saved {lang.upper()} summary to: {summary_path}\n")

                # Copy to docs/ for GitHub Pages
                try:
                    from pathlib import Path

                    post_filename = f"{today}-horizon-{lang}.md"
                    posts_dir = Path("docs/_posts")
                    posts_dir.mkdir(parents=True, exist_ok=True)

                    dest_path = posts_dir / post_filename

                    # The save_daily_summary already wrote front matter
                    # to data/summaries/. Read it back so the deployed
                    # copy preserves the period/period_id fields.
                    with open(summary_path, "r", encoding="utf-8") as f:
                        stored = f.read()
                    with open(dest_path, "w", encoding="utf-8") as f:
                        f.write(stored)

                    self.console.print(f"📄 Copied {lang.upper()} summary to GitHub Pages: {dest_path}\n")
                except Exception as e:
                    self.console.print(f"[yellow]⚠️  Failed to copy {lang.upper()} summary to docs/: {e}[/yellow]\n")

                # Send email if configured
                if self.email_manager and self.config.email and self.config.email.enabled:
                    self.console.print(f"📧 Sending {lang.upper()} email summary...")
                    subscribers = self.storage.load_subscribers()
                    subject = f"Horizon Summary ({lang.upper()}) - {today}"
                    self.email_manager.send_daily_summary(summary, subject, subscribers)

                # Send webhook notification if configured
                if self.webhook_notifier:
                    await self.webhook_notifier.send_daily_summary(
                        summary=summary,
                        important_items=important_items,
                        all_items_count=len(all_items),
                        date=today,
                        lang=lang,
                        summarizer=summarizer,
                    )

            self.console.print("[bold green]✅ Horizon completed successfully![/bold green]")
            usage = get_usage_snapshot()
            if usage.total_tokens > 0:
                self.console.print(
                    f"\n🧮 Token usage this run: "
                    f"{usage.total_tokens} tokens "
                    f"(input: {usage.total_input_tokens}, output: {usage.total_output_tokens})"
                )
                for provider, u in sorted(usage.per_provider.items()):
                    if u.total <= 0:
                        continue
                    self.console.print(
                        f"   • {provider}: {u.total} tokens "
                        f"(in: {u.input_tokens}, out: {u.output_tokens})"
                    )

        except Exception as e:
            self.console.print(f"[bold red]❌ Error: {e}[/bold red]")

            # Send webhook failure notification if configured
            if self.webhook_notifier:
                await self.webhook_notifier.send_failure(
                    date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                    error_message=str(e),
                )

            raise

    def _determine_time_window(self, force_hours: int = None) -> datetime:
        if force_hours:
            since = datetime.now(timezone.utc) - timedelta(hours=force_hours)
        else:
            hours = self.config.filtering.time_window_hours
            since = datetime.now(timezone.utc) - timedelta(hours=hours)
        return since

    async def fetch_all_sources(self, since: datetime) -> List[ContentItem]:
        """Fetch content from all configured sources.

        This is a stable stage entry point for integrations such as MCP.

        Args:
            since: Fetch items published after this time

        Returns:
            List[ContentItem]: All fetched items
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            tasks = []

            # GitHub sources
            if self.config.sources.github:
                github_scraper = GitHubScraper(self.config.sources.github, client)
                tasks.append(self._fetch_with_progress("GitHub", github_scraper, since))

            # Hacker News
            if self.config.sources.hackernews.enabled:
                hn_scraper = HackerNewsScraper(self.config.sources.hackernews, client)
                tasks.append(self._fetch_with_progress("Hacker News", hn_scraper, since))

            # RSS feeds
            if self.config.sources.rss:
                rss_scraper = RSSScraper(self.config.sources.rss, client)
                tasks.append(self._fetch_with_progress("RSS Feeds", rss_scraper, since))

            # Reddit
            if self.config.sources.reddit.enabled:
                reddit_scraper = RedditScraper(self.config.sources.reddit, client)
                tasks.append(self._fetch_with_progress("Reddit", reddit_scraper, since))

            # Telegram
            if self.config.sources.telegram.enabled:
                telegram_scraper = TelegramScraper(self.config.sources.telegram, client)
                tasks.append(self._fetch_with_progress("Telegram", telegram_scraper, since))

            # Twitter
            if self.config.sources.twitter and self.config.sources.twitter.enabled:
                twitter_scraper = TwitterScraper(self.config.sources.twitter, client)
                tasks.append(self._fetch_with_progress("Twitter", twitter_scraper, since))

            # OpenBB (financial news / filings via the OpenBB Platform SDK)
            if self.config.sources.openbb and self.config.sources.openbb.enabled:
                openbb_scraper = OpenBBScraper(self.config.sources.openbb, client)
                tasks.append(self._fetch_with_progress("OpenBB", openbb_scraper, since))

            # OSS Insight trending repos
            if self.config.sources.ossinsight and self.config.sources.ossinsight.enabled:
                oss_scraper = OSSInsightScraper(self.config.sources.ossinsight, client)
                tasks.append(self._fetch_with_progress("OSS Insight", oss_scraper, since))

            # Fetch all concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Flatten results
            all_items = []
            for result in results:
                if isinstance(result, Exception):
                    self.console.print(f"[red]Error fetching source: {result}[/red]")
                elif isinstance(result, list):
                    all_items.extend(result)

            return all_items

    async def _fetch_with_progress(self, name: str, scraper, since: datetime) -> List[ContentItem]:
        """Fetch from a scraper with progress indication.

        Args:
            name: Source name for display
            scraper: Scraper instance
            since: Fetch items after this time

        Returns:
            List[ContentItem]: Fetched items
        """
        self.console.print(f"🔍 Fetching from {name}...")
        items = await scraper.fetch(since)
        self.console.print(f"   Found {len(items)} items from {name}")

        # Show per-sub-source breakdown when there are multiple sub-sources
        sub_counts: Dict[str, int] = defaultdict(int)
        for item in items:
            sub_counts[self._sub_source_label(item)] += 1
        if len(sub_counts) > 1:
            for sub, count in sorted(sub_counts.items()):
                self.console.print(f"      • {sub}: {count}")

        return items

    @staticmethod
    def _sub_source_label(item: ContentItem) -> str:
        """Return a human-readable sub-source label for an item."""
        meta = item.metadata
        if meta.get("subreddit"):
            return f"r/{meta['subreddit']}"
        if meta.get("feed_name"):
            return meta["feed_name"]
        if meta.get("channel"):
            return f"@{meta['channel']}"
        if meta.get("period") and meta.get("repo"):
            return f"ossinsight:{meta.get('primary_language', 'all')}"
        if meta.get("repo"):
            return meta["repo"]
        if meta.get("watchlist"):
            return meta["watchlist"]
        return item.author or "unknown"

    def merge_cross_source_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items that point to the same URL from different sources.

        This is a stable stage helper for integrations such as MCP.

        Keeps the item with the richest content and combines metadata.

        Args:
            items: Items to deduplicate

        Returns:
            List[ContentItem]: Deduplicated items
        """
        def normalize_url(url: str) -> str:
            parsed = urlparse(str(url))
            # Strip www prefix, trailing slashes, and fragments
            host = parsed.hostname or ""
            if host.startswith("www."):
                host = host[4:]
            path = parsed.path.rstrip("/")
            return f"{host}{path}"

        # Group by normalized URL
        url_groups: Dict[str, List[ContentItem]] = {}
        for item in items:
            key = normalize_url(str(item.url))
            url_groups.setdefault(key, []).append(item)

        merged = []
        for key, group in url_groups.items():
            if len(group) == 1:
                merged.append(group[0])
                continue

            # Pick the item with the richest content as primary
            primary = max(group, key=lambda x: len(x.content or ""))

            # Merge metadata and source info from other items
            all_sources = set()
            for item in group:
                all_sources.add(item.source_type.value)
                # Merge metadata (engagement, discussion, etc.)
                for mk, mv in item.metadata.items():
                    if mk not in primary.metadata or not primary.metadata[mk]:
                        primary.metadata[mk] = mv

                # Append content (e.g., comments from another source)
                if item is not primary and item.content:
                    if primary.content and item.content not in primary.content:
                        primary.content = (primary.content or "") + f"\n\n--- From {item.source_type.value} ---\n" + item.content

            primary.metadata["merged_sources"] = list(all_sources)
            merged.append(primary)

        return merged

    async def merge_topic_duplicates(self, items: List[ContentItem]) -> List[ContentItem]:
        """Merge items covering the same topic using AI semantic deduplication.

        This is a stable stage helper for integrations such as MCP.

        Sends all item titles, tags, and summaries to AI in a single call.
        Items must already be sorted by ai_score descending so that the first
        item in each duplicate group is always the highest-scored one.
        Content (comments) from duplicate items is merged into the primary.

        Falls back to returning items unchanged if the AI call fails.
        """
        if len(items) <= 1:
            return items

        from .ai.prompts import TOPIC_DEDUP_SYSTEM, TOPIC_DEDUP_USER
        from .ai.utils import parse_json_response

        # Build the item list for the prompt
        lines = []
        for i, item in enumerate(items):
            tags = ", ".join(item.ai_tags) if item.ai_tags else "—"
            summary = item.ai_summary or "—"
            lines.append(f"[{i}] {item.title}\n    Tags: {tags}\n    Summary: {summary}")
        items_text = "\n\n".join(lines)

        try:
            ai_client = create_ai_client(self.config.ai)
            response = await ai_client.complete(
                system=TOPIC_DEDUP_SYSTEM,
                user=TOPIC_DEDUP_USER.format(items=items_text),
            )
            result = parse_json_response(response)
            if result is None:
                self.console.print("[yellow]  dedup: could not parse AI response, skipping[/yellow]")
                return items

            duplicate_groups = result.get("duplicates", [])
        except Exception as e:
            self.console.print(f"[yellow]  dedup: AI call failed ({e}), skipping[/yellow]")
            return items

        if not duplicate_groups:
            return items

        # Build a set of indices to drop (all non-primary duplicates)
        drop_indices: set[int] = set()
        for group in duplicate_groups:
            if not isinstance(group, list) or len(group) < 2:
                continue
            primary_idx = group[0]
            if primary_idx < 0 or primary_idx >= len(items):
                continue
            primary = items[primary_idx]
            for dup_idx in group[1:]:
                if not isinstance(dup_idx, int) or dup_idx < 0 or dup_idx >= len(items):
                    continue
                if dup_idx == primary_idx:
                    continue
                dup = items[dup_idx]
                # Merge comments/content from the duplicate into the primary
                if dup.content:
                    if not primary.content or dup.content not in primary.content:
                        label = dup.source_type.value
                        primary.content = (primary.content or "") + f"\n\n--- From {label} ---\n{dup.content}"
                self.console.print(
                    f"   [dim]dedup: keep [{primary_idx}] {primary.title}[/dim]\n"
                    f"   [dim]       drop [{dup_idx}] {dup.title}[/dim]"
                )
                drop_indices.add(dup_idx)

        return [item for i, item in enumerate(items) if i not in drop_indices]

    async def _expand_twitter_discussion(self, items: List[ContentItem]) -> None:
        """Second-stage: fetch reply text for important Twitter items and re-analyze.

        Only runs when sources.twitter.fetch_reply_text is True.
        Bounded by max_tweets_to_expand to control cost.
        """
        tw_cfg = self.config.sources.twitter
        if not tw_cfg or not tw_cfg.enabled or not tw_cfg.fetch_reply_text:
            return

        from .models import SourceType

        twitter_items = [
            item for item in items
            if item.source_type == SourceType.TWITTER
        ][:tw_cfg.max_tweets_to_expand]

        if not twitter_items:
            return

        self.console.print(
            f"💬 Fetching reply text for {len(twitter_items)} Twitter items..."
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            scraper = TwitterScraper(tw_cfg, client)
            expanded = []
            for item in twitter_items:
                try:
                    reply_lines = await scraper.fetch_replies_for_item(item)
                    if TwitterScraper.append_discussion_content(item, reply_lines):
                        expanded.append(item)
                        self.console.print(
                            f"   💬 {len(reply_lines)} replies added to: {item.title[:60]}"
                        )
                except Exception as exc:
                    self.console.print(
                        f"   [yellow]⚠️  Reply fetch failed for {item.id}: {exc}[/yellow]"
                    )

        if not expanded:
            return

        self.console.print(
            f"   Re-analyzing {len(expanded)} Twitter items with reply context...\n"
        )
        ai_client = create_ai_client(self.config.ai)
        analyzer = ContentAnalyzer(ai_client)
        await analyzer.analyze_batch(expanded)

    async def _enrich_important_items(self, items: List[ContentItem]) -> None:
        """Enrich items with background knowledge (2nd AI pass).

        For each item that passed the score threshold, call AI to generate
        background knowledge based on the item's actual content.

        Args:
            items: Important items to enrich (modified in-place)
        """
        if not items:
            return

        self.console.print("📚 Enriching with background knowledge...")
        ai_client = create_ai_client(self.config.ai)
        enricher = ContentEnricher(ai_client)
        await enricher.enrich_batch(items)
        self.console.print(f"   Enriched {len(items)} items\n")

    async def _analyze_content(self, items: List[ContentItem]) -> List[ContentItem]:
        """Analyze content items with AI.

        Args:
            items: Items to analyze

        Returns:
            List[ContentItem]: Analyzed items
        """
        self.console.print("🤖 Analyzing content with AI...")

        ai_client = create_ai_client(self.config.ai)
        analyzer = ContentAnalyzer(ai_client)

        return await analyzer.analyze_batch(items)

    async def _generate_summary(
        self,
        items: List[ContentItem],
        date: str,
        total_fetched: int,
        language: str = "en",
    ) -> str:
        """Generate daily summary.

        Args:
            items: Important items to include (already enriched with background/related)
            date: Date string
            total_fetched: Total items fetched
            language: Output language ("en" or "zh")

        Returns:
            str: Markdown summary
        """
        self.console.print("📝 Generating daily summary...")

        summarizer = DailySummarizer()

        return await summarizer.generate_summary(items, date, total_fetched, language=language)

    # --- Roll-up workflows: weekly / monthly / yearly ---------------------

    async def _run_rollup(
        self,
        period: str,
        lookback_label_zh: str,
        lookback_label_en: str,
        save_method_name: str,
        period_id_factory,
    ) -> None:
        """Chain-mode implementation for weekly / monthly / yearly reports.

        Each tier reads the *previous* tier's reports from
        ``data/summaries/`` instead of re-fetching the source stream:

        - weekly:    reads daily summaries (8+ stories)
        - monthly:   reads weekly summaries (9+ callouts)
        - yearly:    reads monthly summaries (9+ callouts)

        For every story we call ``search.search_related_for_stories`` to
        pull related HN/Reddit discussion, then ask the AI to combine
        the original story with that community signal into a follow-up
        paragraph.
        """
        period_cfg = getattr(self.config, period, None)
        if period_cfg is None or not period_cfg.enabled:
            self.console.print(
                f"[yellow]⏭  {period} rollup is disabled in config; skipping.[/yellow]"
            )
            return

        # Which prior-tier reports do we read?
        prior_period = {"weekly": "daily", "monthly": "weekly", "yearly": "monthly"}[period]
        lookback_count = {
            "weekly": period_cfg.lookback_days,
            "monthly": period_cfg.lookback_weeks,
            "yearly": period_cfg.lookback_months,
        }[period]

        self.console.print(
            f"\n[bold cyan]📅 Horizon {period} rollup — "
            f"reading the last {lookback_count} {prior_period} reports[/bold cyan]\n"
        )

        languages = period_cfg.languages or self.config.ai.languages
        # Read prior reports per-language
        summaries_by_lang: Dict[str, List[Path]] = {}
        for lang in languages:
            files = self.storage.list_recent_summaries(
                period=prior_period,
                language=lang,
            )
            summaries_by_lang[lang] = files[-lookback_count:]
            self.console.print(
                f"   {lang}: {len(summaries_by_lang[lang])} {prior_period} report(s) to read\n"
            )

        # Per-language parse + web search + generate
        from .ai.summarizer import (
            parse_daily_full_stories,
            parse_rollup_callouts,
        )

        now = datetime.now(timezone.utc)
        period_id = period_id_factory(now)
        ai_client = create_ai_client(self.config.ai)
        summarizer_cls = {
            "weekly": WeeklySummarizer,
            "monthly": MonthlySummarizer,
            "yearly": YearlySummarizer,
        }[period]

        import httpx as _httpx

        for lang in languages:
            files = summaries_by_lang.get(lang, [])
            if not files:
                self.console.print(
                    f"[yellow]No {prior_period} reports for {lang}; skipping.[/yellow]"
                )
                continue

            # Parse stories from each prior report
            all_stories: List[Story] = []
            for f in files:
                md = f.read_text(encoding="utf-8")
                if prior_period == "daily":
                    stories = parse_daily_full_stories(md, lang)
                else:
                    stories = parse_rollup_callouts(md, lang)
                for s in stories:
                    # Tag the source date from the filename (YYYY-MM-DD-...)
                    s.source_date = f.stem.split("-horizon-")[0]
                all_stories.extend(stories)
            self.console.print(
                f"   {lang}: parsed {len(all_stories)} story(ies) from {len(files)} prior report(s)\n"
            )

            if not all_stories:
                self.console.print(
                    f"[yellow]No stories above threshold for {lang}; skipping.[/yellow]"
                )
                continue

            # Web search: one AsyncClient shared across calls
            async with _httpx.AsyncClient(timeout=30.0) as client:
                from .search import search_related_for_stories
                related = await search_related_for_stories(all_stories, client)
                self.console.print(
                    f"   {lang}: web search done ({sum(len(v) for v in related.values())} related stories)\n"
                )

                summarizer = summarizer_cls(ai_client=ai_client, http_client=client)
                lookback_label = lookback_label_zh if lang == "zh" else lookback_label_en
                report = await summarizer.generate_report(
                    stories=all_stories,
                    period_id=period_id,
                    language=lang,
                    threshold=period_cfg.ai_score_threshold,
                    report_threshold=period_cfg.ai_score_report_threshold,
                    top_n_report=period_cfg.top_n_report,
                    lookback_label=lookback_label,
                    related_by_index=related,
                )

            save_method = getattr(self.storage, save_method_name)
            saved = save_method(period_id, report, language=lang)
            self.console.print(f"💾 Saved {period} {lang.upper()} report to: {saved}\n")
            self._deploy_period_post(period, period_id, lang)

    def _deploy_period_post(self, period: str, period_id: str, lang: str) -> None:
        """Copy a freshly saved roll-up summary into docs/_posts/."""
        try:
            from pathlib import Path

            filename = f"{period_id}-horizon-{lang}.md"
            src = self.storage.summaries_dir / filename
            posts_dir = Path("docs/_posts")
            posts_dir.mkdir(parents=True, exist_ok=True)
            dest = posts_dir / filename

            if not src.exists():
                self.console.print(
                    f"[yellow]⚠️  Source {src} not found; skipping deploy.[/yellow]"
                )
                return

            with open(src, "r", encoding="utf-8") as f:
                stored = f.read()
            with open(dest, "w", encoding="utf-8") as f:
                f.write(stored)
            self.console.print(
                f"📄 Copied {period} {lang.upper()} report to GitHub Pages: {dest}\n"
            )
        except Exception as e:
            self.console.print(
                f"[yellow]⚠️  Failed to deploy {period} {lang} report: {e}[/yellow]\n"
            )

    async def run_weekly(self) -> None:
        """Run the weekly roll-up. Reads ``config.weekly`` for settings."""
        cfg = self.config.weekly
        if cfg is None:
            self.console.print("[yellow]weekly config missing; nothing to do.[/yellow]")
            return
        await self._run_rollup(
            period="weekly",
            lookback_label_zh=f"{cfg.lookback_days} 天",
            lookback_label_en=f"{cfg.lookback_days} days",
            save_method_name="save_weekly_summary",
            period_id_factory=lambda now: now.strftime("%G-W%V"),
        )

    async def run_monthly(self) -> None:
        """Run the monthly roll-up. Reads ``config.monthly`` for settings."""
        cfg = self.config.monthly
        if cfg is None:
            self.console.print("[yellow]monthly config missing; nothing to do.[/yellow]")
            return
        await self._run_rollup(
            period="monthly",
            lookback_label_zh=f"{cfg.lookback_weeks} 周",
            lookback_label_en=f"{cfg.lookback_weeks} weeks",
            save_method_name="save_monthly_summary",
            period_id_factory=lambda now: now.strftime("%Y-%m"),
        )

    async def run_yearly(self) -> None:
        """Run the yearly roll-up. Reads ``config.yearly`` for settings."""
        cfg = self.config.yearly
        if cfg is None:
            self.console.print("[yellow]yearly config missing; nothing to do.[/yellow]")
            return
        await self._run_rollup(
            period="yearly",
            lookback_label_zh=f"{cfg.lookback_months} 个月",
            lookback_label_en=f"{cfg.lookback_months} months",
            save_method_name="save_yearly_summary",
            period_id_factory=lambda now: now.strftime("%Y"),
        )
