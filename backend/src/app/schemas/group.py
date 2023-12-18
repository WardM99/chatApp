"""Schemas for groups"""
from typing import Optional, List

from sqlmodel import SQLModel

class GroupCreate(SQLModel):
    """Schema to create a group"""
    name: str


class ReturnUserBasic(SQLModel):
    """Basic schema to return a user"""
    user_id: Optional[int]
    name: str


class ReturnGroupBasic(SQLModel):
    """Basic schema to return a group"""
    group_id: Optional[int]
    name: str


class ReturnGroup(ReturnGroupBasic):
    """Schema to return a group"""
    users: List[ReturnUserBasic]
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
