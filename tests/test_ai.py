"""Тесты AI-слоя: парсинг ответа OpenRouter и работа сервиса с фейковым провайдером."""

import pytest

from app.core.exceptions import ExternalServiceError
from app.modules.ai.openrouter import OpenRouterProvider
from app.modules.ai.service import AIService
from app.schemas.ai import ChatMessage, ChatResponse, ChatRole


def test_parse_valid_response() -> None:
    body = {
        "model": "openai/gpt-4o-mini",
        "choices": [{"message": {"role": "assistant", "content": "Привет!"}}],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
    }
    response = OpenRouterProvider._parse_response(body)
    assert response.content == "Привет!"
    assert response.usage.total_tokens == 15


def test_parse_malformed_response_raises() -> None:
    with pytest.raises(ExternalServiceError):
        OpenRouterProvider._parse_response({"choices": []})


class _FakeProvider:
    """Фейковый AIProvider — доказывает, что сервис не привязан к OpenRouter."""

    def __init__(self) -> None:
        self.received: list[ChatMessage] = []

    async def chat(self, messages, *, model=None, temperature=0.7, max_tokens=None):
        self.received = messages
        return ChatResponse(content="ответ", model="fake")


async def test_ai_service_uses_provider() -> None:
    provider = _FakeProvider()
    service = AIService(provider)

    response = await service.ask("вопрос")

    assert response.content == "ответ"
    assert provider.received[0].role == ChatRole.SYSTEM
    assert provider.received[1] == ChatMessage.user("вопрос")
