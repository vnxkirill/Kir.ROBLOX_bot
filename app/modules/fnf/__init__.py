"""Модуль FNF (Friday Night Funkin'): ссылки на моды GameJolt."""

from aiogram import Router

from app.core.container import Container
from app.core.module import AppModule
from app.modules.fnf.handlers import router as fnf_router


class FnfModule(AppModule):
    name = "fnf"

    def build_router(self, container: Container) -> Router | None:
        return fnf_router
