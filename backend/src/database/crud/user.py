"""CRUD operations of user"""
from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database.models import User

async def get_user_by_id(database: AsyncSession, user_id: Optional[int]) -> User:
    """Get the user be by id"""
    statement = select(User).where(User.user_id == user_id)
    results = await database.exec(statement)
    return results.one()


async def make_user(database: AsyncSession, name: str, password: str) -> User:
    """Make a new user"""
    if len(password) <= 0:
        raise ValueError("Password can't be empty")

    if len(name) <= 0:
        raise ValueError("Password can't be empty")

    user: User = User(name=name, password=password, groups=[])
    database.add(user)
    await database.commit()
    return user


async def change_status(database: AsyncSession, user: User, new_status: Optional[str]) -> User:
    """Change the status of a user"""
    user.status = new_status
    database.add(user)
    await database.commit()
    return user


async def edit_user_password(database: AsyncSession, user: User, new_password: str) -> User:
    """Update a user's password"""
    user.password = new_password
    database.add(user)
    await database.commit()
    return user


async def edit_user_name(database: AsyncSession, user: User, new_name: str) -> User:
    """Update a user's name"""
    user.name = new_name
    database.add(user)
    await database.commit()
    return user


async def delete_user(database: AsyncSession, user: User) -> None:
    """Delete a user"""
    await database.delete(user)
    await database.commit()


async def get_user_by_name(database: AsyncSession, name: str) -> User:
    """Get the user by name"""
    statement = select(User).where(User.name == name)
    results = await database.exec(statement)
    return results.one()
