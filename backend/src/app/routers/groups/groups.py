"""Router groups"""
from asyncio import Queue
from fastapi import APIRouter, Depends, WebSocket
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from websockets.exceptions import ConnectionClosedOK

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
from src.app.utils.websockets import (
    DataPublisher,
    get_publisher,
    live
)
from src.database.database import get_session
from src.database.models import User, Group

from .messages import message_router

group_router = APIRouter(prefix="/groups")
group_router.include_router(message_router, prefix="/{group_id}")

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
    return await logic_make_new_group(database, user, new_group.name, private=new_group.private)


@group_router.get(
    "/{group_id}",
    status_code=status.HTTP_200_OK,
    response_model=ReturnGroup,
    dependencies=[Depends(require_user), Depends(live)]
)
async def get_group_by_id(
    group: Group = Depends(logic_get_group_by_id)
):
    """get group by id"""
    return group


@group_router.patch(
    "/{group_id}/name",
    status_code=status.HTTP_204_NO_CONTENT
)
async def change_group_name(
    new_group: ChangeGroup,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """change the group name"""
    await logic_edit_group_name(database, user, group, new_group.name)


@group_router.patch(
    "/{group_id}/ownership",
    status_code=status.HTTP_204_NO_CONTENT
)
async def transfer_ownership(
    new_owner: NewOwner,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """transfer ownership"""
    await logic_tranfer_owner(database, user, group, new_owner.user_id)


@group_router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group(
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """delete a group"""
    await logic_delete_group(database, user, group)


@group_router.post(
    "/{group_id}/user",
    status_code=status.HTTP_201_CREATED,
    response_model=ReturnGroup,
    dependencies=[Depends(live)]
)
async def add_user(
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """add user to a group"""
    return await logic_add_user(database, user, group)


@group_router.patch(
    "/{group_id}/user",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(live)]
)
async def remove_user_as_owner(
    user_remove: RemoveUser,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """remove a user from a group as an owner"""
    await logic_remove_user(database, user, group, user_remove.user_id)


@group_router.delete(
    "/{group_id}/user",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(live)]
)
async def remove_user(
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """remove a user from a group"""
    await logic_remove_user(database, user, group, user.user_id)


@group_router.put(
    "/{group_id}/username",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(live)]
)
async def add_user_by_name(
    new_user: AddUserName,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user),
    group: Group = Depends(logic_get_group_by_id)
):
    """add a user to a group by name"""
    await logic_add_user_by_name(database, user, group, new_user.user_name)


@group_router.websocket(
    "/{group_id}/live"
)
async def feed(
    websocket: WebSocket,
    publisher: DataPublisher = Depends(get_publisher)
):
    """Handle websocket"""
    await websocket.accept()
    queue: Queue = await publisher.subscribe()
    try:
        while True:
            data: dict = await queue.get()
            await websocket.send_json(data)
    except ConnectionClosedOK:
        pass
    finally:
        await publisher.unsubscribe(queue)
