"""Глобальная обработка ошибок.

Последний рубеж: ни одно исключение не роняет процесс и не остаётся
без ответа пользователю. Ошибки домена (AppError) показывают своё
user_message, всё остальное — общий текст + полный трейсбек в лог.
"""

from aiogram import Router
from aiogram.types import ErrorEvent
from loguru import logger

from app.core.exceptions import AppError

router = Router(name="errors")

_UNEXPECTED_TEXT = "⚠️ Произошла непредвиденная ошибка. Мы уже разбираемся."


@router.error()
async def handle_error(event: ErrorEvent) -> bool:
    exception = event.exception

    if isinstance(exception, AppError):
        logger.warning("Ошибка домена: {}", exception)
        user_text = exception.user_message
    else:
        logger.opt(exception=exception).error("Необработанное исключение")
        user_text = _UNEXPECTED_TEXT

    message = event.update.message or (
        event.update.callback_query.message if event.update.callback_query else None
    )
    if message:
        try:
            await message.answer(user_text)
        except Exception:  # noqa: BLE001 — отправка ответа не должна ронять обработчик
            logger.exception("Не удалось отправить сообщение об ошибке")
    return True
