"""Модуль FNF (Friday Night Funkin'). Пока заглушка."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule


class FnfModule(AppModule):
    name = "fnf"

    def build_router(self, container: Container) -> Router | None:
        return None
