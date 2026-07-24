"""Telegram-хендлеры раздела «Профиль»: просмотр и ввод ника."""

from html import escape

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback
from app.models import User
from app.modules.profile.states import ProfileEdit
from app.modules.roblox.api import RobloxCatalogClient
from app.repositories import UserRepository

router = Router(name="profile")

_PROMPT = (
    "✏️ Напиши свой <b>ник в Roblox</b> — я проверю, что такой игрок есть, "
    "и сохраню его в профиль.\n"
    "Отмена: /menu"
)
_NOT_FOUND = "❌ Игрок с таким ником не найден в Roblox. Проверь написание и попробуй ещё раз."


class ProfileCallback(CallbackData, prefix="profile"):
    action: str


def _profile_text(user: User | None) -> str:
    nickname = user.nickname if user and user.nickname else None
    if not nickname:
        return (
            "👤 <b>Твой профиль</b>\n\n"
            "Roblox-ник пока не привязан. Нажми кнопку ниже и введи свой ник."
        )
    url = user.roblox_profile_url
    nick = escape(nickname)
    link = f'<a href="{url}">{nick}</a> ☑️' if url else f"<b>{nick}</b>"
    return f"👤 <b>Твой профиль</b>\n\nRoblox: {link}"


def _profile_keyboard(has_nick: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text = "✏️ Изменить Roblox-ник" if has_nick else "✏️ Привязать Roblox-ник"
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
async def save_nickname(
    message: Message, state: FSMContext, db: AsyncSession, container: Container
) -> None:
    nickname = message.text.strip()

    # Проверяем ник в Roblox: сохраняем только реально существующий аккаунт.
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    profile = await container.get(RobloxCatalogClient).resolve_user(nickname)
    if profile is None:
        await message.answer(_NOT_FOUND)
        return

    await UserRepository(db).set_nickname(
        message.from_user.id, profile.username, profile.id
    )
    await state.clear()
    await message.answer(
        f'✅ Roblox-аккаунт подтверждён и сохранён: '
        f'<a href="{profile.url}">{escape(profile.username)}</a>',
        disable_web_page_preview=True,
    )
    await _show_profile(message, db, message.from_user.id)
