from typing import Annotated

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse

from app.models.users import User
from app.services.auth import get_current_user
from app.services.files import get_file, get_files, get_mime_type, save_file

files = APIRouter(
    prefix="/files",
    tags=["Files"],
    responses={404: {"description": "Not found"}}
)
templates = Jinja2Templates(directory="app/templates")


@files.get("/upload", response_class=HTMLResponse)
async def upload_file_page(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)]
) -> _TemplateResponse:
    """Страница загрузки файлов."""

    return templates.TemplateResponse(
        "files/upload.html",
        {"request": request, "user": current_user}
    )


@files.post("/upload", response_class=HTMLResponse)
async def upload_files(
    request: Request,
    current_user: Annotated[User, Depends(get_current_user)],
    files: Annotated[list[UploadFile], File()] = ...
) -> _TemplateResponse:
    """Загрузка файлов."""

    saved_files = []
    for file in files:
        location = await save_file(file)
        saved_files.append((file.filename, location))

    return templates.TemplateResponse(
        "files/upload.html",
        {
            "request": request,
            "saved_files": saved_files,
            "user": current_user
        }
    )


@files.get("/files", response_class=HTMLResponse)
async def files_list_page(
        request: Request,
        current_user: Annotated[User, Depends(get_current_user)],
        file_type: str = ""
) -> _TemplateResponse:
    """Список загруженных файлов."""

    files = get_files(file_type)
    return templates.TemplateResponse(
        "files/files_list.html",
        {"request": request, "files": files, "user": current_user, "file_type": file_type}
    )


@files.get("/{filename}", response_class=HTMLResponse)
async def file_list_page(
        request: Request,
        filename: str,
        current_user: Annotated[User, Depends(get_current_user)]
) -> _TemplateResponse:
    """Страница для отображения одного файла."""

    file_path = get_file(filename)
    file_url = f"/uploads/{filename}"
    mime_type = get_mime_type(file_path)

    return templates.TemplateResponse(
        "files/file_page.html",
        {
            "request": request,
            "file_location": file_url,
            "filename": filename,
            "user": current_user,
            "mime_type": mime_type
        }
    )


@files.get("/{filename}")
async def download_file_page(
        request: Request,
        filename: str,
        current_user: Annotated[User, Depends(get_current_user)]
) -> _TemplateResponse:
    """Страница загруженного файла."""

    file_path = get_file(filename)
    file_url = f"/uploads/{filename}"
    mime_type = get_mime_type(file_path)

    return templates.TemplateResponse(
        "files/download.html",
        {
            "request": request,
            "file_location": file_url,
            "filename": filename,
            "user": current_user,
            "mime_type": mime_type
        }
    )
