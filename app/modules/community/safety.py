"""Фильтр безопасности для детского сообщества.

Блокирует классические схемы обмана в Roblox: выманивание паролей,
«бесплатные робуксы», запросы личных данных и ссылки на сторонние сайты.
Перенесено из legacy robloxbot/safety.py; списки — в нижнем регистре.
"""

import re

# Фразы, которые блокируются всегда.
BLOCKED_PATTERNS = (
    "пароль",
    "password",
    "передай аккаунт",
    "дай аккаунт",
    "free robux",
    "бесплатные робуксы",
    "халявные робуксы",
    "робуксы бесплатно",
    "cookie",
    ".roblosecurity",
    "номер телефона",
    "phone number",
    "домашний адрес",
    "home address",
    "номер карты",
    "card number",
    "cvv",
)

_URL_RE = re.compile(r"https?://\S+|\b\w+\.(?:com|ru|net|org|gg|xyz)\b", re.IGNORECASE)

# Разрешённые ссылки — только официальные домены Roblox.
_ALLOWED_HOSTS = ("roblox.com", "www.roblox.com")


def find_blocked_phrase(text: str) -> str | None:
    """Вернуть первую найденную запрещённую фразу, иначе None."""
    lowered = text.lower()
    for phrase in BLOCKED_PATTERNS:
        if phrase in lowered:
            return phrase
    return None


def has_unsafe_link(text: str) -> bool:
    """True, если в тексте есть ссылка не на Roblox."""
    for match in _URL_RE.finditer(text):
        link = match.group(0).lower()
        host = link.split("//")[-1].split("/")[0]
        if not any(
            host == allowed or host.endswith("." + allowed.removeprefix("www."))
            for allowed in _ALLOWED_HOSTS
        ):
            return True
    return False


def check_text(text: str) -> str | None:
    """Проверить текст пользователя. Вернуть сообщение об ошибке или None, если всё ок."""
    phrase = find_blocked_phrase(text)
    if phrase is not None:
        return (
            "⛔ Это сообщение нельзя опубликовать: оно содержит запрещённую "
            f"фразу («{phrase}»). Никогда не делись паролем и личными данными!"
        )
    if has_unsafe_link(text):
        return (
            "⛔ Ссылки на сторонние сайты запрещены. Разрешены только ссылки "
            "на roblox.com."
        )
    return None


SAFETY_TIPS = (
    "🛡️ Правила безопасности:\n"
    "• Никогда никому не говори свой пароль — даже «админам».\n"
    "• Бесплатных робуксов не бывает — это всегда обман.\n"
    "• Обменивайся только через официальное меню обмена в игре.\n"
    "• Не переходи по ссылкам вне roblox.com.\n"
    "• Если что-то кажется подозрительным — напиши /report."
)
