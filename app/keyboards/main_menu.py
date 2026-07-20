"""Главное меню.

Callback-данные типизированы через CallbackData — никаких «магических
строк»: хендлеры фильтруют по классу, опечатка ловится на старте.
"""

from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MainMenuAction(StrEnum):
    HOME = "home"
    AI = "ai"
    ROBLOX = "roblox"
    PROFILE = "profile"
    SETTINGS = "settings"
    HELP = "help"


class MainMenuCallback(CallbackData, prefix="menu"):
    action: MainMenuAction


_BUTTONS: list[tuple[str, MainMenuAction]] = [
    ("🏠 Главная", MainMenuAction.HOME),
    ("🤖 AI", MainMenuAction.AI),
    ("🎮 Roblox", MainMenuAction.ROBLOX),
    ("👤 Профиль", MainMenuAction.PROFILE),
    ("⚙ Настройки", MainMenuAction.SETTINGS),
    ("❓ Помощь", MainMenuAction.HELP),
]


def main_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for text, action in _BUTTONS:
        builder.button(text=text, callback_data=MainMenuCallback(action=action))
    builder.adjust(2)
    return builder.as_markup()
