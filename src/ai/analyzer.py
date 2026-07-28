"""Content analysis using AI."""

import asyncio
import json
import math
import re
from typing import List, Optional
from tenacity import retry, stop_after_attempt, wait_exponential
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, MofNCompleteColumn

from .client import AIClient
from .prompts import CONTENT_ANALYSIS_SYSTEM, CONTENT_ANALYSIS_USER
from .utils import parse_json_response
from ..models import ContentItem

DEFAULT_THROTTLE_SEC = 0.0
ANALYSIS_STATUS_KEY = "analysis_status"
ANALYSIS_STATUS_OK = "ok"
ANALYSIS_STATUS_FAILED = "failed"
ERROR_BODY_LIMIT = 500
SCORING_FAILURE_RATE_THRESHOLD = 0.5


def _redact_error_text(text: str) -> str:
    """Remove common credential shapes before an upstream error is logged."""
    redacted = re.sub(
        r"(?i)([\"']?(?:api[_-]?key|authorization|access[_-]?token|token|secret)"
        r"[\"']?\s*[:=]\s*[\"']?)([^\"',}\s]+)",
        r"\1[REDACTED]",
        text,
    )
    redacted = re.sub(r"(?i)\bBearer\s+\S+", "Bearer [REDACTED]", redacted)
    redacted = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "sk-[REDACTED]", redacted)
    return " ".join(redacted.split())[:ERROR_BODY_LIMIT]


def _error_details(error: Exception) -> tuple[str, str, str]:
    """Return sanitized (HTTP status, request id, response summary)."""
    def safe_getattr(value, name, default=None):
        try:
            return getattr(value, name, default)
        except Exception:
            return default

    response = safe_getattr(error, "response")
    status = safe_getattr(error, "status_code")
    if status is None and response is not None:
        status = safe_getattr(response, "status_code")

    request_id = safe_getattr(error, "request_id")
    headers = safe_getattr(response, "headers", {}) if response is not None else {}
    if not request_id and hasattr(headers, "get"):
        request_id = headers.get("x-request-id") or headers.get("request-id")

    body = safe_getattr(error, "body")
    if body is None and response is not None:
        body = safe_getattr(response, "text")
    if body is None:
        body = str(error)
    if not isinstance(body, str):
        try:
            body = json.dumps(body, ensure_ascii=False)
        except (TypeError, ValueError):
            body = str(body)

    return (
        str(status) if status is not None else "n/a",
        str(request_id) if request_id else "n/a",
        _redact_error_text(body),
    )


def _client_identity(client: AIClient) -> tuple[str, str]:
    config = getattr(client, "config", None)
    provider = getattr(config, "provider", None) or getattr(client, "provider", "unknown")
    provider = getattr(provider, "value", provider)
    model = getattr(config, "model", None) or getattr(client, "model", "unknown")
    return str(provider), str(model)


def scoring_failure_context(
    items: List[ContentItem],
    client: AIClient,
    threshold: float = SCORING_FAILURE_RATE_THRESHOLD,
) -> Optional[dict]:
    """Describe an unreliable scoring batch, or return None when it is usable."""
    failure_count = sum(
        item.metadata.get(ANALYSIS_STATUS_KEY) == ANALYSIS_STATUS_FAILED
        for item in items
    )
    success_count = len(items) - failure_count
    failure_rate = failure_count / len(items) if items else 0.0
    if failure_rate <= threshold:
        return None
    provider, model = _client_identity(client)
    return {
        "success_count": success_count,
        "failure_count": failure_count,
        "failure_rate": failure_rate,
        "provider": provider,
        "model": model,
    }


