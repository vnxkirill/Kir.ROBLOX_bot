"""Тесты модуля Roblox: парсинг каталога и форматирование."""

from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.handlers import _format_items
from app.modules.roblox.skills import SKILLS, RobloxSkill
from app.schemas.roblox import UGCItem


def test_parse_item_full() -> None:
    raw = {
        "id": 115407134203241,
        "name": "Sword",
        "creatorName": "Rare Finds",
        "creatorHasVerifiedBadge": True,
        "price": 140,
        "favoriteCount": 9639,
    }
    item = RobloxCatalogClient._parse_item(raw)
    assert item.name == "Sword"
    assert item.price == 140
    assert item.creator_verified
    assert item.url == "https://www.roblox.com/catalog/115407134203241"


def test_parse_item_minimal() -> None:
    item = RobloxCatalogClient._parse_item({"id": 1})
    assert item.name == "Без названия"
    assert item.price is None
    assert item.favorite_count == 0


def test_format_items_contains_links() -> None:
    items = [UGCItem(id=42, name="Cat Hat", creator_name="Kir", price=99)]
    text = _format_items(items)
    assert "Cat Hat" in text
    assert "https://www.roblox.com/catalog/42" in text
    assert "99 R$" in text


def test_ready_skills() -> None:
    ready = {s for s, info in SKILLS.items() if info.ready}
    assert ready == {RobloxSkill.CHAT, RobloxSkill.UGC_SEARCH, RobloxSkill.FRIENDS}
