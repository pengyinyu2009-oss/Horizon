from scripts.push_hiboard_daily import build_alert, build_digest


def test_build_digest_distinguishes_scoring_fault_from_valid_zero_selection():
    scoring_fault_md = """# 【评分故障空报】Horizon 每日简报 - 2026-07-28

> 评分服务故障：共抓取 12 条，评分成功 0 条，失败 12 条（失败率 100.0%）。

⚠️ 生成失败：评分服务异常。本页仅用于故障告警，不代表今日无重要动态。
"""
    valid_zero_md = """# Horizon 每日简报 - 2026-07-28

> 已分析 12 条内容，但没有达到重要性阈值的条目。
"""

    fault_name, fault_content, fault_result = build_digest(
        "2026-07-28", scoring_fault_md
    )
    zero_name, zero_content, zero_result = build_digest(
        "2026-07-28", valid_zero_md
    )

    assert fault_name == "⚠️ Horizon 评分故障 · 2026-07-28"
    assert "【评分故障空报】" in fault_content
    assert fault_result == "生成失败：评分服务异常"
    assert zero_name == "Horizon 每日日报 · 2026-07-28"
    assert "有效分析后零入选" in zero_content
    assert zero_result == "已生成 · 0 条入选（有效分析零入选）"


def test_build_alert_supports_publish_lineage_failures():
    name, content, result = build_alert(
        "2026-07-28",
        "血缘自检未达 100%，latest 保留旧页面。",
        "生成失败：血缘自检异常",
    )

    assert name == "⚠️ Horizon 发布告警 · 2026-07-28"
    assert "血缘自检未达 100%" in content
    assert result == "生成失败：血缘自检异常"
