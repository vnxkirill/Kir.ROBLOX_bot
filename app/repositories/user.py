"""Репозиторий пользователей."""

from sqlalchemy import select

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        stmt = select(User).where(User.telegram_id == telegram_id)
        return await self._session.scalar(stmt)

    async def get_or_create(
        self,
        telegram_id: int,
        *,
        username: str | None = None,
        first_name: str | None = None,
        language_code: str | None = None,
    ) -> User:
        """Найти пользователя или создать нового, обновив известные поля."""
        user = await self.get_by_telegram_id(telegram_id)
        if user is None:
            user = self.add(
                User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    language_code=language_code,
                )
            )
        else:
            user.username = username
            user.first_name = first_name
            user.language_code = language_code
        return user

    async def set_nickname(
        self, telegram_id: int, nickname: str, roblox_user_id: int | None = None
    ) -> User:
        """Сохранить Roblox-ник пользователя (создаёт запись, если её ещё нет)."""
        user = await self.get_or_create(telegram_id)
        user.nickname = nickname
        user.roblox_user_id = roblox_user_id
        return user
