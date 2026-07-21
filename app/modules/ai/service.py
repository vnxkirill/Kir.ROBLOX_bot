"""Сервис AI — бизнес-логика поверх абстрактного провайдера.

Здесь в будущем появятся: память диалогов, системные промпты,
выбор модели по задаче, лимиты. Провайдер остаётся тупым транспортом.
"""

from app.modules.ai.knowledge import SYSTEM_PROMPT
from app.modules.ai.provider import AIProvider
from app.schemas.ai import ChatMessage, ChatResponse


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    async def ask(self, question: str) -> ChatResponse:
        """Одиночный вопрос без истории диалога."""
        return await self.chat(question, history=[])

    async def chat(self, question: str, history: list[ChatMessage]) -> ChatResponse:
        """Вопрос с учётом истории диалога (история — без системного промпта)."""
        messages = [
            ChatMessage.system(SYSTEM_PROMPT),
            *history,
            ChatMessage.user(question),
        ]
        return await self._provider.chat(messages)
