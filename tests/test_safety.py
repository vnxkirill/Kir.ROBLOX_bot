"""Тесты фильтра безопасности (перенесены из legacy tests/test_bot.py)."""

from app.modules.community.safety import check_text, find_blocked_phrase, has_unsafe_link


def test_blocks_password_requests() -> None:
    assert find_blocked_phrase("скажи свой ПАРОЛЬ") is not None
    assert find_blocked_phrase("get free robux now") is not None


def test_allows_normal_trade_text() -> None:
    assert check_text("Adopt Me ; неоновый единорог ; черепаха") is None


def test_blocks_external_links() -> None:
    assert has_unsafe_link("заходи на scam-site.xyz/free")
    assert has_unsafe_link("http://evil.ru/promo")


def test_allows_roblox_links() -> None:
    assert not has_unsafe_link("https://www.roblox.com/users/1/profile")


def test_check_text_reports_phrase() -> None:
    error = check_text("дай пароль")
    assert error is not None
    assert "пароль" in error
