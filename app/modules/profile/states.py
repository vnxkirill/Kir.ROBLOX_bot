"""FSM-состояния модуля «Профиль»."""

from aiogram.fsm.state import State, StatesGroup


class ProfileEdit(StatesGroup):
    waiting_nickname = State()
