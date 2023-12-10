from typing import Union

from fastapi import FastAPI
from sqlmodel import SQLModel
from src.database.database import engine

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)