"""AI client abstraction supporting multiple providers."""

import asyncio
import os
import re
from abc import ABC, abstractmethod
from typing import Optional
from openai import AsyncAzureOpenAI, AsyncOpenAI
from anthropic import AsyncAnthropic
from google import genai
from google.genai import types


from ..models import AIConfig, AIProvider
from .tokens import record_usage


_ENV_VAR_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_SECRET_PREFIXES = (
    "sk-",
    "sk_",
    "AIza",
    "xai-",
    "gsk_",
    "hf_",
)
_DEFAULT_API_KEY_ENVS = {
    AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
    AIProvider.OPENAI: "OPENAI_API_KEY",
    AIProvider.AZURE: "AZURE_OPENAI_API_KEY",
    AIProvider.ALI: "DASHSCOPE_API_KEY",
    AIProvider.GEMINI: "GOOGLE_API_KEY",
    AIProvider.DOUBAO: "DOUBAO_API_KEY",
    AIProvider.MINIMAX: "MINIMAX_API_KEY",
    AIProvider.DEEPSEEK: "DEEPSEEK_API_KEY",
}


def _resolve_api_key(config: AIConfig, *, fallback: Optional[str] = None) -> str:
    api_key = os.getenv(config.api_key_env)
    if api_key:
        return api_key
    if fallback is not None:
        return fallback
    raise ValueError(_missing_api_key_message(config))


def _missing_api_key_message(config: AIConfig) -> str:
    expected_env = _DEFAULT_API_KEY_ENVS.get(config.provider)
    if expected_env:
        setup_hint = (
            f"Set {expected_env}=your_api_key in .env or your shell, then set "
            f'ai.api_key_env to "{expected_env}" in data/config.json.'
        )
    else:
        setup_hint = (
            "Set the provider API key in .env or your shell, then set "
            "ai.api_key_env to that environment variable name in data/config.json."
        )

    if _looks_like_api_key_value(config.api_key_env):
        return (
            "Missing API key: ai.api_key_env must be an environment variable "
            f"name, not the API key value. {setup_hint}"
        )

    return (
        "Missing API key environment variable configured by ai.api_key_env. "
        "ai.api_key_env should contain the environment variable name, not the "
        f"key value. {setup_hint}"
    )


def _looks_like_api_key_value(value: str) -> bool:
    if value.startswith(_SECRET_PREFIXES):
        return True
    return not bool(_ENV_VAR_RE.fullmatch(value))


class AIClient(ABC):
    """Abstract base class for AI clients."""

    @abstractmethod
    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion from AI model.

        Args:
            system: System prompt
            user: User prompt
            temperature: Optional sampling temperature override
            max_tokens: Optional maximum tokens override

        Returns:
            str: Generated completion text
        """
        pass


class AnthropicClient(AIClient):
    """Client for Anthropic Claude models."""

    def __init__(self, config: AIConfig):
        """Initialize Anthropic client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)

        kwargs = {"api_key": api_key}
        if config.base_url:
            kwargs["base_url"] = config.base_url

        self.client = AsyncAnthropic(**kwargs)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Claude.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        message = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        usage = getattr(message, "usage", None)
        if usage is not None:
            record_usage(
                "anthropic",
                input_tokens=getattr(usage, "input_tokens", 0),
                output_tokens=getattr(usage, "output_tokens", 0),
            )
        return message.content[0].text


