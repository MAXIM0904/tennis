from fastapi import APIRouter
from games import utils_game
from profile.models import Players
from fastapi import Depends
from profile import authentication
from sqlalchemy.orm import Session
from sql_app.db import get_db, create_bd
from .models import UserSurvey
from . import schema
from profile import utils
import requests
import ast

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
async def users_user(result_survey: schema.ResultSurvey,
                     current_user: Players = Depends(
                         authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает рейтинг игрока после прохождения теста. ПОКА ЗАГЛУШКА Т.К. нет СВЯЗИ С БОТОМ """
    survey_user = result_survey.dict()['answers']
    if len(survey_user) == 9:
        experience = survey_user[0]
        forhand = survey_user[1]
        backhand = survey_user[2]
        serve = survey_user[3]
        speed = survey_user[4]
        tournaments = survey_user[5]
        slice = survey_user[6]
        net = survey_user[7]
        prizes = survey_user[8]

        url = f"http://bugz.su:8086/v1/player/initial-power/" \
              f"{experience}/{forhand}/{backhand}/{slice}/{serve}/{net}/{speed}/{tournaments}/{prizes}"
        response = requests.get(url)
        if response.status_code != 200:
            return utils.answer_user(False, 'Нет ответа от сервера расчета рейтинга')
        data = eval(response.content)
        dict_data = ast.literal_eval(data)
        rating = dict_data['power']
        current_user.rating = rating
        current_user.initial_rating = rating
        create_bd(db=db, db_profile=current_user)
        profile_ratings = {'id': None,
                           'user_id': current_user.id,
                           'score_id': 320,
                           'rating': rating,
                           'rd': 350
                           }
        utils_game.save_rating(db, profile_ratings)
        answer = utils.answer_user_data(
            True, "Теперь вы можете найти партнера для игры", {"rating": utils.rounding_rating(rating)})
    else:
        answer = utils.answer_user(
            False, f'Получены ответы на {len(survey_user)} вопросов. Вы не ответили на {9 - len(survey_user)} вопрос'
        )
    return answer
