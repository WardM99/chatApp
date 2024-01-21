"""The application"""
from contextlib import asynccontextmanager
from environs import Env
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from src.app.exceptions.handler import install_handlers
from src.app.routers import user_router, group_router
from src.app.utils.websockets import install_middleware
from src.database.database import engine

@asynccontextmanager
async def lifespan(_app: FastAPI): # pragma: no cover
    """lifespan"""
    print("lifespan start")
    await startup()
    yield
    # Clean up the ML models and release the resources
    print("lifespan end")

app = FastAPI(
    title="ChatApp",
    version="0.0.1",
    lifespan=lifespan
)

env = Env()
CORS_ORIGINS: list[str] = env.list(
    "CORS_ORIGINS",
    ["http://localhost:3000", "http://localhost:5173" ]
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
install_middleware(app)


install_handlers(app)


app.include_router(user_router)
app.include_router(group_router)


async def startup():
    """creating the database"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
