"""Точка входа GameCore AI — composition root.

Единственное место, где всё собирается вместе: настройки, логирование,
БД, HTTP-клиент, контейнер, модули, middleware и диспетчер.
"""

import asyncio

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from loguru import logger

from app.config import get_settings
from app.core.container import Container
from app.core.logging import setup_logging
from app.database import create_engine_and_factory
from app.middleware import (
    ContainerMiddleware,
    DatabaseMiddleware,
    LoggingMiddleware,
    OwnerOnlyMiddleware,
)
from app.modules.registry import get_modules
from app.routers import build_root_router

# Команды в кнопке «Меню» слева от поля ввода.
_BOT_COMMANDS = [
    BotCommand(command="start", description="🏠 Запустить бота"),
    BotCommand(command="menu", description="📋 Главное меню"),
    BotCommand(command="ai", description="🤖 AI-чат"),
]


async def main() -> None:
    settings = get_settings()
    setup_logging(settings)
    logger.info("Запуск GameCore AI…")

    engine, session_factory = create_engine_and_factory(settings.database)

    async with aiohttp.ClientSession() as http:
        container = Container(settings, engine, session_factory, http)

        # Модули: регистрация сервисов и сбор роутеров.
        modules = get_modules()
        module_routers = []
        for module in modules:
            router = module.build_router(container)
            if router is not None:
                module_routers.append(router)
            logger.info("Модуль подключён: {}", module.name)

        bot = Bot(
            token=settings.bot.token.get_secret_value(),
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        dp = Dispatcher()

        # Порядок middleware важен: логирование → доступ → контейнер → БД.
        dp.update.outer_middleware(LoggingMiddleware())
        dp.update.outer_middleware(OwnerOnlyMiddleware(settings.bot.owner_id))
        dp.update.middleware(ContainerMiddleware(container))
        dp.update.middleware(DatabaseMiddleware(session_factory))

        dp.include_router(build_root_router(module_routers))

        for module in modules:
            await module.on_startup(container)

        await bot.set_my_commands(_BOT_COMMANDS)

        try:
            logger.info("Бот запущен, начинаю polling")
            await dp.start_polling(bot)
        finally:
            for module in modules:
                await module.on_shutdown(container)
            await engine.dispose()
            logger.info("GameCore AI остановлен")


if __name__ == "__main__":
    asyncio.run(main())
