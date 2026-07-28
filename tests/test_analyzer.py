import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

import pytest
from tenacity import wait_none

import src.ai.analyzer as analyzer_module
from src.ai.analyzer import ContentAnalyzer, scoring_failure_context
from src.models import ContentItem, SourceType


def _make_item(item_id: str) -> ContentItem:
    return ContentItem(
        id=item_id,
        source_type=SourceType.RSS,
        title=f"Item {item_id}",
        url="https://example.com/item",
        published_at=datetime(2026, 4, 26, tzinfo=timezone.utc),
    )


def test_analyze_batch_does_not_sleep_by_default(monkeypatch):
    analyzer = ContentAnalyzer(SimpleNamespace())
    items = [_make_item("rss:test:1"), _make_item("rss:test:2")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert len(result) == 2
    assert sleep_calls == []


def test_analyze_batch_sleeps_between_items_when_throttle_configured(monkeypatch):
    client = SimpleNamespace(config=SimpleNamespace(throttle_sec=1.5))
    analyzer = ContentAnalyzer(client)
    items = [_make_item("rss:test:1"), _make_item("rss:test:2"), _make_item("rss:test:3")]
    sleep_calls = []

    async def fake_analyze_item(item):
        item.ai_score = 8.0

    async def fake_sleep(seconds):
        sleep_calls.append(seconds)

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)
    monkeypatch.setattr(analyzer_module.asyncio, "sleep", fake_sleep)

    asyncio.run(analyzer.analyze_batch(items))

    assert sleep_calls == [1.5, 1.5]


def test_analyze_batch_concurrent_processing(monkeypatch):
    """Verify that higher concurrency allows overlapping item processing."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]
    active_count = 0
    max_active = 0

    async def fake_analyze_item(item):
        nonlocal active_count, max_active
        active_count += 1
        max_active = max(max_active, active_count)
        await asyncio.sleep(0.05)  # Small delay to allow overlap
        active_count -= 1

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    asyncio.run(analyzer.analyze_batch(items))

    assert max_active == 3
    assert all(item.ai_score is None for item in items)  # None because fake_analyze_item doesn't set it


def test_analyze_batch_concurrent_preserves_order(monkeypatch):
    """Verify that analyze_batch preserves input order in results."""
    client = SimpleNamespace(config=SimpleNamespace(analysis_concurrency=3))
    analyzer = ContentAnalyzer(client)
    items = [_make_item(f"rss:test:{i}") for i in range(5)]

    async def fake_analyze_item(item):
        item.ai_score = float(item.id.split(":")[-1]) * 10

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    result = asyncio.run(analyzer.analyze_batch(items))

    assert [item.id for item in result] == [item.id for item in items]


def test_analyze_batch_logs_sanitized_failure_summary(monkeypatch, capsys):
    class FakeResponse:
        status_code = 400
        text = '{"error":"invalid request","api_key":"super-secret"}'
        headers = {"x-request-id": "req-123"}

    class FakeHTTPError(Exception):
        response = FakeResponse()

    client = SimpleNamespace(
        config=SimpleNamespace(
            provider=SimpleNamespace(value="deepseek"),
            model="deepseek-chat",
        )
    )
    analyzer = ContentAnalyzer(client)
    items = [_make_item("rss:test:ok"), _make_item("rss:test:failed")]

    async def fake_analyze_item(item):
        if item.id.endswith("failed"):
            raise FakeHTTPError("request rejected")
        item.ai_score = 8.0

    monkeypatch.setattr(analyzer, "_analyze_item", fake_analyze_item)

    result = asyncio.run(analyzer.analyze_batch(items))
    output = capsys.readouterr().out

    assert result[0].metadata["analysis_status"] == "ok"
    assert result[1].metadata["analysis_status"] == "failed"
    assert "analysis_batch success=1 failure=1" in output
    assert "provider=deepseek model=deepseek-chat" in output
    assert "http_status=400" in output
    assert "request_id=req-123" in output
    assert "super-secret" not in output
    assert '"api_key":"[REDACTED]"' in output


def test_analyze_item_reraises_root_cause_after_retries(monkeypatch):
    class FakeHTTPError(Exception):
        pass

    attempts = 0

    async def fail_completion(**_kwargs):
        nonlocal attempts
        attempts += 1
        raise FakeHTTPError("HTTP 400")

    analyzer = ContentAnalyzer(SimpleNamespace(complete=fail_completion))
    monkeypatch.setattr(ContentAnalyzer._analyze_item.retry, "wait", wait_none())

    with pytest.raises(FakeHTTPError, match="HTTP 400"):
        asyncio.run(analyzer._analyze_item(_make_item("rss:test:failed")))

    assert attempts == 3


@pytest.mark.parametrize("response", ["{}", '{"score": "not-a-number"}', '{"score": 11}'])
def test_analyze_item_rejects_invalid_scoring_schema(monkeypatch, response):
    attempts = 0

    async def invalid_completion(**_kwargs):
        nonlocal attempts
        attempts += 1
        return response

    analyzer = ContentAnalyzer(SimpleNamespace(complete=invalid_completion))
    monkeypatch.setattr(ContentAnalyzer._analyze_item.retry, "wait", wait_none())

    with pytest.raises(ValueError, match="invalid analysis score"):
        asyncio.run(analyzer._analyze_item(_make_item("rss:test:invalid-schema")))

    assert attempts == 3


def test_scoring_failure_context_only_flags_more_than_half_failed():
    client = SimpleNamespace(
        config=SimpleNamespace(
            provider=SimpleNamespace(value="deepseek"),
            model="deepseek-chat",
        )
    )
    half_failed = [_make_item("ok"), _make_item("failed")]
    half_failed[0].metadata["analysis_status"] = "ok"
    half_failed[1].metadata["analysis_status"] = "failed"

    assert scoring_failure_context(half_failed, client) is None

    all_failed = [_make_item("failed-1"), _make_item("failed-2")]
    for item in all_failed:
        item.metadata["analysis_status"] = "failed"

    assert scoring_failure_context(all_failed, client) == {
        "success_count": 0,
        "failure_count": 2,
        "failure_rate": 1.0,
        "provider": "deepseek",
        "model": "deepseek-chat",
    }
