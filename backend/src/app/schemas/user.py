"""Schemas of users"""
from typing import Optional, List

from sqlmodel import SQLModel
from src.app.schemas.group import ReturnGroupBasic, ReturnUserBasic


class UserCreate(SQLModel):
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


class ReturnUsers(SQLModel):
    """Represents multiple users"""
    users: List[ReturnUser]


class ChangePassword(SQLModel):
    """Schema to change password"""
    password: str


class ChangeName(SQLModel):
    """Schema to change name"""
    name: str


class ChangeUser(SQLModel):
    """Schema to change user"""
    name: Optional[str]
    password: Optional[str]


class ChangeStatus(SQLModel):
    """Schema to change status"""
    status: Optional[str]
