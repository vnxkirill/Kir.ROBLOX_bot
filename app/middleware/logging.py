"""Логирование входящих обновлений и времени обработки."""

import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update
from loguru import logger


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        started = time.monotonic()
        event_type = event.event_type if isinstance(event, Update) else type(event).__name__
        try:
            return await handler(event, data)
        finally:
            elapsed_ms = (time.monotonic() - started) * 1000
            logger.debug("Обработан {} за {:.1f} мс", event_type, elapsed_ms)
