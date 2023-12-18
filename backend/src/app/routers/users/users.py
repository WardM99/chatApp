"""User routers"""
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from src.app.logic.users_logic import (
    logic_make_new_user,
    logic_generate_token,
    logic_get_user_by_name_and_password,
    require_user,
    logic_get_user_by_id,
    logic_change_name,
    logic_change_password,
    logic_delete_user,
    logic_change_user
)
from src.app.schemas.user import (
    UserCreate,
    Token,
    ReturnUser,
    ChangePassword,
    ChangeName,
    ChangeUser
)
from src.database.database import get_session
from src.database.models import User




user_router = APIRouter(prefix="/users")


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=Token)
async def route_new_user(new_user: UserCreate, database: AsyncSession = Depends(get_session)):
    """make a new user"""
    return await logic_generate_token(
        await logic_make_new_user(database, new_user.name, new_user.password)
    )


@user_router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                database: AsyncSession = Depends(get_session)):
    """Login a user"""
    return await logic_generate_token(
        await logic_get_user_by_name_and_password(
            database,
            form_data.username,
            form_data.password
        )
    )


@user_router.get("/{user_id}",
                 dependencies=[Depends(require_user)],
                 response_model=ReturnUser)
async def get_user(user_id: int, database: AsyncSession = Depends(get_session)):
    """get user"""
    return await logic_get_user_by_id(database, user_id)


@user_router.patch("/{user_id}/password",
                   status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user_id: int,
    password: ChangePassword,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """change password"""
    await logic_change_password(database, user, user_id, password.password)

@user_router.patch("/{user_id}/name",
                   status_code=status.HTTP_204_NO_CONTENT)
async def change_name(
    user_id: int,
    name: ChangeName,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """change name"""
    await logic_change_name(database, user, user_id, name.name)


@user_router.put("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_user(
    user_id: int,
    new_user: ChangeUser,
    database = Depends(get_session),
    user: User = Depends(require_user)
):
    """Change a user"""
    await logic_change_user(database, user, user_id, new_user.name, new_user.password)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    database: AsyncSession = Depends(get_session),
    user: User = Depends(require_user)
):
    """delete user"""
    await logic_delete_user(database, user, user_id)
