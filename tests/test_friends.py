"""Тесты доски «Ищу друзей»: репозиторий, парсинг профиля, форматирование."""

from app.models import FriendListing
from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.friends import _board_text
from app.repositories import FriendListingRepository


async def test_upsert_creates_then_updates(db_session) -> None:
    repo = FriendListingRepository(db_session)
    await repo.upsert(1, 100, "Kir")
    await db_session.commit()

    # Тот же пользователь меняет ник — запись обновляется, не дублируется.
    await repo.upsert(1, 200, "KirNew")
    await db_session.commit()

    listings = await repo.list_all()
    assert len(listings) == 1
    assert listings[0].roblox_username == "KirNew"
    assert listings[0].roblox_user_id == 200


async def test_list_shows_all_users(db_session) -> None:
    repo = FriendListingRepository(db_session)
    await repo.upsert(1, 100, "Kir")
    await repo.upsert(2, 101, "Max")
    await db_session.commit()

    listings = await repo.list_all()
    assert {item.roblox_username for item in listings} == {"Kir", "Max"}


async def test_remove(db_session) -> None:
    repo = FriendListingRepository(db_session)
    await repo.upsert(1, 100, "Kir")
    await db_session.commit()

    assert await repo.remove(1) is True
    await db_session.commit()
    assert await repo.list_all() == []
    assert await repo.remove(1) is False


def test_board_text_empty() -> None:
    assert "Будь первым" in _board_text([])


def test_board_text_lists_and_escapes() -> None:
    listing = FriendListing(telegram_id=1, roblox_user_id=42, roblox_username="a<b>")
    text = _board_text([listing])
    assert "https://www.roblox.com/users/42/profile" in text
    assert "a&lt;b&gt;" in text


def test_resolve_user_parsing() -> None:
    # Проверяем разбор ответа Roblox usernames API на уровне схемы.
    from app.schemas.roblox import RobloxProfile

    p = RobloxProfile(id=1, username="Roblox", display_name="Roblox", verified=True)
    assert p.url == "https://www.roblox.com/users/1/profile"


def test_client_has_resolve_user() -> None:
    assert hasattr(RobloxCatalogClient, "resolve_user")
