"""Клиент новостей: официальная RSS-лента анонсов Roblox.

Только публичный RSS, без авторизации. Источник легко заменить или
дополнить — парсинг вынесен в статический метод.
"""

import xml.etree.ElementTree as ET

import aiohttp
from loguru import logger

from app.core.exceptions import ExternalServiceError
from app.schemas.news import NewsItem

# Официальные анонсы и обновления Roblox.
_ROBLOX_ANNOUNCEMENTS_RSS = "https://devforum.roblox.com/c/updates/announcements/36.rss"
_TIMEOUT = aiohttp.ClientTimeout(total=15)


class RobloxNewsClient:
    def __init__(self, http: aiohttp.ClientSession) -> None:
        self._http = http

    async def latest(self, limit: int = 5) -> list[NewsItem]:
        """Свежие анонсы Roblox (не больше limit)."""
        try:
            async with self._http.get(
                _ROBLOX_ANNOUNCEMENTS_RSS, timeout=_TIMEOUT
            ) as response:
                if response.status != 200:
                    logger.error("Roblox RSS HTTP {}", response.status)
                    raise ExternalServiceError(f"Лента новостей вернула HTTP {response.status}")
                raw = await response.text()
        except aiohttp.ClientError as exc:
            logger.error("Сетевая ошибка ленты новостей: {}", exc)
            raise ExternalServiceError("Не удалось загрузить новости") from exc

        return self._parse(raw)[:limit]

    @staticmethod
    def _parse(raw: str) -> list[NewsItem]:
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            logger.error("Не удалось разобрать RSS новостей: {}", exc)
            raise ExternalServiceError("Формат ленты новостей не распознан") from exc

        items: list[NewsItem] = []
        for node in root.findall(".//item"):
            title = (node.findtext("title") or "").strip()
            link = (node.findtext("link") or "").strip()
            if title and link:
                items.append(
                    NewsItem(
                        title=title,
                        url=link,
                        published=(node.findtext("pubDate") or "").strip(),
                    )
                )
        return items
