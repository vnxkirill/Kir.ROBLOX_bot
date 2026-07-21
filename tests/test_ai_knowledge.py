"""Тесты знаний бота и fallback-роутера."""

from app.modules.ai.knowledge import SYSTEM_PROMPT
from app.routers import build_root_router


def test_system_prompt_mentions_key_sections() -> None:
    for keyword in ("GameCore AI", "Roblox", "FNF", "UGC", "/menu", "GameJolt"):
        assert keyword in SYSTEM_PROMPT, f"в промпте нет «{keyword}»"


def test_system_prompt_has_safety_rule() -> None:
    assert "пароли" in SYSTEM_PROMPT
    assert "робуксов" in SYSTEM_PROMPT


def test_fallback_router_is_last() -> None:
    root = build_root_router([])
    names = [r.name for r in root.sub_routers]
    assert names[-1] == "ai-fallback", f"fallback не последний: {names}"
