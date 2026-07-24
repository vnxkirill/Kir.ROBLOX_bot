"""Тесты профиля: сохранение ника и рендер карточки."""

from app.modules.profile.handlers import _profile_text
from app.repositories import UserRepository


async def test_set_nickname_creates_and_saves(db_session) -> None:
    users = UserRepository(db_session)
    user = await users.set_nickname(555, "KirPro", 12345)
    await db_session.commit()

    assert user.telegram_id == 555
    assert user.nickname == "KirPro"
    assert user.roblox_user_id == 12345
    assert user.roblox_profile_url == "https://www.roblox.com/users/12345/profile"


async def test_set_nickname_updates_existing(db_session) -> None:
    users = UserRepository(db_session)
    await users.set_nickname(555, "Old", 1)
    await db_session.commit()

    await users.set_nickname(555, "New", 2)
    await db_session.commit()

    fresh = await users.get_by_telegram_id(555)
    assert fresh.nickname == "New"
    assert fresh.roblox_user_id == 2


def test_profile_text_without_nick() -> None:
    assert "не привязан" in _profile_text(None)


def test_profile_text_escapes_nick() -> None:
    class _U:
        nickname = "<b>hax</b>"
        roblox_user_id = None
        roblox_profile_url = None

    text = _profile_text(_U())
    assert "&lt;b&gt;" in text


def test_profile_text_links_verified() -> None:
    class _U:
        nickname = "Kir"
        roblox_user_id = 42
        roblox_profile_url = "https://www.roblox.com/users/42/profile"

    text = _profile_text(_U())
    assert "https://www.roblox.com/users/42/profile" in text
    assert "☑️" in text
