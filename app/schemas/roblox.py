"""Схемы Roblox — DTO, независимые от формата API."""

from pydantic import BaseModel


class UGCItem(BaseModel):
    """Предмет каталога Roblox (UGC)."""

    id: int
    name: str
    creator_name: str
    creator_verified: bool = False
    price: int | None = None
    favorite_count: int = 0

    @property
    def url(self) -> str:
        return f"https://www.roblox.com/catalog/{self.id}"


class RobloxProfile(BaseModel):
    """Публичный профиль игрока Roblox."""

    id: int
    username: str
    display_name: str = ""
    verified: bool = False

    @property
    def url(self) -> str:
        return f"https://www.roblox.com/users/{self.id}/profile"
