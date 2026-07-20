"""Базовые хендлеры: /start и навигация по главному меню."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.main_menu import MainMenuAction, MainMenuCallback, main_menu_keyboard
from app.repositories import UserRepository

router = Router(name="start")

_WELCOME = (
    "👋 Привет! Я <b>GameCore AI</b> — твой персональный игровой ассистент.\n\n"
    "Выбери раздел:"
)

# Тексты-заглушки разделов. Логика появится в соответствующих модулях.
_SECTION_STUBS: dict[MainMenuAction, str] = {
    MainMenuAction.HOME: _WELCOME,
    MainMenuAction.AI: "🤖 Раздел AI в разработке.",
    MainMenuAction.ROBLOX: "🎮 Раздел Roblox в разработке.",
    MainMenuAction.PROFILE: "👤 Раздел «Профиль» в разработке.",
    MainMenuAction.SETTINGS: "⚙ Раздел «Настройки» в разработке.",
    MainMenuAction.HELP: "❓ Раздел «Помощь» в разработке.",
}


@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession) -> None:
    users = UserRepository(db)
    await users.get_or_create(
        message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code,
    )
    await message.answer(_WELCOME, reply_markup=main_menu_keyboard())


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.HOME))
async def menu_home(callback: CallbackQuery) -> None:
    await callback.message.edit_text(_WELCOME, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(MainMenuCallback.filter())
async def menu_section(callback: CallbackQuery, callback_data: MainMenuCallback) -> None:
    await callback.message.edit_text(
        _SECTION_STUBS[callback_data.action], reply_markup=main_menu_keyboard()
    )
    await callback.answer()
