from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config.database import AsyncSessionLocal
from app.middleware.user_log import UserLoggerMiddleware
from app.routes.auth import auth_route
from app.routes.files import files
from app.routes.logs import logs_router
from app.routes.main import main_page
from app.routes.user_profile import profile
from app.utils.init_db import init_db, seed_users


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Создание базы данных и наполнение ее тестовыми пользователями при запуске приложения."""

    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_users(session)

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(UserLoggerMiddleware)

app.include_router(auth_route)
app.include_router(main_page)
app.include_router(files)
app.include_router(logs_router)
app.include_router(profile)

app.mount("/uploads", StaticFiles(directory="app/uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
