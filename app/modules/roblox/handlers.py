"""Telegram-хендлеры раздела Roblox: меню навыков и поиск UGC.

«Общение» переводит в AI-чат (модуль ai), «Поиск UGC» — рабочий поиск
по официальному каталогу Roblox. Остальные навыки — в разработке.
"""

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from app.core.container import Container
from app.keyboards import MainMenuButton
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback
from app.modules.roblox.api import RobloxCatalogClient
from app.modules.roblox.skills import (
    SKILLS,
    RobloxSkill,
    RobloxSkillCallback,
    skills_keyboard,
)
from app.modules.roblox.states import UGCSearch
from app.schemas.roblox import UGCItem

router = Router(name="roblox")

_MENU_TEXT = "🎮 <b>Roblox</b> — выбери навык:"
_UGC_PROMPT = (
    "🔎 <b>Поиск Roblox UGC</b>\n\n"
    "Напиши, что ищешь (например: <i>dragon wings</i>, <i>cat hat</i>).\n"
    "Вернуться: /menu"
)
_WIP_TEXT = "⬜ Навык «{title}» пока в разработке."
_NOT_FOUND_TEXT = "🔍 Ничего не нашлось. Попробуй другой запрос."


def _format_items(items: list[UGCItem]) -> str:
    lines = ["🛍 <b>Найдено в каталоге:</b>\n"]
    for item in items:
        verified = " ☑️" if item.creator_verified else ""
        price = f"{item.price} R$" if item.price else "бесплатно/оффсейл"
        lines.append(
            f'• <a href="{item.url}">{item.name}</a>\n'
            f"   {price} · ⭐ {item.favorite_count} · от {item.creator_name}{verified}"
        )
    lines.append("\nИщем дальше? Просто напиши новый запрос. Выход: /menu")
    return "\n".join(lines)


@router.message(F.text == MainMenuButton.ROBLOX)
async def roblox_menu_message(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(_MENU_TEXT, reply_markup=skills_keyboard())


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.ROBLOX))
async def roblox_menu_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(_MENU_TEXT, reply_markup=skills_keyboard())
    await callback.answer()


@router.callback_query(RobloxSkillCallback.filter(F.skill == RobloxSkill.UGC_SEARCH))
async def start_ugc_search(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(UGCSearch.waiting_query)
    await callback.message.edit_text(_UGC_PROMPT)
    await callback.answer()


@router.message(UGCSearch.waiting_query, F.text)
async def do_ugc_search(message: Message, container: Container) -> None:
    client = container.get(RobloxCatalogClient)

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    items = await client.search_ugc(message.text.strip())

    if not items:
        await message.answer(_NOT_FOUND_TEXT)
        return
    await message.answer(_format_items(items), disable_web_page_preview=True)


@router.callback_query(RobloxSkillCallback.filter())
async def skill_stub(callback: CallbackQuery, callback_data: RobloxSkillCallback) -> None:
    """Заглушки: «Общение» подсказывает AI-чат, остальное — «в разработке»."""
    if callback_data.skill == RobloxSkill.CHAT:
        await callback.answer("Открой AI-чат: кнопка «🤖 AI» или /ai", show_alert=True)
        return
    title = SKILLS[callback_data.skill].title
    await callback.answer(_WIP_TEXT.format(title=title), show_alert=True)
