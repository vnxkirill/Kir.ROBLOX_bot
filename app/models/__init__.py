"""ORM-модели приложения.

Важно: каждый новый файл модели нужно импортировать здесь,
чтобы Alembic видел его при автогенерации миграций.
"""

from app.models.friend_listing import FriendListing
from app.models.user import User

__all__ = ["FriendListing", "User"]
