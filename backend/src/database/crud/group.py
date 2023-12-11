from typing import Optional

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from src.database.models import User, Group

async def get_group_by_id(database: AsyncSession, group_id: Optional[int]) -> Group:
    """get a group by id"""
    statement = select(Group).where(Group.group_id == group_id)
    results =  await database.exec(statement)
    return results.one()


async def make_group(database: AsyncSession, owner: User, name: str) -> Group:
    """Make a group"""
    group: Group = Group(name=name, owner_id=owner.user_id)
    group.users.append(owner)
    database.add(group)
    await database.commit()
    return group


async def edit_group_name(database: AsyncSession, group:Group, new_name: str) -> Group:
    """Edit the name of the group"""
    group.name = new_name
    database.add(group)
    await database.commit()
    return group


async def transfer_owner(database: AsyncSession, group: Group, new_owner: User) -> Group:
    """Transfer ownser ship of the group"""
    group.owner_id = new_owner.user_id
    database.add(group)
    await database.commit()
    return group


async def delete_group(database: AsyncSession, group: Group) -> None:
    """Delete the group"""
    await database.delete(group)
    await database.commit()


async def add_user(database: AsyncSession, group: Group, user: User) -> Group:
    """Add user to a group"""
    group.users.append(user)
    database.add(group)
    await database.commit()
    return group


async def remove_user(database: AsyncSession, group: Group, user: User) -> Group:
    """Remove user from a group"""
    group.users.remove(user)
    database.add(group)
    await database.commit()
    return group
