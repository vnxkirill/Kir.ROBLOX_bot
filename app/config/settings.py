"""Конфигурация приложения.

Единственный источник настроек — переменные окружения (или файл .env).
Каждая подсистема имеет собственную группу настроек со своим префиксом,
поэтому новые модули добавляют свои настройки, не трогая чужие.
"""

from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

_ENV_FILE = ".env"


class _GroupSettings(BaseSettings):
    """База для групп настроек: читает .env, игнорирует чужие ключи."""

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )


class BotSettings(_GroupSettings):
    """Настройки Telegram-бота (префикс BOT_)."""

    model_config = SettingsConfigDict(env_prefix="BOT_")

    token: SecretStr
    # Владелец — главный админ проекта.
    owner_id: int
    # Дополнительные админы: BOT_ADMIN_IDS="123,456" (через запятую).
    admin_ids: Annotated[list[int], NoDecode] = Field(default_factory=list)

    @field_validator("admin_ids", mode="before")
    @classmethod
    def _parse_admin_ids(cls, value: object) -> object:
        if isinstance(value, str):
            return [int(part) for part in value.replace(",", " ").split()]
        return value

    @property
    def all_admin_ids(self) -> set[int]:
        """Все админы: владелец + список из BOT_ADMIN_IDS."""
        return {self.owner_id, *self.admin_ids}


class DatabaseSettings(_GroupSettings):
    """Настройки базы данных (префикс DATABASE_).

    Смена SQLite на PostgreSQL — это смена одной строки DATABASE_URL,
    остальной код не меняется.
    """

    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    url: str = "sqlite+aiosqlite:///./gamecore.db"
    echo: bool = False


class OpenRouterSettings(_GroupSettings):
    """Настройки OpenRouter (префикс OPENROUTER_)."""

    model_config = SettingsConfigDict(env_prefix="OPENROUTER_")

    api_key: SecretStr = SecretStr("")
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "openai/gpt-4o-mini"
    timeout_seconds: float = 60.0


class LogSettings(_GroupSettings):
    """Настройки логирования (префикс LOG_)."""

    model_config = SettingsConfigDict(env_prefix="LOG_")

    level: str = "INFO"
    dir: Path = Path("logs")
    rotation: str = "10 MB"
    retention: str = "30 days"


class Settings(BaseSettings):
    """Корневые настройки приложения — композиция групп."""

    bot: BotSettings = Field(default_factory=BotSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    openrouter: OpenRouterSettings = Field(default_factory=OpenRouterSettings)
    log: LogSettings = Field(default_factory=LogSettings)


@lru_cache
def get_settings() -> Settings:
    """Вернуть настройки приложения (кешируются на весь процесс)."""
    return Settings()
