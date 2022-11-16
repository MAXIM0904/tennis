from pydantic import BaseModel
from typing import Union, List
from time import time
from datetime import datetime


def random_int_time():
    """Временная функция генерации ID для таблицы Players"""
    id = int(time() * 100000)
    return int(id)


class ErrorResponseModel(BaseModel):
    success: bool
    message: str


class PositiveResponseModel(ErrorResponseModel):
    data: dict


class SchemaPhone(BaseModel):
    phone: int


class PasswordCreate(BaseModel):
    password: str


class ProfileCreate(PasswordCreate, SchemaPhone):
    id: int = random_int_time()
    name: str = 'xx1x'
    initial_rating: int = 0
    is_male: bool = True # Пол по умолчанию не задан и не спрашивается при регистрации. Может None пока?
    code: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    id: int
    token: str


class TokenData(BaseModel):
    user_id: Union[str, None] = None


class ProfileAuth(SchemaPhone, PasswordCreate):
    pass


class ProfileUpdate(BaseModel):
    name: Union[str, None]
    phone: Union[int, None]
    initial_rating: Union[float, None]
    is_male: Union[bool, None]
    experience: Union[int, None] # num от 1 до 4, новичок, любитель, продвинутый, Мастерс
    secondary_location: Union[int, None]
    primary_location: Union[int, None]
    is_full_reg: Union[bool, None]
    rating: Union[float, None]
    is_bot_blocked: Union[bool, None]
    username: Union[str, None]
    doubles_rating: Union[float, None]
    mixed_rating: Union[float, None]
    city_id: Union[int, None]
    referral: Union[int, None]
    referral_other: Union[str, None]
    racquet: Union[int, None]
    racquet_detail: Union[str, None]
    global_notification: Union[bool, None]
    tournament_id: Union[int, None]
    corporation: Union[int, None]
    play_tennis_id: Union[str, None]
    city_other: Union[str, None]
    offline_tournament_id: Union[int, None]
    status: Union[int, None]
    photo: Union[str, None]

    # class Config:
    #     orm_mode = True


class ProfileUnf(ProfileUpdate):
    id: int
    registered_at: Union[datetime, None]

    class Config:
        orm_mode = True


class ProfileResponseModel(ErrorResponseModel):
    data: List[ProfileUnf]

    class Config:
        orm_mode = True

# class SchemaСonfirmationСodes(BaseModel):
#     phone: int
#     code: int

# class PasswordCreate(BaseModel):
#     password: Union[str, None]
#     verification_password: Union[str, None]
#
#     class Config:
#         orm_mode = True
#
#
# class SmsCode(PasswordCreate):
#     id: int
#     code: int
#
#     class Config:
#         orm_mode = True
#
#
#
# class ProfileUpdate(BaseModel):
#     name: Union[str, None]
#     phone: Union[int, None]
#     initial_rating: Union[float, None]
#     is_male: Union[bool, None]
#     experience: Union[int, None] # num от 1 до 4, новичок, любитель, продвинутый, Мастерс
#     secondary_location: Union[int, None]
#     primary_location: Union[int, None]
#     is_full_reg: Union[bool, None]
#     rating: Union[float, None]
#     is_bot_blocked: Union[bool, None]
#     username: Union[str, None]
#     doubles_rating: Union[float, None]
#     mixed_rating: Union[float, None]
#     city_id: Union[int, None]
#     referral: Union[int, None]
#     referral_other: Union[str, None]
#     racquet: Union[int, None]
#     racquet_detail: Union[str, None]
#     global_notification: Union[bool, None]
#     tournament_id: Union[int, None]
#     corporation: Union[int, None]
#     play_tennis_id: Union[str, None]
#     city_other: Union[str, None]
#     offline_tournament_id: Union[int, None]
#
#     class Config:
#         orm_mode = True
#
#
# class ProfileUnf(ProfileUpdate):
#     id: int
#     registered_at: Union[datetime, None]
#
#     class Config:
#         orm_mode = True
#
#
# class ErrorResponseModel(BaseModel):
#     success: bool
#     message: str
#
#
# class PositiveResponseModel(BaseModel):
#     data: ProfileUnf
#
#
#
#
# class ProfileAuth(BaseModel):
#     phone: int
#     password: str
#
#
