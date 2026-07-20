"""Модуль Roblox: меню навыков, поиск UGC по официальному каталогу."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.handlers import router as roblox_router


class RobloxModule(AppModule):
    name = "roblox"

    def build_router(self, container: Container) -> Router | None:
        container.register(RobloxCatalogClient(container.http))
        return roblox_router
