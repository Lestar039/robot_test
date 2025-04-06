from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import _TemplateResponse

from app.config.database import get_db
from app.models.users import User
from app.services.auth import get_current_user
from app.services.logs import get_logs

logs_router = APIRouter(
    tags=["Logs"],
    responses={404: {"description": "Not found"}}
)
templates = Jinja2Templates(directory="app/templates")

@logs_router.get("/logs", response_class=HTMLResponse)
async def logs(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> _TemplateResponse:
    """Страница просмотра логов."""

    logs = await get_logs(user=current_user, db=db)
    return templates.TemplateResponse(
        "logs/logs.html", {"request": request, "logs": logs, "user": current_user}
    )
