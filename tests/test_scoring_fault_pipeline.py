import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

from scripts.push_hiboard_daily import build_digest
from src.ai.analyzer import ContentAnalyzer, scoring_failure_context
from src.ai.summarizer import DailySummarizer
from src.models import ContentItem, SourceType


def test_all_scoring_requests_fail_logs_marks_report_and_alerts(monkeypatch, capsys):
    client = SimpleNamespace(
        config=SimpleNamespace(
            provider=SimpleNamespace(value="deepseek"),
            model="deepseek-chat",
        )
    )
    analyzer = ContentAnalyzer(client)
    items = [
        ContentItem(
            id=f"rss:dead:{index}",
            source_type=SourceType.RSS,
            title=f"Dead item {index}",
            url=f"https://example.com/{index}",
            published_at=datetime(2026, 7, 28, tzinfo=timezone.utc),
        )
        for index in range(3)
    ]

    async def fail_item(_item):
        raise RuntimeError("HTTP 503 upstream unavailable token=top-secret")

    monkeypatch.setattr(analyzer, "_analyze_item", fail_item)
    analyzed = asyncio.run(analyzer.analyze_batch(items))
    failure = scoring_failure_context(analyzed, client)
    summary = asyncio.run(
        DailySummarizer().generate_summary(
            [],
            "2026-07-28",
            len(items),
            language="zh",
            scoring_failure=failure,
        )
    )
    _, card_content, card_result = build_digest("2026-07-28", summary)
    log = capsys.readouterr().out

    assert "analysis_batch success=0 failure=3" in log
    assert "top-secret" not in log
    assert summary.startswith("# 【评分故障空报】")
    assert "【评分故障空报】" in card_content
    assert card_result == "生成失败：评分服务异常"
