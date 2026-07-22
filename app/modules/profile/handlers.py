"""Telegram-хендлеры раздела «Профиль»: просмотр и ввод ника."""

from html import escape

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback
from app.models import User
from app.modules.profile.states import ProfileEdit
from app.repositories import UserRepository

router = Router(name="profile")

_NICK_MIN = 2
_NICK_MAX = 32

_PROMPT = (
    "✏️ Напиши свой ник (от 2 до 32 символов).\n"
    "Отмена: /menu"
)
_TOO_LONG = f"⚠️ Слишком длинно. Ник должен быть от {_NICK_MIN} до {_NICK_MAX} символов."
_TOO_SHORT = f"⚠️ Слишком коротко. Ник должен быть от {_NICK_MIN} до {_NICK_MAX} символов."


class ProfileCallback(CallbackData, prefix="profile"):
    action: str


def _profile_text(user: User | None) -> str:
    nickname = user.nickname if user and user.nickname else None
    if nickname:
        return f"👤 <b>Твой профиль</b>\n\nНик: <b>{escape(nickname)}</b>"
    return "👤 <b>Твой профиль</b>\n\nНик пока не задан. Нажми кнопку ниже, чтобы ввести."


def _profile_keyboard(has_nick: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text = "✏️ Изменить ник" if has_nick else "✏️ Ввести ник"
    builder.button(text=text, callback_data=ProfileCallback(action="edit"))
    return builder.as_markup()


async def _show_profile(message: Message, db: AsyncSession, telegram_id: int) -> None:
    user = await UserRepository(db).get_by_telegram_id(telegram_id)
    await message.answer(
        _profile_text(user),
        reply_markup=_profile_keyboard(has_nick=bool(user and user.nickname)),
    )


@router.message(F.text == MainMenuButton.PROFILE)
async def profile_message(message: Message, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await _show_profile(message, db, message.from_user.id)


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.PROFILE))
async def profile_callback(
    callback: CallbackQuery, state: FSMContext, db: AsyncSession
) -> None:
    await state.clear()
    await _show_profile(callback.message, db, callback.from_user.id)
    await callback.answer()


@router.callback_query(ProfileCallback.filter(F.action == "edit"))
async def start_edit(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ProfileEdit.waiting_nickname)
    await callback.message.answer(_PROMPT)
    await callback.answer()


@router.message(ProfileEdit.waiting_nickname, F.text)
async def save_nickname(message: Message, state: FSMContext, db: AsyncSession) -> None:
    nickname = message.text.strip()
    if len(nickname) < _NICK_MIN:
        await message.answer(_TOO_SHORT)
        return
    if len(nickname) > _NICK_MAX:
        await message.answer(_TOO_LONG)
        return

    await UserRepository(db).set_nickname(message.from_user.id, nickname)
    await state.clear()
    await message.answer(f"✅ Ник сохранён: <b>{escape(nickname)}</b>")
    await _show_profile(message, db, message.from_user.id)
