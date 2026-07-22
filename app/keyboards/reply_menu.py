"""Reply-клавиатура — постоянные кнопки под полем ввода.

Тексты кнопок объявлены в MainMenuButton: хендлеры фильтруют по этим же
константам, поэтому текст меняется в одном месте.
"""

from enum import StrEnum

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class MainMenuButton(StrEnum):
    HOME = "🏠 Главная"
    CHAT = "💬 Общение"
    AI = "🤖 AI"
    ROBLOX = "🎮 Roblox"
    FNF = "🎵 FNF Mods"
    PROFILE = "👤 Профиль"
    SETTINGS = "⚙ Настройки"
    HELP = "❓ Помощь"


def main_reply_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button in MainMenuButton:
        builder.add(KeyboardButton(text=button))
    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выбери раздел или напиши сообщение…",
    )
