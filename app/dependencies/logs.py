from logger.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func


class Log(Base):
    """таблица для записей логов."""

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)
    url = Column(String)
    status_code = Column(Integer)
    user = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
