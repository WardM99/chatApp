"""The logic of groups"""
from typing import Optional
from fastapi import Depends

from sqlmodel.ext.asyncio.session import AsyncSession
from src.app.exceptions.alreadyingroup import AlreadyInGroupException
from src.app.exceptions.notingroup import NotInGroupException
from src.app.exceptions.wronguser import WrongUserException
from src.app.logic.users_logic import logic_get_user_by_id, require_user
from src.database.crud.group import (
    get_group_by_id,
    make_group,
    edit_group_name,
    transfer_owner,
    delete_group,
    add_user,
    remove_user,
)
from src.database.crud.user import get_user_by_name
from src.database.database import get_session
from src.database.models import User, Group

async def logic_make_new_group(
    database: AsyncSession,
    owner: User,
    name: str,
    private: bool = False
) -> Group:
    """Logic to make a new group"""
    return await make_group(database, owner, name, private=private)


async def logic_get_group_by_id(
    group_id: int,
    database: AsyncSession = Depends(get_session)
) -> Group:
    """Logic to get group by id"""
    return await get_group_by_id(database, group_id)


async def logic_edit_group_name(
        database: AsyncSession,
        user: User,
        group: Group,
        new_name:str
) -> None:
    """Logic to edit the group name"""
    if group.owner_id != user.user_id:
        raise WrongUserException
    await edit_group_name(database, group, new_name)


async def logic_tranfer_owner(
        database: AsyncSession,
        user: User, group: Group,
        new_owner_id
) -> None:
    """Logic of tranfering a group to another owner"""
    if group.owner_id != user.user_id:
        raise WrongUserException
    new_owner: User = await logic_get_user_by_id(database, new_owner_id)
    await transfer_owner(database, group, new_owner)


async def logic_delete_group(database: AsyncSession, user: User, group: Group) -> None:
    """Logic to delete a group"""
    if group.owner_id != user.user_id:
        raise WrongUserException
    await delete_group(database, group)


async def logic_add_user_by_name(
        database: AsyncSession,
        user: User, group: Group,
        new_user_name: str
) -> None:
    """Logic to add a user by name to a group"""
    if group.owner_id != user.user_id:
        raise WrongUserException
    new_user: User = await get_user_by_name(database, new_user_name)
    await add_user(database, group, new_user)


async def logic_add_user(database: AsyncSession, user: User, group: Group) -> Group:
    """Logic to add a user to a group"""
    if group.private and group.owner_id != user.user_id:
        raise WrongUserException
    if user in group.users:
        raise AlreadyInGroupException
    return await add_user(database, group, user)


async def logic_remove_user(
        database: AsyncSession,
        user: User,
        group: Group,
        user_remove_id: Optional[int]
) -> None:
    """Logic to remove a user"""
    if group.owner_id == user.user_id:
        user_remove: User = await logic_get_user_by_id(database, user_remove_id)
        await remove_user(database, group, user_remove)
    elif user.user_id == user_remove_id:
        await remove_user(database, group, user)
    else:
        raise WrongUserException


async def logic_user_in_group(
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
) -> User:
    """Logic to see if user is in the group"""
    if user not in group.users:
        raise NotInGroupException
    return user
