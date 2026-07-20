"""FSM-состояния модуля Roblox."""

from aiogram.fsm.state import State, StatesGroup


class UGCSearch(StatesGroup):
    waiting_query = State()
