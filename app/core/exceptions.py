"""Иерархия исключений приложения.

Все свои ошибки наследуются от AppError — глобальный обработчик
отличает «ожидаемые» ошибки домена от неожиданных сбоев.
"""


class AppError(Exception):
    """Базовая ошибка приложения. user_message показывается пользователю."""

    user_message: str = "⚠️ Что-то пошло не так. Попробуй ещё раз."

    def __init__(self, message: str | None = None, *, user_message: str | None = None) -> None:
        super().__init__(message or self.__class__.__name__)
        if user_message is not None:
            self.user_message = user_message


class NotFoundError(AppError):
    """Запрошенная сущность не найдена."""

    user_message = "🔍 Ничего не найдено."


class ExternalServiceError(AppError):
    """Внешний API (OpenRouter, Roblox и т.п.) вернул ошибку или недоступен."""

    user_message = "🌐 Внешний сервис временно недоступен. Попробуй позже."
