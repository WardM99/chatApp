"""Schemas for messages"""
from typing import Optional, List
from sqlmodel import SQLModel


class WriteMessage(SQLModel):
    """Schema to write a message"""
    message: str
    reply_id: Optional[int]


class ReturnMessage(SQLModel):
    """Schema to return a message"""
    message_id: Optional[int]
    message: str
    sender_id: int
    reply_id: Optional[int]
    group_id: int


class ReturnMessages(SQLModel):
    """Schema to return multiple messages"""
    messages: List[ReturnMessage]
