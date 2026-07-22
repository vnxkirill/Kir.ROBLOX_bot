"""Доска «Ищу друзей»: общий список Roblox-ников, видимый всем пользователям.

Каждый может добавить свой ник (проверяется через официальный API Roblox)
или убрать его. Одно объявление на пользователя.
"""

from contextlib import suppress
from html import escape

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.container import Container
from app.models import FriendListing
from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.skills import RobloxSkill, RobloxSkillCallback
from app.modules.roblox.states import FriendSearch
from app.repositories import FriendListingRepository

friends_router = Router(name="roblox-friends")

_PROMPT = (
    "👥 <b>Ищу друзей</b>\n\n"
    "Напиши свой ник в Roblox — я проверю его и добавлю в общий список.\n"
    "Отмена: /menu"
)
_NOT_FOUND = "❌ Игрок с таким ником не найден в Roblox. Проверь написание."
_EMPTY = "👥 <b>Ищу друзей</b>\n\nПока никто не добавился. Будь первым!"


class FriendsCallback(CallbackData, prefix="rbxfr"):
    action: str


def _board_text(listings: list[FriendListing]) -> str:
    if not listings:
        return _EMPTY
    lines = ["👥 <b>Ищу друзей в Roblox</b>\n"]
    for i, item in enumerate(listings, 1):
        lines.append(
            f'{i}. <a href="{item.profile_url}">{escape(item.roblox_username)}</a>'
        )
    lines.append("\nДобавь свой ник кнопкой ниже — его увидят все!")
    return "\n".join(lines)


def _board_keyboard(has_own: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="➕ Добавить мой ник", callback_data=FriendsCallback(action="add"))
    if has_own:
        builder.button(
            text="🗑 Убрать мой ник", callback_data=FriendsCallback(action="remove")
        )
    builder.adjust(1)
    return builder.as_markup()


async def _show_board(message: Message, db: AsyncSession, telegram_id: int, *, edit: bool) -> None:
    repo = FriendListingRepository(db)
    listings = await repo.list_all()
    has_own = await repo.get_by_telegram_id(telegram_id) is not None
    text = _board_text(listings)
    markup = _board_keyboard(has_own)
    if edit:
        with suppress(TelegramBadRequest):
            await message.edit_text(text, reply_markup=markup, disable_web_page_preview=True)
    else:
        await message.answer(text, reply_markup=markup, disable_web_page_preview=True)


@friends_router.callback_query(RobloxSkillCallback.filter(F.skill == RobloxSkill.FRIENDS))
async def open_board(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    await state.clear()
    await _show_board(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer()


@friends_router.callback_query(FriendsCallback.filter(F.action == "add"))
async def start_add(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(FriendSearch.waiting_nickname)
    await callback.message.answer(_PROMPT)
    await callback.answer()


@friends_router.callback_query(FriendsCallback.filter(F.action == "remove"))
async def remove_own(callback: CallbackQuery, state: FSMContext, db: AsyncSession) -> None:
    await FriendListingRepository(db).remove(callback.from_user.id)
    await state.clear()
    await _show_board(callback.message, db, callback.from_user.id, edit=True)
    await callback.answer("🗑 Твой ник убран из списка")


@friends_router.message(FriendSearch.waiting_nickname, F.text)
async def save_nickname(
    message: Message, state: FSMContext, container: Container, db: AsyncSession
) -> None:
    nickname = message.text.strip()

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    profile = await container.get(RobloxCatalogClient).resolve_user(nickname)
    if profile is None:
        await message.answer(_NOT_FOUND)
        return

    await FriendListingRepository(db).upsert(
        message.from_user.id, profile.id, profile.username
    )
    await state.clear()
    await message.answer(
        f'✅ Добавил тебя в список: <a href="{profile.url}">{escape(profile.username)}</a>',
        disable_web_page_preview=True,
    )
    await _show_board(message, db, message.from_user.id, edit=False)
