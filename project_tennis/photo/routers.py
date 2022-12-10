from fastapi import APIRouter
from fastapi import Depends, UploadFile, File
from profile import authentication
from profile import utils
from profile.models import Players
from .utils import save_img


photo = APIRouter()


@photo.post("/userPhoto")
async def photo_user(file_user: UploadFile = File(...),
                     current_user: Players = Depends(authentication.get_current_user)):
    """ Функция загрузки аватарки пользователя. """
    file_url = f"media/{current_user.id}/userPhoto"
    new_name = f"{current_user.id}.jpg"
    answer_save = save_img(file_url=file_url, file_user=file_user, new_name=new_name)
    return utils.answer_user(answer_save[0], answer_save[1])


@photo.post("/matchPhoto")
async def photo_match(
        file_match: UploadFile = File(...),
        current_user: Players = Depends(authentication.get_current_user)):
    """ Функция загрузки фотографий матча. """
    file_url = f"media/{current_user.id}/matchPhoto"
    new_name = f"{current_user.id}.jpg"
    answer_save = save_img(file_url=file_url, file_user=file_match, new_name=new_name)
    return utils.answer_user(answer_save[0], answer_save[1])


@photo.get("/defaultAvatars")
async def default_avatars(current_user: Players = Depends(authentication.get_current_user)):
    """ Получение дефолтных аватарок """
    url_avatar = {"avatars": [
        "https://tennis.app/defAv1.jpg",
        "https://tennis.app/defAv2.jpg",
        "https://tennis.app/defAv3.jpg"
    ]}

    return utils.answer_user_data(True, "", url_avatar)
