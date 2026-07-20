"""Модуль профиля: память пользователя, достижения. Пока заглушка."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule


class ProfileModule(AppModule):
    name = "profile"

    def build_router(self, container: Container) -> Router | None:
        return None
