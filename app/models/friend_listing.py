"""Объявление «ищу друзей»: привязка Telegram-пользователя к его Roblox-нику.

Один пользователь — одно объявление (upsert по telegram_id).
Список объявлений общий: его видят все пользователи бота.
"""

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class FriendListing(Base, TimestampMixin):
    __tablename__ = "friend_listings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    roblox_user_id: Mapped[int] = mapped_column(BigInteger)
    roblox_username: Mapped[str]

    @property
    def profile_url(self) -> str:
        return f"https://www.roblox.com/users/{self.roblox_user_id}/profile"
