from pydantic import BaseModel
from typing import Union
from datetime import date


class ApplicationCreate(BaseModel):

    loc_szao: Union[bool, None]
    loc_sao: Union[bool, None]
    loc_svao: Union[bool, None]
    loc_zao: Union[bool, None]
    loc_cao: Union[bool, None]
    loc_vao: Union[bool, None]
    loc_uzao: Union[bool, None]
    loc_uao: Union[bool, None]
    loc_uvao: Union[bool, None]
    game_type: Union[int, None]
    game_date: Union[date, None]
    game_time: Union[int, None]
    duration: Union[int, None]
    tennis_site: Union[str, None]
    pay: Union[int, None]
    game_time_hh: Union[bool, None]

    class Config:
        orm_mode = True


class ApplicationInf(ApplicationCreate):
    id: int
    user_id: Union[int, None]

    class Config:
        orm_mode = True
