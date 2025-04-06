from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.database import Base, engine
from app.models.users import User
from app.utils.security import get_password_hash


async def init_db() -> None:
    """Создает таблицы приложения в базе данных."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed_users(db: AsyncSession) -> None:
    """Создает тестовых пользователей при запуске приложения."""

    result = await db.execute(select(User))
    users = result.scalars().all()
    if not users:
        test_users = [
            User(
                login="alice", full_name="Alice Doe", password=get_password_hash("pass1"),
                company="Sber", position="Dev"
            ),
            User(
                login="bob", full_name="Bob Smith", password=get_password_hash("pass2"),
                company="Sber", position="QA"
            ),
            User(
                login="carol", full_name="Carol Danvers", password=get_password_hash("pass3"),
                company="Sber", position="Manager"
            ),
            User(
                login="dave", full_name="Dave Grohl", password=get_password_hash("pass4"),
                company="Sber", position="DevOps"
            ),
            User(
                login="eve", full_name="Eve Torres", password=get_password_hash("pass5"),
                company="Sber", position="HR"
            ),
        ]
        db.add_all(test_users)
        await db.commit()
