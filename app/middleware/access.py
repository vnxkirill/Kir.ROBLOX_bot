"""Контроль доступа: закрытое тестирование.

Сейчас бот отвечает только владельцу (BOT_OWNER_ID).
Когда проект откроется для всех — этот middleware заменяется
на систему ролей, остальной код не меняется.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject
from loguru import logger

_CLOSED_BETA_TEXT = "🚧 Проект находится в закрытом тестировании."


class OwnerOnlyMiddleware(BaseMiddleware):
    def __init__(self, owner_id: int) -> None:
        self._owner_id = owner_id

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = data.get("event_from_user")
        if user is None or user.id == self._owner_id:
            return await handler(event, data)

        logger.info("Отклонён не-владелец: id={} username={}", user.id, user.username)
        if isinstance(event, Message):
            await event.answer(_CLOSED_BETA_TEXT)
        elif isinstance(event, CallbackQuery):
            await event.answer(_CLOSED_BETA_TEXT, show_alert=True)
        return None
