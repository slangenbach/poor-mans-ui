"""Database."""

from dataclasses import dataclass

from fastlite import database


@dataclass
class ChatSchema:
    """Schema for chat table."""

    id: int = 0
    title: str = ""
    created_at: str = ""


@dataclass
class MessageSchema:
    """Schema for message table."""

    id: int = 0
    chat_id: int = 0
    role: str = ""
    content: str = ""
    timestamp: str = ""


db = database("test.db")
chats = db.create(ChatSchema, pk="id")
messages = db.create(MessageSchema, pk="id")
