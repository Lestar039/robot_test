from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.templating import Jinja2Templates, _TemplateResponse

from app.config.database import get_db
from app.utils.jwt_security import create_access_token
from app.utils.security import authenticate_user

auth_route = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="app/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_route.get("/login", response_class=HTMLResponse)
async def login(request: Request) -> _TemplateResponse:
    """Страница авторизации."""

    return templates.TemplateResponse("auth/login.html", {"request": request})


@auth_route.post("/login")
async def login_post(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    login: Annotated[str, Form()] = ...,
    password: Annotated[str, Form()] = ...,

) -> RedirectResponse:
    """Авторизация пользователя."""

    user = await authenticate_user(login, password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Неверные логин или пароль")
    access_token = create_access_token(data={"sub": user.login})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)

    return response
