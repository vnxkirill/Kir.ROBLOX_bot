"""Fallback: любое текстовое сообщение вне разделов — это разговор с AI.

Пишешь боту «привет» — он сразу переходит в режим общения, без кнопок.
Роутер подключается ПОСЛЕДНИМ (см. app/routers/root.py), поэтому кнопки
меню и команды обрабатываются раньше и сюда не попадают.
"""

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.core.container import Container
from app.modules.ai.handlers import chat_message
from app.modules.ai.states import AIChat

fallback_router = Router(name="ai-fallback")


@fallback_router.message(F.text, ~F.text.startswith("/"))
async def any_text_starts_chat(
    message: Message, state: FSMContext, container: Container
) -> None:
    """Первое сообщение вне разделов: включаем режим общения и сразу отвечаем."""
    if not container.settings.openrouter.api_key.get_secret_value():
        return  # AI не настроен — молчим, пусть работают только кнопки

    await state.set_state(AIChat.chatting)
    await state.update_data(history=[])
    await chat_message(message, state, container)
