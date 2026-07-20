"""Создание асинхронного движка БД и фабрики сессий."""

from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import DatabaseSettings


def create_engine_and_factory(
    settings: DatabaseSettings,
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """Создать движок и фабрику сессий по настройкам БД."""
    engine = create_async_engine(settings.url, echo=settings.echo)

    if settings.url.startswith("sqlite"):
        _enable_sqlite_pragmas(engine)

    factory = async_sessionmaker(engine, expire_on_commit=False)
    return engine, factory


def _enable_sqlite_pragmas(engine: AsyncEngine) -> None:
    """WAL и foreign_keys для SQLite: конкурентность и целостность ссылок."""

    @event.listens_for(engine.sync_engine, "connect")
    def _on_connect(dbapi_connection, _record) -> None:  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
