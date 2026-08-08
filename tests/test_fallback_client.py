"""Tests for FallbackAIClient (provider fallback chain on 401/429/5xx)."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.ai.client import (
    FallbackAIClient,
    OpenAIClient,
    _should_fallback,
    create_ai_client,
)
from src.models import AIConfig, AIProvider


def _make_primary(**overrides) -> AIConfig:
    defaults = {
        "provider": AIProvider.MINIMAX,
        "model": "MiniMax-M3",
        "api_key_env": "MINIMAX_API_KEY",
        "temperature": 0.3,
        "max_tokens": 4096,
    }
    defaults.update(overrides)
    return AIConfig(**defaults)


def _make_deepseek_fallback() -> dict:
    return {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "api_key_env": "DEEPSEEK_API_KEY",
        "temperature": 0.3,
        "max_tokens": 4096,
    }


class _StatusError(Exception):
    """Duck-typed stand-in for openai.APIStatusError family."""

    def __init__(self, status_code: int, msg: str = "err"):
        super().__init__(msg)
        self.status_code = status_code


def _ok_response(text: str = '{"ok": true}') -> MagicMock:
    r = MagicMock()
    r.choices = [MagicMock()]
    r.choices[0].message.content = text
    r.usage.prompt_tokens = 5
    r.usage.completion_tokens = 3
    return r


class TestShouldFallback:
    def test_401_triggers(self):
        assert _should_fallback(_StatusError(401))

    def test_429_triggers(self):
        assert _should_fallback(_StatusError(429))

    @pytest.mark.parametrize("code", [500, 502, 503, 504])
    def test_5xx_triggers(self, code):
        assert _should_fallback(_StatusError(code))

    @pytest.mark.parametrize("code", [400, 403, 404])
    def test_4xx_others_do_not(self, code):
        assert not _should_fallback(_StatusError(code))

    def test_no_status_code_does_not(self):
        assert not _should_fallback(RuntimeError("boom"))
        assert not _should_fallback(TimeoutError("slow"))

    def test_value_error_missing_key_does_not(self):
        # _resolve_api_key raises ValueError("Missing API key ...") with no status_code
        assert not _should_fallback(ValueError("Missing API key environment variable"))


class TestFactoryDispatch:
    def test_no_fallbacks_returns_plain_client(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        c = create_ai_client(_make_primary())
        assert isinstance(c, OpenAIClient)
        assert not isinstance(c, FallbackAIClient)
        assert c.config.provider == AIProvider.MINIMAX

    def test_with_fallbacks_returns_wrapper(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))
        assert isinstance(c, FallbackAIClient)
        assert c.config.provider == AIProvider.MINIMAX
        assert len(c._clients) == 2
        assert c._clients[0].config.provider == AIProvider.MINIMAX
        assert c._clients[1].config.provider == AIProvider.DEEPSEEK

    def test_wrapper_config_is_primary(self, monkeypatch):
        """Downstream code reads client.config.throttle_sec / prompt_overrides
        from the primary — make sure wrapper.config is the primary config."""
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(
            _make_primary(
                fallbacks=[_make_deepseek_fallback()],
                throttle_sec=4.5,
                analysis_concurrency=8,
                prompt_overrides={"analysis_system": "x"},
            )
        )
        assert c.config.throttle_sec == 4.5
        assert c.config.analysis_concurrency == 8
        assert c.config.prompt_overrides == {"analysis_system": "x"}


class TestFallbackBehaviour:
    def test_primary_401_then_fallback_succeeds(self, monkeypatch, capsys):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))

        with patch.object(
            c._clients[0].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_primary, patch.object(
            c._clients[1].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_backup:
            m_primary.side_effect = _StatusError(401, "quota")
            m_backup.return_value = _ok_response('{"from": "deepseek"}')

            out = asyncio.run(c.complete(system="s", user="u"))
            assert "deepseek" in out
            assert m_primary.call_count == 1
            assert m_backup.call_count == 1

        captured = capsys.readouterr().out
        assert "[ai_fallback]" in captured
        assert "401" in captured

    def test_primary_429_then_fallback_succeeds(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))

        with patch.object(
            c._clients[0].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_primary, patch.object(
            c._clients[1].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_backup:
            m_primary.side_effect = _StatusError(429, "rate")
            m_backup.return_value = _ok_response('{"from": "deepseek"}')
            out = asyncio.run(c.complete(system="s", user="u"))
            assert "deepseek" in out

    def test_400_does_not_fallback(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))

        with patch.object(
            c._clients[0].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_primary, patch.object(
            c._clients[1].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_backup:
            m_primary.side_effect = _StatusError(400, "bad prompt")
            with pytest.raises(_StatusError) as exc:
                asyncio.run(c.complete(system="s", user="u"))
            assert exc.value.status_code == 400
            assert m_backup.call_count == 0

    def test_all_providers_exhausted_raises_last(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))

        with patch.object(
            c._clients[0].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_primary, patch.object(
            c._clients[1].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_backup:
            m_primary.side_effect = _StatusError(401, "quota")
            m_backup.side_effect = _StatusError(503, "deepseek down")
            with pytest.raises(_StatusError) as exc:
                asyncio.run(c.complete(system="s", user="u"))
            assert exc.value.status_code == 503  # last error bubbles up
            assert m_primary.call_count == 1
            assert m_backup.call_count == 1

    def test_primary_success_never_touches_fallback(self, monkeypatch):
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        c = create_ai_client(_make_primary(fallbacks=[_make_deepseek_fallback()]))

        with patch.object(
            c._clients[0].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_primary, patch.object(
            c._clients[1].client.chat.completions, "create", new_callable=AsyncMock
        ) as m_backup:
            m_primary.return_value = _ok_response('{"from": "minimax"}')
            out = asyncio.run(c.complete(system="s", user="u"))
            assert "minimax" in out
            assert m_backup.call_count == 0

    def test_nested_fallback_config_does_not_recurse(self, monkeypatch):
        """If a sub-config also declares fallbacks, its _build_one call must
        NOT route through create_ai_client again (would infinitely nest)."""
        monkeypatch.setenv("MINIMAX_API_KEY", "k")
        monkeypatch.setenv("DEEPSEEK_API_KEY", "d")
        inner = {
            "provider": "deepseek",
            "model": "deepseek-chat",
            "api_key_env": "DEEPSEEK_API_KEY",
            "fallbacks": [
                {"provider": "minimax", "model": "x", "api_key_env": "MINIMAX_API_KEY"}
            ],
        }
        c = create_ai_client(_make_primary(fallbacks=[inner]))
        # children are built via _build_one, not the public factory, so the
        # inner fallbacks field is ignored — chain is [minimax, deepseek].
        assert len(c._clients) == 2
        assert isinstance(c._clients[1], OpenAIClient)
        assert c._clients[1].config.provider == AIProvider.DEEPSEEK
