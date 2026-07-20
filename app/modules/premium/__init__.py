"""Модуль premium: экономика, подписки. Пока заглушка."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule


class PremiumModule(AppModule):
    name = "premium"

    def build_router(self, container: Container) -> Router | None:
        return None
