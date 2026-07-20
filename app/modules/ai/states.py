"""FSM-состояния AI-чата."""

from aiogram.fsm.state import State, StatesGroup


class AIChat(StatesGroup):
    chatting = State()
