"""Базовые хендлеры: /start, /menu и навигация по главному меню.

Разделы открываются двумя способами: reply-кнопки под полем ввода
и inline-кнопки в сообщении. Оба ведут к одним и тем же действиям.
"""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import (
    MainMenuAction,
    MainMenuButton,
    main_menu_keyboard,
    main_reply_keyboard,
)
from app.keyboards.main_menu import MainMenuCallback
from app.repositories import UserRepository

router = Router(name="start")

_WELCOME = (
    "👋 Привет! Я <b>GameCore AI</b> — твой персональный игровой ассистент.\n\n"
    "Выбери раздел:"
)

# Тексты-заглушки разделов, у которых ещё нет своего модуля с хендлерами.
# Раздел с реальной логикой (например AI) сюда не входит — его обрабатывает
# роутер соответствующего модуля.
_SECTION_STUBS: dict[MainMenuAction, str] = {
    MainMenuAction.SETTINGS: "⚙ Раздел «Настройки» в разработке.",
    MainMenuAction.HELP: "❓ Раздел «Помощь» в разработке.",
}

# Соответствие reply-кнопок разделам-заглушкам.
_BUTTON_TO_ACTION: dict[MainMenuButton, MainMenuAction] = {
    MainMenuButton.SETTINGS: MainMenuAction.SETTINGS,
    MainMenuButton.HELP: MainMenuAction.HELP,
}


@router.message(CommandStart())
async def cmd_start(message: Message, db: AsyncSession, state: FSMContext) -> None:
    await state.clear()
    users = UserRepository(db)
    await users.get_or_create(
        message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        language_code=message.from_user.language_code,
    )
    await message.answer(_WELCOME, reply_markup=main_reply_keyboard())


@router.message(Command("menu"))
@router.message(F.text == MainMenuButton.HOME)
async def cmd_menu(message: Message, state: FSMContext) -> None:
    """Вернуться в главное меню из любого состояния."""
    await state.clear()
    await message.answer(_WELCOME, reply_markup=main_reply_keyboard())


@router.message(F.text.in_(set(_BUTTON_TO_ACTION)))
async def reply_section(message: Message, state: FSMContext) -> None:
    await state.clear()
    action = _BUTTON_TO_ACTION[MainMenuButton(message.text)]
    await message.answer(_SECTION_STUBS[action])


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.HOME))
async def menu_home(callback: CallbackQuery) -> None:
    await callback.message.edit_text(_WELCOME, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(MainMenuCallback.filter(F.action.in_(set(_SECTION_STUBS))))
async def menu_section(callback: CallbackQuery, callback_data: MainMenuCallback) -> None:
    await callback.message.edit_text(
        _SECTION_STUBS[callback_data.action], reply_markup=main_menu_keyboard()
    )
    await callback.answer()
