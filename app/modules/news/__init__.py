"""Модуль «Новости»: свежие анонсы Roblox из официальной RSS-ленты."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.news.api import RobloxNewsClient
from app.modules.news.handlers import router as news_router


class NewsModule(AppModule):
    name = "news"

    def build_router(self, container: Container) -> Router | None:
        container.register(RobloxNewsClient(container.http))
        return news_router
