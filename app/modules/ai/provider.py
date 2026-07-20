"""Абстракция AI-провайдера.

Остальной проект зависит ТОЛЬКО от этого интерфейса и схем.
OpenRouter — лишь одна из реализаций; замена провайдера
не затрагивает ни сервисы, ни хендлеры.
"""

from typing import Protocol

from app.schemas.ai import ChatMessage, ChatResponse


class AIProvider(Protocol):
    """Любой поставщик языковой модели."""

    async def chat(
        self,
        messages: list[ChatMessage],
        *,
        model: str | None = None,
        temperature: float = 0.7,
        max_tokens: int | None = None,
    ) -> ChatResponse:
        """Выполнить чат-запрос и вернуть ответ модели."""
        ...
