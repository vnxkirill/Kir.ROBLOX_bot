"""Модуль сообщества. Пока заглушка."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule


class CommunityModule(AppModule):
    name = "community"

    def build_router(self, container: Container) -> Router | None:
        return None
