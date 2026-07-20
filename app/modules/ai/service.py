"""Сервис AI — бизнес-логика поверх абстрактного провайдера.

Здесь в будущем появятся: память диалогов, системные промпты,
выбор модели по задаче, лимиты. Провайдер остаётся тупым транспортом.
"""

from app.modules.ai.provider import AIProvider
from app.schemas.ai import ChatMessage, ChatResponse

_SYSTEM_PROMPT = (
    "Ты — GameCore AI, дружелюбный персональный игровой ассистент. "
    "Отвечай кратко и по делу, на языке пользователя."
)


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    async def ask(self, question: str) -> ChatResponse:
        """Одиночный вопрос без истории диалога."""
        messages = [
            ChatMessage.system(_SYSTEM_PROMPT),
            ChatMessage.user(question),
        ]
        return await self._provider.chat(messages)
