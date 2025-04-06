from typing import Annotated

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.config.database import get_db
from app.models.users import User
from app.services.auth import get_current_user

templates = Jinja2Templates(directory="app/templates")

profile = APIRouter(prefix="/profile", tags=["Profile"])

@profile.get("/", response_class=HTMLResponse)
async def profile_page(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)]
) -> _TemplateResponse:
    """Страница профиля пользователя."""

    return templates.TemplateResponse(
        "profile/profile.html", {"request": request, "user": current_user}
    )


@profile.get("/edit", response_class=HTMLResponse)
async def edit_profile_page(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
)  -> _TemplateResponse:
    """Страница обновления профиля."""

    return templates.TemplateResponse(
        "profile/edit_profile.html", {"request": request, "user": current_user}
    )


@profile.post("/edit")
async def update_profile(
    request: Request,
    full_name: Annotated[str, Form()] = ...,
    company: Annotated[str, Form()] = ...,
    position: Annotated[str, Form()] = ...,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    """Обновление профиля."""

    current_user.full_name = full_name
    current_user.company = company
    current_user.position = position
    await db.commit()
    return RedirectResponse(url="/profile", status_code=303)
