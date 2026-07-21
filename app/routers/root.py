"""Корневой роутер приложения.

Собирает: обработчик ошибок → базовые хендлеры → роутеры модулей →
fallback (AI-чат на любой текст). Порядок критичен: fallback ловит
всё, что не обработали разделы, поэтому он строго последний.
"""

from aiogram import Router

from app.handlers import errors, start
from app.modules.ai.fallback import fallback_router


def build_root_router(module_routers: list[Router]) -> Router:
    root = Router(name="root")
    root.include_router(errors.router)
    root.include_router(start.router)
    for module_router in module_routers:
        root.include_router(module_router)
    root.include_router(fallback_router)
    return root
