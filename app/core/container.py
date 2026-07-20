"""Контейнер зависимостей (Dependency Injection).

Простой явный контейнер вместо тяжёлого DI-фреймворка: все зависимости
создаются в одном месте (composition root — app/main.py), передаются
явно и легко подменяются в тестах.

Сервисы регистрируются по своему типу и достаются через container.get(Тип),
поэтому модули не знают, КАК создаётся сервис, — только его интерфейс.
"""

from typing import TypeVar

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker

from app.config import Settings

T = TypeVar("T")


class Container:
    """Держатель зависимостей приложения."""

    def __init__(
        self,
        settings: Settings,
        engine: AsyncEngine,
        session_factory: async_sessionmaker,
        http: ClientSession,
    ) -> None:
        self.settings = settings
        self.engine = engine
        self.session_factory = session_factory
        self.http = http
        self._services: dict[type, object] = {}

    def register(self, instance: object, *, as_type: type | None = None) -> None:
        """Зарегистрировать сервис. По умолчанию — по его собственному типу."""
        key = as_type or type(instance)
        if key in self._services:
            raise RuntimeError(f"Сервис {key.__name__} уже зарегистрирован")
        self._services[key] = instance

    def get(self, service_type: type[T]) -> T:
        """Получить сервис по типу (включая базовый класс/протокол)."""
        service = self._services.get(service_type)
        if service is None:
            raise RuntimeError(f"Сервис {service_type.__name__} не зарегистрирован")
        return service  # type: ignore[return-value]
