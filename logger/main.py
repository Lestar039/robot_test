from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from logger.database import Base, engine
from logger.routes import logs


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Создает таблицу logs в базе данныых."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(logs)
