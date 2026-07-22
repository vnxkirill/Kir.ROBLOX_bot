"""Репозиторий объявлений «ищу друзей»."""

from sqlalchemy import select

from app.models import FriendListing
from app.repositories.base import BaseRepository


class FriendListingRepository(BaseRepository[FriendListing]):
    model = FriendListing

    async def list_all(self, limit: int = 50) -> list[FriendListing]:
        """Все объявления, новые сверху."""
        stmt = select(FriendListing).order_by(FriendListing.created_at.desc()).limit(limit)
        return list(await self._session.scalars(stmt))

    async def get_by_telegram_id(self, telegram_id: int) -> FriendListing | None:
        stmt = select(FriendListing).where(FriendListing.telegram_id == telegram_id)
        return await self._session.scalar(stmt)

    async def upsert(
        self, telegram_id: int, roblox_user_id: int, roblox_username: str
    ) -> FriendListing:
        """Добавить или обновить объявление пользователя (одно на человека)."""
        listing = await self.get_by_telegram_id(telegram_id)
        if listing is None:
            listing = self.add(
                FriendListing(
                    telegram_id=telegram_id,
                    roblox_user_id=roblox_user_id,
                    roblox_username=roblox_username,
                )
            )
        else:
            listing.roblox_user_id = roblox_user_id
            listing.roblox_username = roblox_username
        return listing

    async def remove(self, telegram_id: int) -> bool:
        """Удалить объявление пользователя. True — если было что удалять."""
        listing = await self.get_by_telegram_id(telegram_id)
        if listing is None:
            return False
        await self.delete(listing)
        return True
