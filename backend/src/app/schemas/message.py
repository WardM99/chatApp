"""Schemas for messages"""
from typing import Optional, List

from fastapi_camelcase import CamelModel
from src.app.schemas.group import ReturnUserBasic, ReturnGroupBasic

class WriteMessage(CamelModel):
    """Schema to write a message"""
    message: str
    reply_id: Optional[int] = None


class ReturnMessageBasic(CamelModel):
    """Basic schema to return a message"""
    message_id: Optional[int]
    message: str
    sender_id: int
    sender: ReturnUserBasic


class ReturnMessage(ReturnMessageBasic):
    """Schema to return a message"""
    group_id: int
    group: ReturnGroupBasic
    reply_id: Optional[int] = None
    reply: Optional[ReturnMessageBasic] = None


class ReturnMessages(CamelModel):
    """Schema to return multiple messages"""
    messages: List[ReturnMessage]
