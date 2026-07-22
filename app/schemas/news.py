"""Схемы новостей — DTO, независимые от источника (RSS, API и т.п.)."""

from pydantic import BaseModel


class NewsItem(BaseModel):
    """Одна новость."""

    title: str
    url: str
    published: str = ""
