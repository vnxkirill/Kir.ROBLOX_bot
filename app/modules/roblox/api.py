"""Клиент официального каталога Roblox.

Использует только публичные API (без авторизации) — автоматизация
аккаунтов запрещена правилами Roblox и здесь не применяется.
"""

from typing import Any

import aiohttp
from loguru import logger

from app.core.exceptions import ExternalServiceError
from app.schemas.roblox import RobloxProfile, UGCItem

_CATALOG_URL = "https://catalog.roblox.com/v1/search/items/details"
_USERNAMES_URL = "https://users.roblox.com/v1/usernames/users"
# API принимает только эти значения Limit.
_PAGE_LIMIT = 10
_TIMEOUT = aiohttp.ClientTimeout(total=15)


class RobloxCatalogClient:
    def __init__(self, http: aiohttp.ClientSession) -> None:
        self._http = http

    async def search_ugc(self, keyword: str) -> list[UGCItem]:
        """Найти предметы каталога по ключевому слову."""
        params = {"Keyword": keyword, "Limit": _PAGE_LIMIT}
        try:
            async with self._http.get(
                _CATALOG_URL, params=params, timeout=_TIMEOUT
            ) as response:
                body = await response.json()
                if response.status == 429:
                    raise ExternalServiceError(
                        "Roblox API: слишком много запросов",
                        user_message="⏳ Roblox просит подождать. Попробуй через минуту.",
                    )
                if response.status != 200:
                    logger.error("Roblox catalog HTTP {}: {}", response.status, body)
                    raise ExternalServiceError(f"Roblox catalog вернул HTTP {response.status}")
        except aiohttp.ClientError as exc:
            logger.error("Сетевая ошибка Roblox catalog: {}", exc)
            raise ExternalServiceError("Сетевая ошибка при обращении к Roblox") from exc

        return [self._parse_item(raw) for raw in body.get("data", [])]

    async def resolve_user(self, username: str) -> RobloxProfile | None:
        """Найти игрока по нику. None — если такого аккаунта нет."""
        payload = {"usernames": [username], "excludeBannedUsers": False}
        try:
            async with self._http.post(
                _USERNAMES_URL, json=payload, timeout=_TIMEOUT
            ) as response:
                if response.status != 200:
                    logger.error("Roblox usernames HTTP {}", response.status)
                    raise ExternalServiceError(f"Roblox вернул HTTP {response.status}")
                body = await response.json()
        except aiohttp.ClientError as exc:
            logger.error("Сетевая ошибка Roblox usernames: {}", exc)
            raise ExternalServiceError("Сетевая ошибка при обращении к Roblox") from exc

        data = body.get("data") or []
        if not data:
            return None
        raw = data[0]
        return RobloxProfile(
            id=raw["id"],
            username=raw["name"],
            display_name=raw.get("displayName", ""),
            verified=raw.get("hasVerifiedBadge", False),
        )

    @staticmethod
    def _parse_item(raw: dict[str, Any]) -> UGCItem:
        return UGCItem(
            id=raw["id"],
            name=raw.get("name", "Без названия"),
            creator_name=raw.get("creatorName", "?"),
            creator_verified=raw.get("creatorHasVerifiedBadge", False),
            price=raw.get("price"),
            favorite_count=raw.get("favoriteCount", 0),
        )