class ContentAnalyzer:
    """Analyzes content items using AI to determine importance."""

    def __init__(self, ai_client: AIClient):
        self.client = ai_client

    @staticmethod
    def _parse_json_response(response: str) -> Optional[dict]:
        """Try multiple strategies to extract a JSON object from an AI response.

        Returns the parsed dict, or None if all strategies fail.
        """
        return parse_json_response(response)

    def _get_throttle_sec(self) -> float:
        """Return the configured inter-item throttle, clamped to zero or above."""
        config = getattr(self.client, "config", None)
        throttle_sec = getattr(config, "throttle_sec", DEFAULT_THROTTLE_SEC)
        return max(throttle_sec, 0.0)

    def _get_concurrency(self) -> int:
        """Return the configured analysis concurrency, clamped to 1 or above."""
        config = getattr(self.client, "config", None)
        concurrency = getattr(config, "analysis_concurrency", 1)
        return max(concurrency, 1)

    async def analyze_batch(self, items: List[ContentItem]) -> List[ContentItem]:
        throttle_sec = self._get_throttle_sec()
        concurrency = self._get_concurrency()
        semaphore = asyncio.Semaphore(concurrency)
        provider, model = _client_identity(self.client)
        success_count = 0
        failure_count = 0

        async def _process(item: ContentItem, index: int, progress_task) -> ContentItem:
            nonlocal success_count, failure_count
            async with semaphore:
                try:
                    await self._analyze_item(item)
                    item.metadata[ANALYSIS_STATUS_KEY] = ANALYSIS_STATUS_OK
                    success_count += 1
                except Exception as e:
                    status, request_id, body = _error_details(e)
                    print(
                        "analysis_failure "
                        f"item={item.id} provider={provider} model={model} "
                        f"http_status={status} request_id={request_id} "
                        f"error_type={type(e).__name__} body={body}"
                    )
                    item.ai_score = 0.0
                    item.ai_reason = "Analysis failed"
                    item.ai_summary = item.title
                    item.ai_tags = []
                    item.metadata[ANALYSIS_STATUS_KEY] = ANALYSIS_STATUS_FAILED
                    failure_count += 1
                if throttle_sec > 0 and index < len(items) - 1:
                    await asyncio.sleep(throttle_sec)
            progress.advance(progress_task)
            return item

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            MofNCompleteColumn(),
            transient=True,
        ) as progress:
            task = progress.add_task("Analyzing", total=len(items))
            coros = [
                _process(item, i, task) for i, item in enumerate(items)
            ]
            analyzed_items = await asyncio.gather(*coros)

        total = success_count + failure_count
        failure_rate = failure_count / total if total else 0.0
        print(
            "analysis_batch "
            f"success={success_count} failure={failure_count} "
            f"provider={provider} model={model} failure_rate={failure_rate:.1%}"
        )
        return analyzed_items

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=2, max=10),
        reraise=True,
    )
    async def _analyze_item(self, item: ContentItem) -> None:
        """Analyze a single content item.

        Args:
            item: Content item to analyze (modified in-place)
        """
        # Prepare content section
        content_section = ""
        if item.content:
            # Split off comments if present
            content_text = item.content
            if "--- Top Comments ---" in content_text:
                main, comments_part = content_text.split("--- Top Comments ---", 1)
                content_section = f"Content: {main.strip()[:800]}"
            else:
                content_section = f"Content: {content_text[:1000]}"

        # Prepare discussion section (comments, engagement)
        discussion_parts = []
        if item.content and "--- Top Comments ---" in item.content:
            comments_part = item.content.split("--- Top Comments ---", 1)[1]
            discussion_parts.append(f"Community Comments:\n{comments_part[:1500]}")

        meta = item.metadata
        engagement_items = []
        if meta.get("score"):
            engagement_items.append(f"score: {meta['score']}")
        if meta.get("descendants"):
            engagement_items.append(f"{meta['descendants']} comments")
        if meta.get("favorite_count"):
            engagement_items.append(f"{meta['favorite_count']} likes")
        if meta.get("retweet_count"):
            engagement_items.append(f"{meta['retweet_count']} retweets")
        if meta.get("reply_count"):
            engagement_items.append(f"{meta['reply_count']} replies")
        if meta.get("views"):
            engagement_items.append(f"{meta['views']} views")
        if meta.get("bookmarks"):
            engagement_items.append(f"{meta['bookmarks']} bookmarks")
        if meta.get("upvote_ratio"):
            engagement_items.append(f"upvote ratio: {meta['upvote_ratio']:.0%}")
        if engagement_items:
            discussion_parts.append(f"Engagement: {', '.join(engagement_items)}")
        if meta.get("discussion_url"):
            discussion_parts.append(f"Discussion: {meta['discussion_url']}")
        if meta.get("community_note"):
            discussion_parts.append(f"Community Note: {meta['community_note']}")

        discussion_section = "\n".join(discussion_parts) if discussion_parts else ""

        # Generate user prompt
        user_prompt = CONTENT_ANALYSIS_USER.format(
            title=item.title,
            source=f"{item.source_type.value}",
            author=item.author or "Unknown",
            url=str(item.url),
            content_section=content_section,
            discussion_section=discussion_section
        )

        # Get AI completion. A per-config prompt override (if present)
        # wins over the hardcoded default system prompt.
        config = getattr(self.client, "config", None)
        prompt_overrides = getattr(config, "prompt_overrides", None) or {}
        system_prompt = prompt_overrides.get("analysis_system") or CONTENT_ANALYSIS_SYSTEM
        response = await self.client.complete(
            system=system_prompt,
            user=user_prompt,
        )

        # Parse JSON response with robust fallback
        result = self._parse_json_response(response)
        if not isinstance(result, dict):
            raise ValueError(
                f"could not parse analysis response: {_redact_error_text(response)}"
            )

        # Update item with analysis results
        score_value = result.get("score")
        try:
            if isinstance(score_value, bool):
                raise TypeError("boolean is not a score")
            score = float(score_value)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "invalid analysis score "
                f"in response: {_redact_error_text(response)}"
            ) from error
        if not math.isfinite(score) or not 0 <= score <= 10:
            raise ValueError(
                "invalid analysis score "
                f"in response: {_redact_error_text(response)}"
            )
        item.ai_score = score
        item.ai_reason = result.get("reason", "")
        item.ai_summary = result.get("summary", item.title)
        item.ai_tags = result.get("tags", [])
