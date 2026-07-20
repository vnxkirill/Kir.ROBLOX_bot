"""Тесты DI-контейнера."""

import pytest

from app.core.container import Container


class _FakeService:
    pass


def _make_container() -> Container:
    # Для контейнера как такового зависимости не важны — подойдут заглушки.
    return Container(settings=None, engine=None, session_factory=None, http=None)  # type: ignore[arg-type]


def test_register_and_get() -> None:
    container = _make_container()
    service = _FakeService()
    container.register(service)
    assert container.get(_FakeService) is service


def test_get_unregistered_raises() -> None:
    container = _make_container()
    with pytest.raises(RuntimeError, match="не зарегистрирован"):
        container.get(_FakeService)


def test_double_register_raises() -> None:
    container = _make_container()
    container.register(_FakeService())
    with pytest.raises(RuntimeError, match="уже зарегистрирован"):
        container.register(_FakeService())
