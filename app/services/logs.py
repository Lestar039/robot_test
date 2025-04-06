from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.dependencies.logs import Log
from app.models.users import User


async def get_logs(user: User, db: AsyncSession) -> Sequence[Row[Any] | RowMapping | Any]:
    """Выгружает логи пользователя из БД."""

    result = await db.execute(
        select(Log).where(Log.user == user.login).order_by(Log.timestamp.desc())
    )
    return result.scalars().all()
