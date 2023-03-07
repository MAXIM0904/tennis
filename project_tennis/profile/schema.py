from pydantic import BaseModel
from typing import Union, List
from datetime import datetime


class ErrorResponseModel(BaseModel):
    success: bool
    message: str


class PositiveResponseModel(ErrorResponseModel):
    data: dict|list


class SchemaPhone(BaseModel):
    phone: int


class PasswordCreate(BaseModel):
    password: str


class ProfileCreate(PasswordCreate, SchemaPhone):
    id: int = 1
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




class ShemaAnotherPlayer(BaseModel):
    id: int
    lastName: Union[str, None]
    firstName: Union[str, None]
    power: int| float
    isMale: bool
    countOfMatches: int
    telegram: Union[str, None]
    urlAvatar: Union[str, None]
    country: Union[dict, None]
    city: Union[dict, None]
    district: Union[dict, None]
    isFavorite: bool


class ProfileUpdate(BaseModel):
    firstName: Union[str, None]
    lastName: Union[str, None]
    phone: Union[int, None]
    telegram: Union[str, None] #вместо telegram(завявано на бота)
    cityId: Union[int, None]
    districtId: Union[int, None]
    birthDate: Union[int, None] # в базе Date
    isMale: Union[bool, None]
    gameStyle: Union[str, None]
    isRightHand: Union[bool, None]
    isOneBackhand: Union[bool, None]
    ground: Union[str, None]
    shoesName: Union[str, None]
    racquetId: Union[list[int], None]
    stringsId: Union[list[int], None]
    urlAvatar: Union[str, None]


class ProfileUnf(ProfileUpdate):
    id: int
    countryId: str

    class Config:
        orm_mode = True


class ProfileResponseModel(ErrorResponseModel):
    data: List[ProfileUnf]

    class Config:
        orm_mode = True


class SchemaFavorite(BaseModel):
    favoriteId: int

    class Config:
        orm_mode = True
