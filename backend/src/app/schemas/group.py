"""Schemas for groups"""
from typing import Optional, List

from fastapi_camelcase import CamelModel

class GroupCreate(CamelModel):
    """Schema to create a group"""
    name: str
    is_private: bool = False


class ReturnUserBasic(CamelModel):
    """Basic schema to return a user"""
    user_id: Optional[int]
    name: str
    status: Optional[str]


class ReturnGroupBasic(CamelModel):
    """Basic schema to return a group"""
    group_id: Optional[int]
    name: str
    is_private: bool


class ReturnGroup(ReturnGroupBasic):
    """Schema to return a group"""
    users: List[ReturnUserBasic]
    owner_id: Optional[int]
    owner: ReturnUserBasic


class ChangeGroup(CamelModel):
    """Schema to change the groups name"""
    name: str


class NewOwner(CamelModel):
    """Schema to transfer ownership"""
    user_id: Optional[int]


class RemoveUser(CamelModel):
    """Schema to remove a user to the group"""
    user_id: Optional[int]


class AddUserName(CamelModel):
    """Schema to add a user by name"""
    user_name: str
