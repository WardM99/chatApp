"""The logic of users"""
from typing import Optional

from datetime import timedelta, datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import NoResultFound
from src.app.exceptions.wrongcredentials import WrongCredentialsException
from src.app.exceptions.wronguser import WrongUserException
from src.app.schemas.user import Token, ReturnUser, ReturnUserBasic
from src.database.database import get_session
from src.database.crud.user import (
    make_user,
    get_user_by_name,
    get_user_by_id,
    edit_user_password,
    edit_user_name,
    delete_user,
    change_status
)
from src.database.models import User

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def logic_make_new_user(database: AsyncSession, name: str, password: str) -> User:
    """logic to make a new user"""
    print(f"name: {name}")
    user: User = await make_user(database, name, pwd_context.hash(password))
    print(f"user: {user}")
    return user


async def logic_get_user_by_name(
    user_name: str,
    database: AsyncSession = Depends(get_session)
) -> User:
    """Logic to get user by name"""
    user: User = await get_user_by_name(database, user_name)
    return user


async def logic_get_user_by_name_and_password(database: AsyncSession,
                                              name: str,
                                              password: str) -> User:
    """Logic to get user by name and password"""
    try:
        user: User = await get_user_by_name(database, name)
        if verify_password(password, user.password):
            return user
        raise WrongCredentialsException
    except NoResultFound as exc:
        raise WrongCredentialsException from exc


async def logic_get_user_by_id(database: AsyncSession,
                               user_id: Optional[int]) -> User:
    """Logic to get user by id"""
    return await get_user_by_id(database, user_id)


async def logic_change_password(database: AsyncSession,
                                user: User,
                                user_id: int,
                                password: str):
    """Logic to change the password"""
    if user.user_id != user_id:
        raise WrongUserException
    await edit_user_password(database, user, pwd_context.hash(password))


async def logic_change_name(database: AsyncSession,
                            user: User,
                            user_id: int,
                            name: str
                        ):
    """Logic to change the name"""
    if user.user_id != user_id:
        raise WrongUserException
    await edit_user_name(database, user, name)


async def logic_change_status(database: AsyncSession,
                              user: User,
                              user_id: int,
                              new_status: Optional[str]
                            ) -> None:
    """logic to change the status of a user"""
    if user.user_id != user_id:
        raise WrongUserException
    await change_status(database, user, new_status)


async def logic_delete_user(database: AsyncSession,
                            user: User,
                            user_id: int):
    """Logic to delete the name"""
    if user.user_id != user_id:
        raise WrongUserException
    await delete_user(database, user)


async def logic_change_user(database: AsyncSession,
                            user: User,
                            user_id: int,
                            new_name: Optional[str],
                            new_password: Optional[str]):
    """Logic to change the user"""
    if user.user_id != user_id:
        raise WrongUserException
    if new_name:
        await edit_user_name(database, user, new_name)
    if new_password:
        await edit_user_password(database, user, new_password)

async def user_to_return_user_basic(user: User) -> ReturnUserBasic:
    """logic to make a ReturnUser from a User"""
    return ReturnUserBasic(
        user_id=user.user_id,
        name=user.name,
        status=user.status
    )

async def user_to_return_user(user: User) -> ReturnUser:
    """logic to make a ReturnUser from a User"""
    return ReturnUser(
        user_id=user.user_id,
        name=user.name,
        status=user.status,
        groups=user.groups
    )

async def logic_generate_token(user: User) -> Token:
    """The logic to create a token"""
    access_token = create_token(user)
    return_user: ReturnUser = await user_to_return_user(user)
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=return_user
    )


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_token(user: User):
    """Create an access token"""
    data: dict = {"type": "access", "sub": str(user.user_id)}
    data["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(
        data,
        "WPll6MnvmR1NLf7x6jszNNXlQUwhqpKIyIUyQdg3zio7ngodp82FRbh1JM4UO5qZ",
        algorithm=ALGORITHM
    )


async def get_user_from_access_token(
    database: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme)
) -> User:
    """Get the user from an access token"""
    print(f"token: {token}")
    payload = jwt.decode(
        token,
        "WPll6MnvmR1NLf7x6jszNNXlQUwhqpKIyIUyQdg3zio7ngodp82FRbh1JM4UO5qZ",
        algorithms="HS256"
    )
    print(f"payload: {payload}")
    user_id: int | None = payload.get("sub")
    type_in_token: int | None = payload.get("type")
    if user_id is None or type_in_token is None:
        raise JWTError()

    user: User = await get_user_by_id(database, int(user_id))
    return user


async def require_user(user: User = Depends(get_user_from_access_token)) -> User:
    """Require a user to be logged in"""
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify that a password matches a hash found in the database"""
    return pwd_context.verify(plain_password, hashed_password)
