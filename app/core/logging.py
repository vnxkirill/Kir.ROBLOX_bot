"""Настройка логирования через Loguru.

Стандартный logging (в т.ч. aiogram и SQLAlchemy) перехватывается
и направляется в Loguru — весь вывод в одном формате и одном месте.
"""

import inspect
import logging
import sys

from loguru import logger

from app.config import Settings


class _InterceptHandler(logging.Handler):
    """Мост stdlib logging → Loguru (рецепт из документации Loguru)."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Ищем реальный фрейм вызова, чтобы в логе было верное место.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging(settings: Settings) -> None:
    """Настроить логирование всего приложения. Вызывается один раз при старте."""
    logger.remove()

    logger.add(
        sys.stderr,
        level=settings.log.level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
    )

    settings.log.dir.mkdir(parents=True, exist_ok=True)
    logger.add(
        settings.log.dir / "gamecore_{time:YYYY-MM-DD}.log",
        level=settings.log.level,
        rotation=settings.log.rotation,
        retention=settings.log.retention,
        encoding="utf-8",
        enqueue=True,  # безопасно из async-кода
    )

    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)
