"""Schemas of users"""
from typing import Optional, List

from fastapi_camelcase import CamelModel
from sqlmodel import SQLModel
from src.app.schemas.group import ReturnGroupBasic, ReturnUserBasic


class UserCreate(CamelModel):
    """Schema to create a user"""
    name: str
    password: str


class ReturnUser(ReturnUserBasic):
    """Represents a user"""
    groups: List[ReturnGroupBasic]


class Token(SQLModel):
    """Token generated after the user is created or loged in"""
    access_token: str
    token_type: str
    user: ReturnUser


class ReturnUsers(CamelModel):
    """Represents multiple users"""
    users: List[ReturnUser]


class ChangePassword(CamelModel):
    """Schema to change password"""
    password: str


class ChangeName(CamelModel):
    """Schema to change name"""
    name: str


class ChangeUser(CamelModel):
    """Schema to change user"""
    name: Optional[str]
    password: Optional[str]


class ChangeStatus(CamelModel):
    """Schema to change status"""
    status: Optional[str]
