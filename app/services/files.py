import mimetypes
import os
from pathlib import Path

from fastapi import HTTPException, UploadFile

UPLOAD_FOLDER = "app/uploads"

if not Path(UPLOAD_FOLDER).exists():
    Path(UPLOAD_FOLDER).mkdir(parents=True)


async def save_file(file: UploadFile) -> str:
    """Сохранение файла."""

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    try:
        with open(file_location, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)
        return file_location
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error saving file: {error}")



def get_files(file_type_filter: str = "") -> list:
    """Получение списка файлов."""

    files_data = []
    for filename in os.listdir(UPLOAD_FOLDER):
        path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(path):
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type is None:
                mime_type = "application/octet-stream"

            if file_type_filter and not mime_type.startswith(file_type_filter + "/"):
                continue

            files_data.append({
                "filename": filename,
                "mime_type": mime_type,
                "path": f"/uploads/{filename}"
            })
    return files_data


def get_file(filename: str) -> str:
    """Загрузка файла."""

    file_location = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_location):
        raise HTTPException(status_code=404, detail="File not found")
    return file_location


def get_mime_type(filename: str) -> str:
    """Получить MIME-тип файла."""

    mime_type, _ = mimetypes.guess_type(filename)
    if mime_type is None:
        raise HTTPException(status_code=415, detail="Unsupported file type")
    return mime_type
