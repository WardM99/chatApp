from typing import Union

from fastapi import FastAPI
from sqlmodel import SQLModel
from src.app.exceptions.handler import install_handlers
from src.app.routers import user_router
from src.database.database import engine


app = FastAPI()

install_handlers(app)

app.include_router(user_router)


@app.on_event("startup")
async def startup():
    """creating the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
