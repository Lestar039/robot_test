from pydantic import BaseModel, Field


class LogCreateSchema(BaseModel):
    """Валидация данных логов."""

    method: str = Field(..., max_length=10)
    url: str
    status_code: int
    user: str
