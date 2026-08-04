"""Каталог мини-игр площадки.

Единственное место со списком игр: добавить игру = дописать GameInfo.
Сами игры живут в docs/games/ (статические HTML5, хостятся на GitHub Pages).
"""

from dataclasses import dataclass

# Базовый URL мини-аппа (GitHub Pages из папки docs/).
GAMES_BASE_URL = "https://vnxkirill.github.io/Kir.ROBLOX_bot/games"


@dataclass(frozen=True)
class GameInfo:
    """Игра площадки: слаг = папка в docs/games/."""

    slug: str
    title: str
    description: str
    ready: bool = False

    @property
    def url(self) -> str:
        return f"{GAMES_BASE_URL}/{self.slug}/"


GAMES: list[GameInfo] = [
    GameInfo(
        slug="runner",
        title="🏃 Roblox Runner",
        description="Перепрыгивай кубики — чем дальше, тем быстрее!",
        ready=True,
    ),
    GameInfo(
        slug="fnf-beat",
        title="🎤 FNF Beat Battle",
        description="Классика со стрелками + битва с ботом на 26 нот-букв!",
        ready=True,
    ),
]
