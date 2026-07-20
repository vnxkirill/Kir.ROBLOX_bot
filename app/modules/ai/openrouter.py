"""Реализация AIProvider поверх OpenRouter (OpenAI-совместимый API)."""

from typing import Any

import aiohttp
from loguru import logger

from app.config import OpenRouterSettings
from app.core.exceptions import ExternalServiceError
from app.schemas.ai import ChatMessage, ChatResponse, ChatUsage


class OpenRouterProvider:
    """AIProvider, работающий через https://openrouter.ai."""

    def __init__(self, settings: OpenRouterSettings, http: aiohttp.ClientSession) -> None:
        self._settings = settings
        self._http = http

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        payload: dict[str, Any] = {
            "model": model or self._settings.model,
            "messages": [m.model_dump(mode="json") for m in messages],
            "temperature": temperature,
        }
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens

        try:
            async with self._http.post(
                f"{self._settings.base_url}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {self._settings.api_key.get_secret_value()}",
                },
                timeout=aiohttp.ClientTimeout(total=self._settings.timeout_seconds),
            ) as response:
                body = await response.json()
                if response.status != 200:
                    logger.error("OpenRouter HTTP {}: {}", response.status, body)
                    raise ExternalServiceError(f"OpenRouter вернул HTTP {response.status}")
        except aiohttp.ClientError as exc:
            logger.error("Сетевая ошибка OpenRouter: {}", exc)
            raise ExternalServiceError("Сетевая ошибка при обращении к OpenRouter") from exc

        return self._parse_response(body)

    @staticmethod
    def _parse_response(body: dict[str, Any]) -> ChatResponse:
        try:
            choice = body["choices"][0]
            usage = body.get("usage") or {}
            return ChatResponse(
                content=choice["message"]["content"],
                model=body.get("model", ""),
                usage=ChatUsage(
                    prompt_tokens=usage.get("prompt_tokens", 0),
                    completion_tokens=usage.get("completion_tokens", 0),
                    total_tokens=usage.get("total_tokens", 0),
                ),
            )
        except (KeyError, IndexError, TypeError) as exc:
            logger.error("Неожиданный формат ответа OpenRouter: {}", body)
            raise ExternalServiceError("Неожиданный формат ответа OpenRouter") from exc