class OpenAIClient(AIClient):
    """Client for OpenAI-compatible APIs."""

    # Default base URLs per provider
    _DEFAULT_BASE_URLS = {
        "ali": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "deepseek": "https://api.deepseek.com",
        "doubao": "https://ark.cn-beijing.volces.com/api/v3",
        "minimax": "https://api.minimax.io/v1",
        "ollama": "http://localhost:11434/v1",
    }

    # Providers that don't support response_format
    _NO_RESPONSE_FORMAT = {"minimax"}

    # Providers that need temperature clamped to (0, 1]
    _TEMP_CLAMP = {"minimax"}

    def __init__(self, config: AIConfig):
        """Initialize OpenAI-compatible client.

        Args:
            config: AI configuration
        """
        self.config = config

        fallback = "no_key" if config.provider == AIProvider.OLLAMA else None
        api_key = _resolve_api_key(config, fallback=fallback)

        kwargs = {"api_key": api_key}
        base_url = config.base_url or self._DEFAULT_BASE_URLS.get(config.provider.value)
        if base_url:
            kwargs["base_url"] = base_url

        self.client = AsyncOpenAI(**kwargs)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        self.provider = config.provider.value
        # Some newer models (e.g. Claude Opus 4.7 on Bedrock Converse) reject
        # `temperature`. We learn this on first 400 and stop sending it.
        self._supports_temperature = True

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using OpenAI-compatible API.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        # Clamp temperature for providers that require it
        if self.provider in self._TEMP_CLAMP and temperature <= 0:
            temperature = 0.01

        try:
            response = await self._do_request(
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                include_temperature=self._supports_temperature,
            )
        except Exception as exc:
            if self._supports_temperature and self._is_temperature_unsupported(
                str(exc)
            ):
                self._supports_temperature = False
                response = await self._do_request(
                    system=system,
                    user=user,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    include_temperature=False,
                )
            else:
                raise
        usage = getattr(response, "usage", None)
        if usage is not None:
            record_usage(
                self.provider,
                input_tokens=getattr(usage, "prompt_tokens", 0),
                output_tokens=getattr(usage, "completion_tokens", 0),
            )
        return response.choices[0].message.content

    async def _do_request(
        self,
        *,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
        include_temperature: bool,
    ):
        request_kwargs = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "max_tokens": max_tokens,
        }
        if include_temperature:
            request_kwargs["temperature"] = temperature
        if self.provider not in self._NO_RESPONSE_FORMAT:
            request_kwargs["response_format"] = {"type": "json_object"}
        return await self.client.chat.completions.create(**request_kwargs)

    @staticmethod
    def _is_temperature_unsupported(message: str) -> bool:
        lowered = message.lower()
        return "temperature" in lowered and (
            "deprecated" in lowered
            or "not support" in lowered
            or "unsupported" in lowered
        )


class AzureOpenAIClient(AIClient):
    """Client for Azure OpenAI deployments.

    Uses the native AsyncAzureOpenAI client, which requires the deployment
    name (passed as `model`), azure_endpoint (resource base URL), and
    api_version. The deployment path is assembled internally by the SDK.
    """

    # Newer reasoning-series models reject legacy `max_tokens` and require
    # `max_completion_tokens` instead. Azure uses deployment names as `model`,
    # so a best-effort guess can be wrong for custom deployment aliases.
    _MODELS_REQUIRING_MAX_COMPLETION_TOKENS = ("o1", "o3", "o4", "gpt-5")

    def __init__(self, config: AIConfig):
        """Initialize Azure OpenAI client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)
        if not config.azure_endpoint_env:
            raise ValueError("azure_endpoint_env is required for azure provider")
        azure_endpoint = os.getenv(config.azure_endpoint_env)
        if not azure_endpoint:
            raise ValueError(f"Missing Azure endpoint: {config.azure_endpoint_env}")
        if not config.api_version:
            raise ValueError("api_version is required for azure provider")

        self.client = AsyncAzureOpenAI(
            api_key=api_key,
            azure_endpoint=azure_endpoint,
            api_version=config.api_version,
        )
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens
        self._use_max_completion_tokens = any(
            config.model.startswith(prefix)
            for prefix in self._MODELS_REQUIRING_MAX_COMPLETION_TOKENS
        )

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Azure OpenAI.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        try:
            response = await self._create_completion(
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                use_max_completion_tokens=self._use_max_completion_tokens,
            )
        except Exception as exc:
            fallback = self._token_fallback_mode(str(exc))
            if fallback is None:
                raise

            self._use_max_completion_tokens = fallback
            response = await self._create_completion(
                system=system,
                user=user,
                temperature=temperature,
                max_tokens=max_tokens,
                use_max_completion_tokens=fallback,
            )

        usage = getattr(response, "usage", None)
        if usage is not None:
            record_usage(
                "openai",
                input_tokens=getattr(usage, "prompt_tokens", 0),
                output_tokens=getattr(usage, "completion_tokens", 0),
            )
        return response.choices[0].message.content

    async def _create_completion(
        self,
        *,
        system: str,
        user: str,
        temperature: float,
        max_tokens: int,
        use_max_completion_tokens: bool,
    ):
        tokens_kwarg = (
            {"max_completion_tokens": max_tokens}
            if use_max_completion_tokens
            else {"max_tokens": max_tokens}
        )
        return await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=temperature,
            response_format={"type": "json_object"},
            **tokens_kwarg,
        )

    @staticmethod
    def _token_fallback_mode(message: str) -> Optional[bool]:
        lowered = message.lower()
        if "max_completion_tokens" in lowered and "max_tokens" in lowered:
            return True
        if "max_tokens" in lowered and "max_completion_tokens" not in lowered:
            return False
        return None


class GeminiClient(AIClient):
    """Client for Google Gemini models."""

    def __init__(self, config: AIConfig):
        """Initialize Gemini client.

        Args:
            config: AI configuration
        """
        self.config = config

        api_key = _resolve_api_key(config)

        self.client = genai.Client(api_key=api_key)
        self.model = config.model
        self.temperature = config.temperature
        self.max_tokens = config.max_tokens

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate completion using Gemini.

        Args:
            system: System prompt
            user: User prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            str: Generated text
        """
        temperature = self.temperature if temperature is None else temperature
        max_tokens = self.max_tokens if max_tokens is None else max_tokens

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=user,
            config=types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                max_output_tokens=max_tokens,
                response_mime_type="application/json"
            )
        )
        usage = getattr(response, "usage_metadata", None)
        if usage is not None:
            total = getattr(usage, "total_token_count", 0) or 0
            prompt = getattr(usage, "prompt_token_count", 0) or 0
            completion = max(0, total - prompt)
            record_usage("gemini", input_tokens=prompt, output_tokens=completion)
        return response.text


