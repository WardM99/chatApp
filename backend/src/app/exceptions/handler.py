"""Handlers for the exceptions"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound, IntegrityError
from jose import ExpiredSignatureError, JWTError
from starlette import status

from src.app.exceptions.alreadyingroup import AlreadyInGroupException
from src.app.exceptions.wrongcredentials import WrongCredentialsException
from src.app.exceptions.wronguser import WrongUserException
from src.app.exceptions.notingroup import NotInGroupException

def install_handlers(app: FastAPI): # pragma: no cover
    """Intall all custom exception handlers"""

    @app.exception_handler(NoResultFound)
    def no_result_found(_request: Request, _exception: NoResultFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Not Found"}
        )


    @app.exception_handler(IntegrityError)
    def integrity_error(_request: Request, _exception: IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Bad Request"}
        )


    @app.exception_handler(ExpiredSignatureError)
    def expired_signature_error(_request: Request, _exception: ExpiredSignatureError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "Credentials are expired"}
        )


    @app.exception_handler(JWTError)
    def jwt_error(_request: Request, _exception: JWTError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "You are not authorized for this"}
        )

    @app.exception_handler(WrongUserException)
    def wrong_user_exception(_request: Request, _exception: WrongUserException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "You are not authorized for this"}
        )


    @app.exception_handler(WrongCredentialsException)
    def wrong_credentials_error(_request: Request, _exception: WrongCredentialsException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "You are not authorized for this"}
        )


    @app.exception_handler(NotInGroupException)
    def not_in_group_error(_request: Request, _exception: NotInGroupException):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": "You are not a member of this group"}
        )


    @app.exception_handler(AlreadyInGroupException)
    def already_in_group_error(_request: Request, _exception: AlreadyInGroupException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"message": "You are already a member of this group"}
        )


    @app.exception_handler(Exception)
    def something_wrong(_request: Request, _exception: Exception):
        return JSONResponse(
            status_code=500,
            content={"messgae": "Somthing's wrong. I CAN FEEL IT"}
        )
