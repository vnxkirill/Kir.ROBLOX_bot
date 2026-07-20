"""Корневой роутер приложения.

Собирает: обработчик ошибок → базовые хендлеры → роутеры модулей.
Порядок важен: модульные роутеры подключаются после базовых,
но до «catch-all» хендлеров, если такие появятся.
"""

from aiogram import Router

from app.handlers import errors, start


def build_root_router(module_routers: list[Router]) -> Router:
    root = Router(name="root")
    root.include_router(errors.router)
    root.include_router(start.router)
    for module_router in module_routers:
        root.include_router(module_router)
    return root
