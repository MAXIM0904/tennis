from typing import List
from datetime import date
from pydantic import BaseModel
from typing import Union
from datetime import datetime


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


class ApplicationModel(BaseModel):
    requests: List[ApplicationInf]


class DoublesScoresSchemas(BaseModel):

    match_won: Union[bool, None] = True
    first_set_f: Union[int, None] = 12
    first_set_s: Union[int, None] = 11
    first_set_tie_f: Union[int, None]
    first_set_tie_s: Union[int, None]
    second_set_f: Union[int, None]
    second_set_s: Union[int, None]
    second_set_tie_f: Union[int, None]
    second_set_tie_s: Union[int, None]
    third_set_f: Union[int, None]
    third_set_s: Union[int, None]
    third_set_tie_f: Union[int, None]
    third_set_tie_s: Union[int, None]
    status: Union[int, None]
    played_at: Union[datetime, None]
    fourth_set_f: Union[int, None]
    fourth_set_s: Union[int, None]
    fourth_set_tie_f: Union[int, None]
    fourth_set_tie_s: Union[int, None]
    fifth_set_f: Union[int, None]
    fifth_set_s: Union[int, None]
    fifth_set_tie_f: Union[int, None]
    fifth_set_tie_s: Union[int, None]
    sets: Union[int, None]

    class Config:
        orm_mode = True


class DoublesScoresCreate(DoublesScoresSchemas):
    f_two_id: Union[int, None]
    s_one_id: Union[int, None]
    s_two_id: Union[int, None]

    class Config:
        orm_mode = True


class SchemaDoublesScores(BaseModel):
    requests: DoublesScoresCreate


class DoublesScoresSchemasInf(DoublesScoresCreate):
    id: Union[int, None]
    f_one_id: Union[int, None]

    class Config:
        orm_mode = True


class ScoresSchemasCreate(DoublesScoresSchemas):
    s_id: Union[int, None]

    class Config:
        orm_mode = True


class ScoresSchemasInf(ScoresSchemasCreate):
    id: Union[int, None]
    f_id: Union[int, None]

    class Config:
        orm_mode = True


class SchemaScores(BaseModel):
    requests: ScoresSchemasInf
