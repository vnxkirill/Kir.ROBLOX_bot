"""Конфигурация приложения.

Единственный источник настроек — переменные окружения (или файл .env).
Каждая подсистема имеет собственную группу настроек со своим префиксом,
поэтому новые модули добавляют свои настройки, не трогая чужие.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

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
    owner_id: int


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
