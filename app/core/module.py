"""Система модулей.

Каждая крупная возможность (AI, Roblox, профиль, экономика…) — это модуль:
самодостаточный пакет со своими handlers, сервисами и жизненным циклом.
Ядро приложения ничего не знает о содержимом модулей — оно лишь
вызывает их хуки и подключает их роутеры.

Добавление новой возможности = новый пакет в app/modules + одна строка
в списке регистрации. Ядро не меняется.
"""

from abc import ABC, abstractmethod

from aiogram import Router

from app.core.container import Container


class AppModule(ABC):
    """Базовый класс модуля приложения."""

    name: str
    """Уникальное имя модуля (для логов и диагностики)."""

    @abstractmethod
    def build_router(self, container: Container) -> Router | None:
        """Создать роутер модуля. None — если у модуля нет Telegram-хендлеров."""

    async def on_startup(self, container: Container) -> None:  # noqa: B027
        """Хук запуска: открыть соединения, прогреть кеши. По умолчанию — ничего."""

    async def on_shutdown(self, container: Container) -> None:  # noqa: B027
        """Хук остановки: закрыть ресурсы. По умолчанию — ничего."""
