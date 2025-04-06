import os

import httpx
from dotenv import load_dotenv
from fastapi import Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.utils.jwt_security import decode_access_token

load_dotenv()

LOGGER_PORT = os.getenv("LOGGER_PORT")


class UserLoggerMiddleware(BaseHTTPMiddleware):
    """Логирует запросы пользователей."""

    async def dispatch(self, request: Request, call_next) -> Response:
        """Отправляет логи в сервис логов."""

        user_login = "anonymous"
        token = request.cookies.get("access_token")
        if token:
            user_login = decode_access_token(token)

        response = await call_next(request)

        log_data = {
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "user": user_login
        }

        try:
            async with httpx.AsyncClient() as client:
                await client.post(f"http://logger:{LOGGER_PORT}/logs", json=log_data)
        except Exception:
            pass

        return response
