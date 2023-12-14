"""Router groups"""
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status

from src.app.logic.groups_logic import (
    logic_add_user,
    logic_add_user_by_name,
    logic_delete_group,
    logic_edit_group_name,
    logic_get_group_by_id,
    logic_make_new_group,
    logic_remove_user,
    logic_tranfer_owner
)
from src.app.logic.users_logic import (
    require_user
)
from src.app.schemas.group import(
    ReturnGroup,
    RemoveUser,
    GroupCreate,
    ChangeGroup,
    NewOwner,
    AddUserName
)
from src.database.database import get_session
from src.database.models import User, Group

group_router = APIRouter(prefix="/groups")

@group_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnGroup
)
async def make_group(
    new_group: GroupCreate,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """make a new group"""
    return await logic_make_new_group(database, user, new_group.name)


@group_router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReturnGroup,
    dependencies=[Depends(require_user)]
)
async def get_group_by_id(
    group_id: int,
    database: AsyncSession = Depends(get_session)
):
    """get group by id"""
    return await logic_get_group_by_id(database, group_id)


@group_router.patch(
    "/{group_id}/name",
    status_code=status.HTTP_204_NO_CONTENT
)
async def change_group_name(
    group_id: int,
    new_group: ChangeGroup,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """change the group name"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_edit_group_name(database, user, group, new_group.name)


@group_router.patch(
    "/{group_id}/ownership",
    status_code=status.HTTP_204_NO_CONTENT
)
async def transfer_ownership(
    group_id: int,
    new_owner: NewOwner,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """transfer ownership"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_tranfer_owner(database, user, group, new_owner.user_id)


@group_router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group(
    group_id: int,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """delete a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_delete_group(database, user, group)


@group_router.put(
    "/{group_id}/user",
    status_code=status.HTTP_204_NO_CONTENT
)
async def add_user(
    group_id: int,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """add user to a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_add_user(database, user, group)


@group_router.delete(
    "/{group_id}/user",
    status_code=status.HTTP_204_NO_CONTENT
)
async def remove_user(
    group_id: int,
    user_remove: RemoveUser,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """remove a user from a group"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_remove_user(database, user, group, user_remove.user_id)


@group_router.put(
    "/{group_id}/username",
    status_code=status.HTTP_204_NO_CONTENT
)
async def add_user_by_name(
    group_id: int,
    new_user: AddUserName,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """add a user to a group by name"""
    group: Group = await logic_get_group_by_id(database, group_id)
    await logic_add_user_by_name(database, user, group, new_user.user_name)
