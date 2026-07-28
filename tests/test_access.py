"""Тесты контроля доступа: открытое тестирование + флаг is_admin."""

from types import SimpleNamespace

from app.config.settings import BotSettings
from app.middleware.access import AccessMiddleware

_OWNER = 262147628
_ADMIN = 5847299382


def _bot_settings(**kwargs) -> BotSettings:
    return BotSettings(token="x", owner_id=_OWNER, _env_file=None, **kwargs)


def test_admin_ids_parsed_from_string() -> None:
    settings = _bot_settings(admin_ids=f"{_ADMIN}")
    assert settings.admin_ids == [_ADMIN]
    assert settings.all_admin_ids == {_OWNER, _ADMIN}


def test_admin_ids_default_empty() -> None:
    settings = _bot_settings()
    assert settings.admin_ids == []
    assert settings.all_admin_ids == {_OWNER}


async def _run(middleware: AccessMiddleware, user_id: int | None) -> dict:
    data: dict = {}
    if user_id is not None:
        data["event_from_user"] = SimpleNamespace(id=user_id)

    async def handler(event, handler_data):
        handler_data["handled"] = True
        return "ok"

    result = await middleware(handler, SimpleNamespace(), data)
    assert result == "ok"  # все пользователи проходят
    return data


async def test_everyone_passes_admin_flagged() -> None:
    middleware = AccessMiddleware({_OWNER, _ADMIN})

    data = await _run(middleware, _OWNER)
    assert data["is_admin"] is True

    data = await _run(middleware, _ADMIN)
    assert data["is_admin"] is True

    data = await _run(middleware, 111)
    assert data["is_admin"] is False

    data = await _run(middleware, None)
    assert data["is_admin"] is False
