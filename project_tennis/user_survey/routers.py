from fastapi import APIRouter
from profile.models import Players
from fastapi import Depends
from profile import authentication
from sqlalchemy.orm import Session
from sql_app.db import get_db
from .models import UserSurvey
from . import schema
from profile import utils


survey = APIRouter()


@survey.get("/questions")
async def users_user(current_user: Players = Depends(authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает вопросы для тестирования """

    questions = db.query(UserSurvey).all()
    if questions:
        schema_questions = schema.SchemaSurvey(questions=questions)
        answer = utils.answer_user_data(True, "", schema_questions.dict())
        return answer

    answer = utils.answer_user(False, "Вопросы не найдены.")
    return answer



@survey.post("/result")
async def users_user(current_user: Players = Depends(authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает рейтинг игрока после прохождения теста. ПОКА ЗАГЛУШКА Т.К. нет СВЯЗИ С БОТОМ """

    answer = utils.answer_user_data(True, "Теперь вы можете найти партнера для игры", {"rating": "1234 BTRP"})
    return answer
