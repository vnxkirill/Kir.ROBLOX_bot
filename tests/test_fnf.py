"""Тесты FNF-модуля: инструкции по скачиванию и установке модов."""

from app.modules.fnf.handlers import _ASSETS_DIR, GUIDES, _build_album


def test_guides_present() -> None:
    assert set(GUIDES) == {"download", "install"}


def test_guide_assets_exist() -> None:
    for guide in GUIDES.values():
        for filename, _ in guide.steps:
            assert (_ASSETS_DIR / filename).is_file(), f"нет файла {filename}"


def test_album_caption_only_on_first() -> None:
    for guide in GUIDES.values():
        album = _build_album(guide)
        assert len(album) == len(guide.steps)
        assert album[0].caption == guide.caption
        assert all(item.caption is None for item in album[1:])


def test_caption_within_telegram_limit() -> None:
    # Лимит подписи Telegram — 1024 символа.
    for guide in GUIDES.values():
        assert len(guide.caption) <= 1024, f"подпись «{guide.title}» слишком длинная"