def create_ai_client(config: AIConfig) -> AIClient:
    """Factory function to create appropriate AI client.

    Args:
        config: AI configuration

    Returns:
        AIClient: Initialized AI client

    Raises:
        ValueError: If provider is not supported
    """
    # 2026-08-08: provider fallback chain. When config.fallbacks is non-
    # empty, wrap [config, *fallbacks] in FallbackAIClient so any 401/429/5xx
    # (quota/auth/provider-side failures) cascades to the next provider.
    # wrapper.config stays pointed at the primary config so analyzer/enricher
    # keep reading throttle/concurrency/prompt_overrides from the primary.
    if config.fallbacks:
        return FallbackAIClient([config, *config.fallbacks])

    if config.provider == AIProvider.ANTHROPIC:
        return AnthropicClient(config)
    elif config.provider == AIProvider.AZURE:
        return AzureOpenAIClient(config)
    elif config.provider == AIProvider.GEMINI:
        return GeminiClient(config)
    elif config.provider in {
        AIProvider.OPENAI,
        AIProvider.ALI,
        AIProvider.DOUBAO,
        AIProvider.MINIMAX,
        AIProvider.DEEPSEEK,
        AIProvider.OLLAMA,
    }:
        return OpenAIClient(config)
    else:
        raise ValueError(f"Unsupported AI provider: {config.provider}")
# 2026-11-04 fallback policy (user directive: DeepSeek is a PAID backup —
# only switch when MiniMax is completely unusable, never on a whim):
#   - 401/403 (auth/quota dead)          -> switch to the next provider at once
#   - 429 / 5xx / network & timeout      -> retry the SAME provider with
#     backoff; retries exhausted -> count toward a run-scoped circuit
#     breaker; only when the breaker trips (consecutive failures) does the
#     run move to the fallback. A single success resets the streak.
#   - 400 and other 4xx                  -> raise at once (schema/prompt
#     problem; it would fail identically everywhere).
_FALLBACK_STATUS_CODES = {401, 403}
_TRANSIENT_MAX_ATTEMPTS = 3            # 1 call + 2 retries
_TRANSIENT_BACKOFF_S = (2.0, 4.0)      # sleep before retry #1 / #2
_BREAKER_THRESHOLD = 5                 # consecutive exhausted calls


def _classify_failure(exc: BaseException) -> Optional[str]:
    """'auth' | 'transient' | None. Duck-typed on .status_code so the
    module keeps zero SDK error-class imports; None = not a provider
    failure at all (400 schema errors, local ValueErrors, ...)."""
    if isinstance(exc, (ValueError, TypeError, KeyError)):
        return None  # 本地逻辑错误，换谁都没用
    code = getattr(exc, "status_code", None)
    if code in _FALLBACK_STATUS_CODES:
        return "auth"
    if code == 400:
        return None
    if code is None or code == 429 or code >= 500:
        return "transient"
    return None


def _should_fallback(exc: BaseException) -> bool:
    """Backwards-compatible shim: True when the failure justifies moving
    off this provider (auth immediately; transient only after the caller
    exhausts its retries — callers should prefer _classify_failure)."""
    return _classify_failure(exc) is not None


