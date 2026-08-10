import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
MAINLAND_MINIMAX_BASE_URL = "https://api.minimaxi.com/v1"
PRODUCTION_CONFIGS = (
    "config.github.json",
    "config.global.json",
    "config.github-trending.json",
    "config.ee.json",
)


@pytest.mark.parametrize("config_name", PRODUCTION_CONFIGS)
def test_production_minimax_configs_use_mainland_endpoint(config_name: str):
    config_path = REPO_ROOT / "data" / config_name
    ai_config = json.loads(config_path.read_text(encoding="utf-8"))["ai"]

    assert ai_config["provider"] == "minimax"
    assert ai_config.get("base_url") == MAINLAND_MINIMAX_BASE_URL
