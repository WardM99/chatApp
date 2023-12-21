"""Schemas for messages"""
from typing import Optional, List
from sqlmodel import SQLModel
from src.app.schemas.group import ReturnUserBasic, ReturnGroupBasic

class WriteMessage(SQLModel):
    """Schema to write a message"""
    message: str
    reply_id: Optional[int]


class ReturnMessageBasic(SQLModel):
    """Basic schema to return a message"""
    message_id: Optional[int]
    message: str
    sender_id: int
    sender: ReturnUserBasic


class ReturnMessage(ReturnMessageBasic):
    """Schema to return a message"""
    group_id: int
    group: ReturnGroupBasic
    reply_id: Optional[int]
    reply: Optional[ReturnMessageBasic] = None


class ReturnMessages(SQLModel):
    """Schema to return multiple messages"""
    messages: List[ReturnMessage]
