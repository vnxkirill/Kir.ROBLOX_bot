"""Реестр модулей приложения.

Единственное место, где перечислены активные модули.
Добавить возможность = дописать одну строку.
"""

from app.core.module import AppModule
from app.modules.ai import AIModule
from app.modules.community import CommunityModule
from app.modules.fnf import FnfModule
from app.modules.news import NewsModule
from app.modules.premium import PremiumModule
from app.modules.profile import ProfileModule
from app.modules.roblox import RobloxModule


def get_modules() -> list[AppModule]:
    return [
        AIModule(),
        RobloxModule(),
        FnfModule(),
        NewsModule(),
        ProfileModule(),
        CommunityModule(),
        PremiumModule(),
    ]
