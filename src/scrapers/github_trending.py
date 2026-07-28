"""GitHub Trending board scraper (2026-07-28).

GitHub has no official trending API, so this scrapes
``https://github.com/trending[<language>]?since=daily|weekly|monthly``
directly — the page exposes the richest field set, including the
per-period star increment ("1,024 stars this week"). GitHub natively
publishes daily/weekly/monthly boards; all configured periods are
fetched every run so the report can render the three sub-boards side
by side.

Degradation chain: if HTML parsing yields zero rows for *every*
period (markup change, network block), the scraper falls back to the
OSS Insight API (already integrated for the OSHW board) so the board
degrades instead of going blank. A distinct ``ALERT`` line is printed
when even the fallback produces nothing.
"""

import re
from datetime import datetime, timezone
from typing import List, Optional, Tuple

import httpx
from bs4 import BeautifulSoup

from ..models import (
    ContentItem,
    GitHubTrendingConfig,
    OSSInsightConfig,
    SourceType,
)
from .base import BaseScraper
from .ossinsight import OSSInsightScraper


_PERIOD_LABELS = {
    "daily": "today",
    "weekly": "this week",
    "monthly": "this month",
}

# OSS Insight period used as fallback for each GitHub trending period.
_OSS_PERIOD_MAP = {
    "daily": "past_24_hours",
    "weekly": "past_week",
    "monthly": "past_28_days",
}

_NUMBER_RE = re.compile(r"[\d,]+")


def _parse_count(text: str) -> int:
    """Parse '12,345' / '1,024 stars today' style counts to int."""
    m = _NUMBER_RE.search(text or "")
    if not m:
        return 0
    try:
        return int(m.group(0).replace(",", ""))
    except ValueError:
        return 0


