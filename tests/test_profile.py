"""Тесты профиля: сохранение ника и рендер карточки."""

from app.modules.profile.handlers import _profile_text
from app.repositories import UserRepository


async def test_set_nickname_creates_and_saves(db_session) -> None:
    users = UserRepository(db_session)
    user = await users.set_nickname(555, "KirPro")
    await db_session.commit()

    assert user.telegram_id == 555
    assert user.nickname == "KirPro"


async def test_set_nickname_updates_existing(db_session) -> None:
    users = UserRepository(db_session)
    await users.set_nickname(555, "Old")
    await db_session.commit()

    await users.set_nickname(555, "New")
    await db_session.commit()

    fresh = await users.get_by_telegram_id(555)
    assert fresh.nickname == "New"


def test_profile_text_without_nick() -> None:
    assert "не задан" in _profile_text(None)


def test_profile_text_escapes_nick() -> None:
    class _U:
        nickname = "<b>hax</b>"

    text = _profile_text(_U())
    assert "&lt;b&gt;" in text
