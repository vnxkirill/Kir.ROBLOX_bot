"""Telegram-хендлеры раздела «Новости»: свежие анонсы Roblox."""

from html import escape

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.core.container import Container
from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback
from app.modules.news.api import RobloxNewsClient
from app.schemas.news import NewsItem

router = Router(name="news")

_EMPTY_TEXT = "📭 Сейчас новостей нет. Загляни позже."


def _format(items: list[NewsItem]) -> str:
    lines = ["📰 <b>Свежие новости Roblox</b>\n"]
    for i, item in enumerate(items, 1):
        lines.append(f'{i}. <a href="{item.url}">{escape(item.title)}</a>')
    lines.append("\nИсточник: официальные анонсы Roblox DevForum.")
    return "\n".join(lines)


async def _send_news(message: Message, container: Container) -> None:
    client = container.get(RobloxNewsClient)
    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    items = await client.latest()
    text = _format(items) if items else _EMPTY_TEXT
    await message.answer(text, disable_web_page_preview=True)


@router.message(F.text == MainMenuButton.NEWS)
async def news_message(message: Message, state: FSMContext, container: Container) -> None:
    await state.clear()
    await _send_news(message, container)


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.NEWS))
async def news_callback(
    callback: CallbackQuery, state: FSMContext, container: Container
) -> None:
    await state.clear()
    await _send_news(callback.message, container)
    await callback.answer()
