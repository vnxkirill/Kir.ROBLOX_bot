"""Модуль Roblox: меню навыков, поиск UGC, доска «Ищу друзей»."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.friends import friends_router
from app.modules.roblox.handlers import router as roblox_router


class RobloxModule(AppModule):
    name = "roblox"

    def build_router(self, container: Container) -> Router | None:
        container.register(RobloxCatalogClient(container.http))
        # friends_router — раньше основного: перехватывает навык FRIENDS
        # до общего обработчика-заглушки в handlers.py.
        friends_router.include_router(roblox_router)
        return friends_router
