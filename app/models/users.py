from sqlalchemy import Column, Integer, String

from app.config.database import Base


class User(Base):
    """Класс пользователей."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    login = Column(String(length=50), unique=True)
    password = Column(String(length=100))
    full_name = Column(String(length=50))
    company = Column(String(length=50))
    position = Column(String(length=30))