class GitHubTrendingScraper(BaseScraper):
    """Scraper for github.com/trending (daily/weekly/monthly sub-boards)."""

    BASE_URL = "https://github.com/trending"

    def __init__(self, config: GitHubTrendingConfig, http_client: httpx.AsyncClient):
        super().__init__(config, http_client)
        self.cfg: GitHubTrendingConfig = config
        self._keywords_lower = [kw.lower() for kw in self.cfg.keywords if kw]

    async def fetch(self, since: datetime) -> List[ContentItem]:
        """Fetch every configured (period, language) trending board."""
        if not self.cfg.enabled:
            return []

        items: List[ContentItem] = []
        seen_ids: set[str] = set()
        parsed_periods = 0

        for period in self.cfg.periods:
            period_rows: List[Tuple[str, str, str, str, int, int, int]] = []
            for language in self.cfg.languages:
                period_rows.extend(await self._fetch_board(period, language))
            if period_rows:
                parsed_periods += 1
            period_count = 0
            for row in period_rows:
                item = self._row_to_item(row, period)
                if item is None or item.id in seen_ids:
                    continue
                seen_ids.add(item.id)
                items.append(item)
                period_count += 1
                if period_count >= self.cfg.max_items:
                    break  # page order is GitHub's own ranking — keep the top

        if parsed_periods == 0 and self.cfg.fallback_to_ossinsight:
            print(
                "github_trending: HTML parsing yielded 0 rows for every "
                "period, falling back to OSS Insight"
            )
            items = await self._fallback_fetch()

        if not items:
            print(
                "ALERT github_trending_empty: no trending data from HTML "
                "or fallback; board will render empty"
            )

        return items

    async def _fetch_board(
        self, period: str, language: str
    ) -> List[Tuple[str, str, str, str, int, int, int]]:
        """Fetch and parse one trending page.

        Returns rows of (repo, description, language, url,
        total_stars, forks, period_stars).
        """
        url = f"{self.BASE_URL}/{language}" if language else self.BASE_URL
        try:
            response = await self.client.get(
                url,
                params={"since": period},
                headers={
                    "Accept": "text/html",
                    "User-Agent": "Horizon/1.0 (+github-trending-board)",
                },
                timeout=20.0,
                follow_redirects=True,
            )
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(f"github_trending: fetch failed for {period}/{language or 'all'}: {e}")
            return []
        return self.parse_trending_html(response.text, period)

    @staticmethod
    def parse_trending_html(
        html: str, period: str
    ) -> List[Tuple[str, str, str, str, int, int, int]]:
        """Parse one trending page into rows.

        Kept static and pure so fixture tests can drive it without HTTP.
        """
        soup = BeautifulSoup(html, "html.parser")
        rows = []
        for article in soup.select("article.Box-row"):
            link = article.select_one("h2 a[href]")
            if not link or not link.get("href"):
                continue
            repo = link["href"].strip("/")
            if "/" not in repo:
                continue

            desc_el = article.select_one("p")
            description = desc_el.get_text(strip=True) if desc_el else ""

            lang_el = article.select_one('[itemprop="programmingLanguage"]')
            language = lang_el.get_text(strip=True) if lang_el else ""

            stars_el = article.select_one('a[href$="/stargazers"]')
            total_stars = _parse_count(stars_el.get_text()) if stars_el else 0

            forks_el = article.select_one('a[href$="/forks"]')
            forks = _parse_count(forks_el.get_text()) if forks_el else 0

            period_el = article.select_one("span.float-sm-right")
            period_stars = _parse_count(period_el.get_text()) if period_el else 0

            rows.append((
                repo,
                description,
                language,
                f"https://github.com/{repo}",
                total_stars,
                forks,
                period_stars,
            ))
        return rows

    def _row_to_item(self, row, period: str) -> Optional[ContentItem]:
        repo, description, language, url, total_stars, forks, period_stars = row

        if self.cfg.min_stars and total_stars < self.cfg.min_stars:
            return None
        if self._keywords_lower:
            haystack = f"{repo} {description}".lower()
            if not any(kw in haystack for kw in self._keywords_lower):
                return None

        label = _PERIOD_LABELS.get(period, period)
        title = f"{repo} (+{period_stars}⭐ {label})"
        content_lines = [
            f"GitHub Trending ({period}): {repo}",
            f"Stars {label}: {period_stars}",
            f"Total stars: {total_stars}",
            f"Forks: {forks}",
        ]
        if language:
            content_lines.append(f"Language: {language}")
        if description:
            content_lines += ["", description]

        return ContentItem(
            id=self._generate_id(SourceType.GITHUB_TRENDING.value, period, repo),
            source_type=SourceType.GITHUB_TRENDING,
            title=title,
            url=url,
            content="\n".join(content_lines),
            author=repo.split("/")[0],
            published_at=datetime.now(timezone.utc),
            metadata={
                "repo": repo,
                "period": period,
                "stars_gained": period_stars,
                "total_stars": total_stars,
                "forks": forks,
                "primary_language": language,
                "description": description,
            },
        )

    async def _fallback_fetch(self) -> List[ContentItem]:
        """Degrade to OSS Insight when the trending pages unparse."""
        items: List[ContentItem] = []
        seen_ids: set[str] = set()
        for period in self.cfg.periods:
            oss_period = _OSS_PERIOD_MAP.get(period)
            if not oss_period:
                continue
            oss_cfg = OSSInsightConfig(
                enabled=True,
                period=oss_period,
                languages=["All"],
                keywords=self.cfg.keywords,
                min_stars=self.cfg.min_stars,
                max_items=self.cfg.max_items,
            )
            rows = await OSSInsightScraper(oss_cfg, self.client).fetch(
                datetime.now(timezone.utc)
            )
            for item in rows:
                repo = item.metadata.get("repo") or item.title
                item.id = self._generate_id(
                    SourceType.GITHUB_TRENDING.value, period, str(repo)
                )
                if item.id in seen_ids:
                    continue
                seen_ids.add(item.id)
                item.source_type = SourceType.GITHUB_TRENDING
                item.metadata["period"] = period
                item.metadata["fallback"] = "ossinsight"
                label = _PERIOD_LABELS.get(period, period)
                gained = item.metadata.get("stars_gained", 0)
                item.title = f"{repo} (+{gained}⭐ {label})"
                items.append(item)
        return items
