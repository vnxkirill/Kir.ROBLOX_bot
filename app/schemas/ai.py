"""Схемы AI-слоя — провайдеро-независимые DTO.

Сервисы и хендлеры работают с этими типами, а не с сырым JSON
конкретного API.
"""

from enum import StrEnum

from pydantic import BaseModel


class ChatRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(BaseModel):
    role: ChatRole
    content: str

    @classmethod
    def system(cls, content: str) -> "ChatMessage":
        return cls(role=ChatRole.SYSTEM, content=content)

    @classmethod
    def user(cls, content: str) -> "ChatMessage":
        return cls(role=ChatRole.USER, content=content)

    @classmethod
    def assistant(cls, content: str) -> "ChatMessage":
        return cls(role=ChatRole.ASSISTANT, content=content)


class ChatUsage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


class ChatResponse(BaseModel):
    content: str
    model: str
    usage: ChatUsage = ChatUsage()
