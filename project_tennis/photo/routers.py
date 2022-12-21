import os

from fastapi import APIRouter
from fastapi import Depends, UploadFile, File, Form
from profile import authentication
from profile import utils
from profile.models import Players
from .utils import save_img
from games import models
from sqlalchemy.orm import Session
from sql_app.db import get_db


photo = APIRouter()


@photo.post("/userPhoto")
async def photo_user(file_user: UploadFile = File(...),
                     current_user: Players = Depends(authentication.get_current_user)):
    """ Функция загрузки аватарки пользователя. """
    file_url = f"media/{current_user.id}/userPhoto"
    new_name = f"{current_user.id}.jpg"
    answer_save = save_img(file_url=file_url, file_user=file_user, new_name=new_name)
    url = utils.url_avatar(f"{file_url}/{new_name}")
    return utils.answer_user_data(answer_save[0], answer_save[1], {"url": url})


@photo.post("/matchPhoto")
async def photo_match(
        matchId: int = Form(),
        file_match: UploadFile = File(...),
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция загрузки фотографий матча. """
    match = db.query(models.Scores).get(matchId)
    if match:
        file_url = f"media/{match.id}/matchPhoto"
        new_name = f"{match.id}.jpg"
        answer_save = save_img(file_url=file_url, file_user=file_match, new_name=new_name)
        url = utils.url_avatar(f"{file_url}/{new_name}")
        return utils.answer_user_data(answer_save[0], answer_save[1], {"url": url})
    return utils.answer_user(True, "Матчей не найдено")


@photo.get("/defaultAvatars")
async def default_avatars(current_user: Players = Depends(authentication.get_current_user)):
    """ Получение дефолтных аватарок """
    url_default = f"media/defaultAvatars"
    default_avatar = [
        f"{utils.url_host}/image/{url_default}/{file}" for file in os.listdir(url_default)
    ]
    url_avatar = {"avatars": default_avatar}
    return utils.answer_user_data(True, "", url_avatar)
