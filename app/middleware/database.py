"""Сессия БД на каждое обновление.

Открывает AsyncSession, кладёт её в data["db"], коммитит при успехе
и откатывает при ошибке — паттерн unit-of-work на один апдейт.
Хендлерам не нужно управлять транзакциями вручную.
"""

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self._session_factory() as session:
            data["db"] = session
            result = await handler(event, data)
            await session.commit()
            return result
