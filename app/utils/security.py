from typing import Any

from passlib.context import CryptContext
from sqlalchemy import Row, RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.users import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """Хэширование пароля."""

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля."""

    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(
        login: str,
        password: str,
        db: AsyncSession
) -> None | Row[Any] | RowMapping:
    """Аутентификация пользователя."""

    result = await db.execute(select(User).filter(User.login == login))
    user = result.scalars().first()

    if user is None:
        return None

    if not verify_password(password, user.password):
        return None

    return user
