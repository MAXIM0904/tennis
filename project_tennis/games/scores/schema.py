from pydantic import BaseModel
from typing import Union
from datetime import datetime



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

class DoublesScoresSchemasInf(DoublesScoresCreate):
    id: Union[int, None]
    f_one_id: Union[int, None]

    class Config:
        orm_mode = True




class ScoresSchemasCreate(DoublesScoresSchemas):
    s_id: Union[int, None] = 586080284

    class Config:
        orm_mode = True


class ScoresSchemasInf(ScoresSchemasCreate):
    id: Union[int, None]
    f_id: Union[int, None]

    class Config:
        orm_mode = True