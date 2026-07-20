"""Меню навыков Roblox.

Навык = будущая возможность модуля. ready=True — навык работает,
False — показывается как «в разработке». Включение навыка = смена
флага + свой хендлер.
"""

from dataclasses import dataclass
from enum import StrEnum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class RobloxSkill(StrEnum):
    CHAT = "chat"
    UGC_SEARCH = "ugc"
    NEWS = "news"
    PLAYER_CHECK = "players"
    GAME_SEARCH = "games"
    AVATAR_ANALYSIS = "avatar"
    IMAGE_SEARCH = "image"
    REMINDERS = "reminders"
    QUESTS = "quests"
    TOURNAMENTS = "tournaments"


class RobloxSkillCallback(CallbackData, prefix="rbx"):
    skill: RobloxSkill


@dataclass(frozen=True)
class SkillInfo:
    title: str
    ready: bool


SKILLS: dict[RobloxSkill, SkillInfo] = {
    RobloxSkill.CHAT: SkillInfo("Общение", ready=True),
    RobloxSkill.UGC_SEARCH: SkillInfo("Поиск Roblox UGC", ready=True),
    RobloxSkill.NEWS: SkillInfo("Новости Roblox", ready=False),
    RobloxSkill.PLAYER_CHECK: SkillInfo("Проверка игроков", ready=False),
    RobloxSkill.GAME_SEARCH: SkillInfo("Поиск игр", ready=False),
    RobloxSkill.AVATAR_ANALYSIS: SkillInfo("Анализ аватара", ready=False),
    RobloxSkill.IMAGE_SEARCH: SkillInfo("Поиск по картинке", ready=False),
    RobloxSkill.REMINDERS: SkillInfo("Напоминания", ready=False),
    RobloxSkill.QUESTS: SkillInfo("Квесты", ready=False),
    RobloxSkill.TOURNAMENTS: SkillInfo("Турниры", ready=False),
}


def skills_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for skill, info in SKILLS.items():
        mark = "✅" if info.ready else "⬜"
        builder.button(
            text=f"{mark} {info.title}",
            callback_data=RobloxSkillCallback(skill=skill),
        )
    builder.adjust(2)
    return builder.as_markup()
