"""Тесты FNF-модуля: инструкция по установке модов."""

from app.modules.fnf.handlers import _ASSETS_DIR, _GUIDE_CAPTION, _GUIDE_STEPS, _build_album


def test_guide_assets_exist() -> None:
    for filename, _ in _GUIDE_STEPS:
        assert (_ASSETS_DIR / filename).is_file(), f"нет файла {filename}"


def test_album_caption_only_on_first() -> None:
    album = _build_album()
    assert len(album) == len(_GUIDE_STEPS)
    assert album[0].caption == _GUIDE_CAPTION
    assert all(item.caption is None for item in album[1:])


def test_caption_within_telegram_limit() -> None:
    # Лимит подписи Telegram — 1024 символа.
    assert len(_GUIDE_CAPTION) <= 1024
