"""Telegram-хендлеры раздела «Игры»: площадка мини-игр (Mini App).

Меню собирается из catalog.GAMES: готовые игры открываются как WebApp
прямо в Telegram, неготовые показывают «скоро».
"""

from aiogram import F, Router
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.keyboards import MainMenuButton
from app.modules.games.catalog import GAMES, GAMES_BASE_URL

router = Router(name="games")

_GAMES_TEXT = (
    "🕹 <b>batmGAMES</b>\n\n"
    "Наша игровая площадка — подарок каждому игроку: мини-игры прямо в Telegram!\n"
    "Выбирай и играй, ничего скачивать не нужно:"
)


class GamesCallback(CallbackData, prefix="games"):
    action: str
    slug: str = ""


def _games_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for game in GAMES:
        if game.ready:
            builder.button(text=game.title, web_app=WebAppInfo(url=game.url))
        else:
            builder.button(
                text=f"🔒 {game.title}",
                callback_data=GamesCallback(action="soon", slug=game.slug),
            )
    builder.button(
        text="🕹 batmGAMES — вся площадка", web_app=WebAppInfo(url=f"{GAMES_BASE_URL}/")
    )
    builder.adjust(1)
    return builder.as_markup()


@router.message(F.text == MainMenuButton.GAMES)
async def games_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_GAMES_TEXT, reply_markup=_games_keyboard())


@router.callback_query(GamesCallback.filter(F.action == "soon"))
async def game_soon(callback: CallbackQuery, callback_data: GamesCallback) -> None:
    game = next((g for g in GAMES if g.slug == callback_data.slug), None)
    title = game.title if game else "Игра"
    await callback.answer(f"{title} — уже в разработке, следи за новостями! 🔜", show_alert=True)
