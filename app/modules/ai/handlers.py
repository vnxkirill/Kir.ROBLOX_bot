"""Telegram-хендлеры AI-чата.

Вход — кнопка «🤖 AI» (reply или inline) либо команда /ai. Внутри чата
каждое текстовое сообщение уходит в AIService вместе с историей диалога
(хранится в FSM). Выход — кнопка «Выйти» или /menu (глобальный хендлер).
"""

from aiogram import F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.container import Container
from app.keyboards import MainMenuButton, main_reply_keyboard
from app.keyboards.main_menu import MainMenuAction, MainMenuCallback, main_menu_keyboard
from app.modules.ai.service import AIService
from app.modules.ai.states import AIChat
from app.schemas.ai import ChatMessage

router = Router(name="ai")

# Сколько последних сообщений истории отправлять модели (пар вопрос-ответ ×2).
_HISTORY_LIMIT = 20

_CHAT_INTRO = (
    "🤖 <b>AI-чат</b>\n\n"
    "Пиши мне что угодно — отвечу. Контекст диалога сохраняется.\n"
    "Выйти: кнопка ниже или /menu."
)
_NO_KEY_TEXT = (
    "🔑 AI-чат не настроен: не задан OPENROUTER_API_KEY в .env.\n"
    "Получить ключ: https://openrouter.ai/keys"
)
_EXIT_TEXT = "👋 Вышли из AI-чата."


class AIChatCallback(CallbackData, prefix="ai"):
    action: str


def _chat_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="🧹 Очистить контекст", callback_data=AIChatCallback(action="clear"))
    builder.button(text="🚪 Выйти", callback_data=AIChatCallback(action="exit"))
    builder.adjust(2)
    return builder.as_markup()


@router.message(Command("ai"))
@router.message(F.text == MainMenuButton.AI)
async def enter_ai_chat_message(
    message: Message, state: FSMContext, container: Container
) -> None:
    """Вход в AI-чат по reply-кнопке или команде /ai."""
    if not container.settings.openrouter.api_key.get_secret_value():
        await message.answer(_NO_KEY_TEXT)
        return

    await state.set_state(AIChat.chatting)
    await state.update_data(history=[])
    await message.answer(_CHAT_INTRO, reply_markup=_chat_keyboard())


@router.callback_query(MainMenuCallback.filter(F.action == MainMenuAction.AI))
async def enter_ai_chat(
    callback: CallbackQuery, state: FSMContext, container: Container
) -> None:
    """Вход в AI-чат по inline-кнопке."""
    if not container.settings.openrouter.api_key.get_secret_value():
        await callback.message.edit_text(_NO_KEY_TEXT, reply_markup=main_menu_keyboard())
        await callback.answer()
        return

    await state.set_state(AIChat.chatting)
    await state.update_data(history=[])
    await callback.message.edit_text(_CHAT_INTRO, reply_markup=_chat_keyboard())
    await callback.answer()


@router.callback_query(AIChatCallback.filter(F.action == "clear"), AIChat.chatting)
async def clear_context(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(history=[])
    await callback.answer("🧹 Контекст очищен")


@router.callback_query(AIChatCallback.filter(F.action == "exit"))
async def exit_ai_chat(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(_EXIT_TEXT)
    await callback.message.answer(
        "Ты в главном меню.", reply_markup=main_reply_keyboard()
    )
    await callback.answer()


@router.message(AIChat.chatting, F.text)
async def chat_message(message: Message, state: FSMContext, container: Container) -> None:
    service = container.get(AIService)

    data = await state.get_data()
    history = [ChatMessage.model_validate(m) for m in data.get("history", [])]

    await message.bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    response = await service.chat(message.text, history)

    history.append(ChatMessage.user(message.text))
    history.append(ChatMessage.assistant(response.content))
    await state.update_data(
        history=[m.model_dump(mode="json") for m in history[-_HISTORY_LIMIT:]]
    )

    await message.answer(response.content)
