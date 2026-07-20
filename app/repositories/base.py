"""Базовый репозиторий.

Репозиторий — единственный слой, который пишет SQL/ORM-запросы.
Сервисы работают с репозиториями и не знают про SQLAlchemy,
поэтому смену СУБД или схемы переживает только этот слой.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base


class BaseRepository[ModelT: Base]:
    """Общие CRUD-операции для одной модели."""

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get(self, id_: int) -> ModelT | None:
        return await self._session.get(self.model, id_)

    def add(self, instance: ModelT) -> ModelT:
        self._session.add(instance)
        return instance

    async def delete(self, instance: ModelT) -> None:
        await self._session.delete(instance)
