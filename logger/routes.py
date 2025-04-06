from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from logger.database import get_db
from logger.models import Log
from logger.schemas import LogCreateSchema

logs = APIRouter()


@logs.post("/logs")
async def create_log(log: LogCreateSchema, db: Annotated[AsyncSession, Depends(get_db)]) -> dict:
    """Принимает, валидирует и записывает логи в базу данных."""

    new_log = Log(**log.model_dump(exclude_none=True))
    db.add(new_log)
    await db.commit()
    return {"message": "Log saved"}
