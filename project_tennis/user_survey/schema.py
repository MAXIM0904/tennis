from typing import List
from pydantic import BaseModel


class UserSurveyInf(BaseModel):
    id: int
    question: str
    answer_0: str
    answer_1: str
    answer_2: str = None
    answer_3: str = None

    class Config:
        orm_mode = True


class SchemaSurvey(BaseModel):
    questions: List[UserSurveyInf]


class ResultSurvey(BaseModel):
    answers: list
