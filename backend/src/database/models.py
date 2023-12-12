"""Models"""

from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class UserGroupLink(SQLModel, table=True):
    """Model to link User and Group"""
    user_id: int = Field(foreign_key="user.user_id", primary_key=True)
    group_id: int = Field(foreign_key="group.group_id", primary_key=True)


class User(SQLModel, table=True):
    """Model User"""
    user_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False)

    groups: List["Group"] = Relationship(
        back_populates="users",
        link_model=UserGroupLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Group(SQLModel, table=True):
    """Model Group"""
    group_id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)
    owner_id: Optional[int] = Field(foreign_key="user.user_id", index=True)

    users: List[User] = Relationship(
        back_populates="groups",
        link_model=UserGroupLink,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Message(SQLModel, table=True):
    """Model Message"""
    message_id: Optional[int] = Field(default=None, primary_key=True)
    message: str = Field(nullable=False)
    sender_id: int = Field(foreign_key="user.user_id", index=True)
    reply_id: Optional[int] = Field(default=None, foreign_key="message.message_id")
    group_id: int = Field(foreign_key="group.group_id", index=True)
