from typing import Any

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Row, RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import get_db
from app.models.users import User
from app.utils.jwt_security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(
        request: Request,
        db: AsyncSession = Depends(get_db)
) -> None | Row[Any] | RowMapping:
    """Получить текущего пользователя."""

    token = request.cookies.get("access_token")
    if not token:
        return None

    user_login = decode_access_token(token)
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.login == user_login))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