class FallbackAIClient(AIClient):
    """Provider chain with a paid-backup-friendly switch policy.

    self.config points at the primary config so analyzer/enricher keep
    reading throttle_sec / analysis_concurrency / prompt_overrides from
    the primary. Switching to the (paid) fallback happens only when:
      - the primary fails auth/quota (401/403), or
      - the run-scoped breaker opens after _BREAKER_THRESHOLD consecutive
        transient failures (each retried _TRANSIENT_MAX_ATTEMPTS times).
    A single success resets the transient streak.
    """

    def __init__(self, configs):
        if not configs:
            raise ValueError("FallbackAIClient requires at least one config")
        self.config = configs[0]
        self._configs = list(configs)
        self._clients: list = [None] * len(configs)
        self._disabled_indices: set[int] = set()
        # 连续瞬态失败计数（仅对主 provider；成功即清零）
        self._transient_streak = 0

    @staticmethod
    def _build_one(config: AIConfig) -> AIClient:
        if config.provider == AIProvider.ANTHROPIC:
            return AnthropicClient(config)
        elif config.provider == AIProvider.AZURE:
            return AzureOpenAIClient(config)
        elif config.provider == AIProvider.GEMINI:
            return GeminiClient(config)
        elif config.provider in {
            AIProvider.OPENAI,
            AIProvider.ALI,
            AIProvider.DOUBAO,
            AIProvider.MINIMAX,
            AIProvider.DEEPSEEK,
            AIProvider.OLLAMA,
        }:
            return OpenAIClient(config)
        else:
            raise ValueError(f"Unsupported AI provider: {config.provider}")

    def _get_client(self, idx: int) -> AIClient:
        if self._clients[idx] is None:
            self._clients[idx] = self._build_one(self._configs[idx])
        return self._clients[idx]

    def _provider_str(self, idx: int) -> str:
        provider = getattr(self._configs[idx], "provider", "?")
        return provider.value if hasattr(provider, "value") else str(provider)

    async def complete(
        self,
        system: str,
        user: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        last_exc: Optional[BaseException] = None
        last_provider: Optional[str] = None
        for idx in range(len(self._configs)):
            if idx in self._disabled_indices:
                continue
            try:
                client = self._get_client(idx)
            except Exception as e:
                # Build-time failure (e.g. missing API key) — skippable.
                self._disabled_indices.add(idx)
                last_exc, last_provider = e, self._provider_str(idx)
                print(
                    f"[ai_fallback] {last_provider} build failed "
                    f"({type(e).__name__}: {e}) — trying next provider"
                )
                continue

            for attempt in range(_TRANSIENT_MAX_ATTEMPTS):
                try:
                    out = await client.complete(system, user, temperature, max_tokens)
                    if idx == 0:
                        self._transient_streak = 0
                    return out
                except Exception as e:
                    kind = _classify_failure(e)
                    if kind is None:
                        raise  # 400/本地错误：换谁都没用
                    last_exc, last_provider = e, self._provider_str(idx)
                    if kind == "auth":
                        self._disabled_indices.add(idx)
                        print(
                            f"[ai_fallback] {last_provider} auth/quota dead "
                            f"(status={getattr(e, 'status_code', '?')}) — "
                            f"switching to next provider for this run"
                        )
                        break  # 下一个 provider
                    # transient：先重试
                    if attempt + 1 < _TRANSIENT_MAX_ATTEMPTS:
                        await asyncio.sleep(
                            _TRANSIENT_BACKOFF_S[min(attempt, len(_TRANSIENT_BACKOFF_S) - 1)]
                        )
                        continue
                    # 重试耗尽
                    if idx == 0:
                        self._transient_streak += 1
                        if self._transient_streak >= _BREAKER_THRESHOLD:
                            self._disabled_indices.add(idx)
                            print(
                                f"[ai_fallback] {last_provider} unavailable "
                                f"{self._transient_streak} consecutive calls — "
                                f"circuit open, switching to next provider "
                                f"for this run"
                            )
                            break  # 本次调用由 fallback 接管
                        raise
                    raise  # 备胎自己也瞬态失败：如实上抛
        if last_exc is None:
            raise RuntimeError("All AI providers are disabled for this run")
        print(f"[ai_fallback] all providers exhausted (last={last_provider})")
        raise last_exc
