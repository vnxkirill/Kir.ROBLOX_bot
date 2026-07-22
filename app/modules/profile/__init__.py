"""Модуль профиля: ввод ника, память пользователя, достижения."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.profile.handlers import router as profile_router


class ProfileModule(AppModule):
    name = "profile"

    def build_router(self, container: Container) -> Router | None:
        return profile_router
