"""Тесты площадки мини-игр."""

from app.modules.games.catalog import GAMES, GAMES_BASE_URL
from app.modules.games.handlers import _games_keyboard


def test_catalog_has_ready_runner() -> None:
    ready = [g for g in GAMES if g.ready]
    assert any(g.slug == "runner" for g in ready)


def test_game_urls_point_to_pages() -> None:
    for game in GAMES:
        assert game.url == f"{GAMES_BASE_URL}/{game.slug}/"
        assert game.url.startswith("https://")


def test_keyboard_ready_games_are_webapps() -> None:
    keyboard = _games_keyboard()
    buttons = [b for row in keyboard.inline_keyboard for b in row]
    # все игры + кнопка «вся площадка»
    assert len(buttons) == len(GAMES) + 1

    by_text = {b.text: b for b in buttons}
    for game in GAMES:
        if game.ready:
            button = by_text[game.title]
            assert button.web_app is not None and button.web_app.url == game.url
        else:
            button = by_text[f"🔒 {game.title}"]
            assert button.web_app is None and button.callback_data is not None
