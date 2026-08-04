"""Модуль «Игры»: площадка мини-игр (Telegram Mini App)."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.games.handlers import router as games_router


class GamesModule(AppModule):
    name = "games"

    def build_router(self, container: Container) -> Router | None:
        return games_router
