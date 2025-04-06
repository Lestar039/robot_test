from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.services.auth import get_current_user

templates = Jinja2Templates(directory="app/templates")

main_page = APIRouter(
    tags=["Main Page"],
    responses={404: {"description": "Not found"}}
)
@main_page.get("/", response_class=HTMLResponse)
async def home(
        request: Request,
        current_user: Annotated[str, Depends(get_current_user)]
) -> _TemplateResponse:
    """Главная страница."""

    return templates.TemplateResponse("main/index.html", {
        "request": request,
        "user": current_user
    })
