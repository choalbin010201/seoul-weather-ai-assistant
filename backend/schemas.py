from datetime import date as Date
from typing import Literal
from pydantic import BaseModel, Field


class DataCreate(BaseModel):
    date: Date
    value: float
    memo: str = Field(default="", max_length=300)


class DataUpdate(BaseModel):
    date: Date | None = None
    value: float | None = None
    memo: str | None = Field(default=None, max_length=300)


class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)


class ConversationCreate(BaseModel):
    title: str = Field(default="새 대화", max_length=100)
    messages: list[Message] = Field(default_factory=list)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    conversation_id: str | None = None