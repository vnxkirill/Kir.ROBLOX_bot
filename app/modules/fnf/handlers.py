"""Telegram-хендлеры раздела FNF: ссылки на сообщество модов GameJolt."""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback

router = Router(name="fnf")

_FNF_TEXT = (
    "🎵 <b>FNF Mods</b>\n\n"
    "Моды Friday Night Funkin' живут на GameJolt — жми кнопку:"
)

_GAMEJOLT_FNF_URL = "https://gamejolt.com/c/fnf"
_GAMEJOLT_FNF_GAMES_URL = "https://gamejolt.com/c/fnf/games"


def _fnf_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Открыть GameJolt FNF", url=_GAMEJOLT_FNF_URL)
    builder.button(text="🕹 Только игры и моды", url=_GAMEJOLT_FNF_GAMES_URL)
    builder.adjust(1)
    return builder.as_markup()


@router.message(F.text == MainMenuButton.FNF)
async def fnf_menu_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_FNF_TEXT, reply_markup=_fnf_keyboard())


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.FNF))
async def fnf_menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(_FNF_TEXT, reply_markup=_fnf_keyboard())
    await callback.answer()
