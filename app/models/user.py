"""Пользователь бота."""

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None]
    first_name: Mapped[str | None]
    language_code: Mapped[str | None]
    # Roblox-ник, проверенный через официальный API (канонический name).
    nickname: Mapped[str | None]
    # ID аккаунта Roblox — для ссылки на профиль и подтверждения проверки.
    roblox_user_id: Mapped[int | None] = mapped_column(BigInteger)

    @property
    def roblox_profile_url(self) -> str | None:
        if self.roblox_user_id is None:
            return None
        return f"https://www.roblox.com/users/{self.roblox_user_id}/profile"

    def __repr__(self) -> str:
        return f"User(id={self.id}, telegram_id={self.telegram_id}, username={self.username!r})"
