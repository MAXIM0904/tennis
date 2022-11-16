from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from profile import authentication
from os import makedirs
from profile import utils
from profile.models import Players
photo = APIRouter()


@photo.post("/userPhoto")
async def photo_user(file_user: UploadFile = File(...), current_user: Players = Depends(authentication.get_current_user)):
    """ Функция загрузки аватарки пользователя. """
    file_url = f"media/{current_user.id}/userPhoto"
    makedirs(file_url, exist_ok=True)
    with open(f"{file_url}/{file_user.filename}", "wb") as buffer:
        buffer.write(file_user.file.read())

    return utils.answer_user(True," Фото успешно загружены")


@photo.post("/matchPhoto")
async def photo_user(
        file_match: UploadFile = File(...),
        current_user: Players = Depends(authentication.get_current_user)
):
    """ Функция массовой загрузки фотографий матча. """
    file_url = f"media/{current_user.id}/matchPhoto"
    makedirs(file_url, exist_ok=True)
    with open(f"{file_url}/{file_match.filename}", "wb") as buffer:
        buffer.write(file_match.file.read())

    return utils.answer_user(True," Фото успешно загружены")
