"""Модуль Roblox: поиск UGC, анализ аккаунтов, новости. Пока заглушка."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule


class RobloxModule(AppModule):
    name = "roblox"

    def build_router(self, container: Container) -> Router | None:
        return None
