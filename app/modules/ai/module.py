"""Модуль AI: регистрирует провайдер и сервис в контейнере."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.ai.openrouter import OpenRouterProvider
from app.modules.ai.provider import AIProvider
from app.modules.ai.service import AIService


class AIModule(AppModule):
    name = "ai"

    def build_router(self, container: Container) -> Router | None:
        provider = OpenRouterProvider(container.settings.openrouter, container.http)
        container.register(provider, as_type=AIProvider)  # type: ignore[type-abstract]
        container.register(AIService(provider))
        # Telegram-хендлеры AI появятся позже — сейчас только сервисы.
        return None
