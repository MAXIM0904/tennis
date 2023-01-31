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
    dict_experience = {"новичок": 1,
                       "любитель": 2,
                       "продвинутый": 3,
                       "мастерс": 4}

    dict_forhand = {"нестабильный": 1,
                    "стабильный": 2,
                    "сильный": 3,
                    "очень сильный": 4}

    dict_speed = {"медленная": 1,
                  "средняя": 2,
                  "быстрая": 3,
                  "очень быстрая": 4}

    dict_tournaments = {'да': 1,
                        'нет': 2}

    for i_survey in result_survey.requests:
        value = [value for key, value in i_survey.items()
                 if 'answer' in key.lower()]
        value = value[0].lower()
        if i_survey['id'] == 1:
            experience = dict_experience[value]
        elif i_survey['id'] == 2:
            forhand = dict_forhand[value]
        elif i_survey['id'] == 3:
            backhand = dict_forhand[value]
        elif i_survey['id'] == 4:
            serve = dict_forhand[value]
        elif i_survey['id'] == 5:
            speed = dict_speed[value]
        elif i_survey['id'] == 6:
            tournaments = dict_tournaments[value]
        elif i_survey['id'] == 7:
            slice = dict_forhand[value]
        elif i_survey['id'] == 8:
            net = dict_forhand[value]
        elif i_survey['id'] == 9:
            prizes = dict_tournaments[value]

    url = f"http://bugz.su:8086/v1/player/initial-power/" \
          f"{experience}/{forhand}/{backhand}/{slice}/{serve}/{net}/{speed}/{tournaments}/{prizes}"
    response = requests.get(url)
    if response.status_code == 200:
        data = eval(response.content)
        dict_data = ast.literal_eval(data)
        rating = dict_data['power']
    current_user.rating = rating
    create_bd(db=db, db_profile=current_user)
    profile_ratings = {'id': None,
                       'user_id': current_user.id,
                       'score_id': 320,
                       'rating': rating,
                       'rd': 350
                       }
    utils_game.save_rating(db, profile_ratings)

    answer = utils.answer_user_data(
        True, "Теперь вы можете найти партнера для игры", {"rating": rating})
    return answer
