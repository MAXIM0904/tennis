from fastapi import APIRouter
from typing import List
from fastapi.responses import JSONResponse
from fastapi import Depends, UploadFile, File
from profile import authentication
from os import makedirs


photo = APIRouter()


@photo.post("/userPhoto")
async def photo_user(file_user: UploadFile = File(...), current_user: dict = Depends(authentication.get_current_user)):
    """ Функция загрузки аватарки пользователя. """
    file_url = f"media/{current_user['message'].id}/userPhoto"
    makedirs(file_url, exist_ok=True)
    with open(f"{file_url}/{file_user.filename}", "wb") as buffer:
        buffer.write(file_user.file.read())
    return JSONResponse({
        "success": True,
        "message": "Фото успешно загружены"
    })


@photo.post("/matchPhoto")
async def photo_user(
        file_match: List[UploadFile] = File(...),
        current_user: dict = Depends(authentication.get_current_user)
):
    """ Функция массовой загрузки фотографий матча. """
    file_url = f"media/{current_user['message'].id}/matchPhoto"
    makedirs(file_url, exist_ok=True)
    for i_file_match in file_match:
        with open(f"{file_url}/{i_file_match.filename}", "wb") as buffer:
            buffer.write(i_file_match.file.read())

    return {
        "success": True,
        "message": "Фото успешно загружены"
    }
