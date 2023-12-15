"""Schemas for groups"""
from typing import Optional, List

from sqlmodel import SQLModel
from src.app.schemas.user import ReturnUser

class GroupCreate(SQLModel):
    """Schema to create a group"""
    name: str


class ReturnGroup(SQLModel):
    """Schema to return a group"""
    group_id: Optional[int]
    name: str
    users: List[ReturnUser]
    owner_id: Optional[int]


class ChangeGroup(SQLModel):
    """Schema to change the groups name"""
    name: str


class NewOwner(SQLModel):
    """Schema to transfer ownership"""
    user_id: Optional[int]


class RemoveUser(SQLModel):
    """Schema to remove a user to the group"""
    user_id: Optional[int]


class AddUserName(SQLModel):
    """Schema to add a user by name"""
    user_name: str
