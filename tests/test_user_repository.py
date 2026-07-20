"""Тесты репозитория пользователей."""

from app.repositories import UserRepository


async def test_get_or_create_creates_new(db_session) -> None:
    users = UserRepository(db_session)
    user = await users.get_or_create(123, username="kirill", first_name="Кирилл")
    await db_session.commit()

    assert user.id is not None
    assert user.telegram_id == 123
    assert user.username == "kirill"


async def test_get_or_create_updates_existing(db_session) -> None:
    users = UserRepository(db_session)
    first = await users.get_or_create(123, username="old")
    await db_session.commit()

    second = await users.get_or_create(123, username="new")
    await db_session.commit()

    assert second.id == first.id
    assert second.username == "new"


async def test_get_by_telegram_id_missing(db_session) -> None:
    users = UserRepository(db_session)
    assert await users.get_by_telegram_id(999) is None
