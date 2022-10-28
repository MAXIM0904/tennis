from pydantic import BaseModel
from typing import Union
from time import time
from datetime import datetime


def random_int_time():
    id = int(time() * 100000)
    return int(id)


class PhoneCreate(BaseModel):
    phone: int

    class Config:
        orm_mode = True


class PasswordCreate(BaseModel):
    password: Union[str, None]
    verification_password: Union[str, None]

    class Config:
        orm_mode = True


class SmsCode(PasswordCreate):
    id: int
    code: int

    class Config:
        orm_mode = True


class ProfileCreate(PasswordCreate, PhoneCreate):
    id: int = random_int_time()
    name: str = 'xx1x'
    initial_rating: int = 0
    is_male: bool = True # Пол по умолчанию не задан и не спрашивается при регистрации. Может None пока?

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True


class ProfileUnf(ProfileUpdate):
    id: int
    registered_at: Union[datetime, None]

    class Config:
        orm_mode = True


class ProfilenModel(BaseModel):
    success: bool = True
    message: str = ""
    data: ProfileUnf


class Token(BaseModel):
    success: bool = True
    message: str = "Пользователь успешно авторизован"
    data: dict
    token_type: str = "bearer"


class ProfileAuth(BaseModel):
    phone: int
    password: str


class TokenData(BaseModel):
    user_id: Union[str, None] = None
