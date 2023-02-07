from fastapi import APIRouter
from sqlalchemy.orm import Session
from sql_app.db import get_db
from fastapi import Depends
from games import schema
from games.models import GameOrders, DoublesScores, Scores, Ratings
from profile import utils, authentication
from profile.models import Players
from sql_app.db import create_bd
from . import utils_game
from sqlalchemy import or_, desc
import requests
import math
import ast

game = APIRouter()


@game.get("/request")
async def read_own_items(current_user: Players = Depends(authentication.get_current_user),
                         db: Session = Depends(get_db)):
    """ Функция отбирает все заявки """
    user_profile = db.query(GameOrders).all()
    schema_profile = schema.ApplicationModel(requests=user_profile)
    return utils.answer_user_data(True, "", schema_profile.dict())


@game.post("/request/add")
async def application_create(application_create: schema.ApplicationCreate,
                             current_user: Players = Depends(
                                 authentication.get_current_user),
                             db: Session = Depends(get_db)):
    """ Функция создания заявок """
    create_data = application_create.dict(exclude_unset=True)
    create_data['user_id'] = current_user.id
    db_application = GameOrders(**create_data)
    create_bd(db=db, db_profile=db_application)
    return utils.answer_user(True, "Заявка успешно принята")


@game.post("/matches/doubles_create")
async def doubles_scores_create(
        doubles_scores_create: schema.SchemaScores,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):

    """ Функция создает запись игры с 4-мя игроками """

    create_doubles_scores = doubles_scores_create.dict(exclude_unset=True)
    create_doubles_scores['f_one_id'] = current_user.id
    db_create_doubles = DoublesScores(**create_doubles_scores)
    create_bd(db=db, db_profile=db_create_doubles)
    # schema_profile = schema.SchemaDoublesScores(requests=db_create_doubles)
    # return utils.answer_user_data(True, "Отлично, счет внесен. Ваша сила изменилась:", schema_profile.dict())


@game.post("/matches/create")
async def scores_create(
        scores_create: schema.SchemaScores,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция создает запись игры с 2-мя игроками """
    dict_scores = utils_game.dictionary_save(scores_create, current_user.id)
    db_create_scores = Scores(**dict_scores)
    create_bd(db=db, db_profile=db_create_scores)
    rating_1_user = db.query(Ratings).filter(Ratings.user_id == db_create_scores.f_id).order_by(
        desc(Ratings.score_id)).limit('1').all()
    rating_2_user = db.query(Ratings).filter(Ratings.user_id == db_create_scores.s_id).order_by(
        desc(Ratings.score_id)).limit('1').all()
    if rating_1_user:
        rating_1, stability_1 = rating_1_user[0].rating, rating_1_user[0].rd
    else:
        rating_1, stability_1 = 0, 0
    if rating_2_user:
        rating_2, stability_2 = rating_1_user[0].rating, rating_1_user[0].rd
    else:
        rating_2, stability_2 = 0, 0

    if len(scores_create.result) > 3:
        game = 1
    else:
        game = 0

    url = f"http://bugz.su:8086/v1/power/{db_create_scores.id}/{rating_1}/{stability_1}/{rating_2}/{stability_2}/{game}"
    response = requests.get(url)

    if response.status_code == 200:
        data = eval(response.content)
        dict_data = ast.literal_eval(data)

        profile_ratings = {'id': None,
                           'user_id': db_create_scores.f_id,
                           'score_id': dict_data['score'],
                           'rating': dict_data['new_rating_first_player'],
                           'rd': dict_data['new_stability_first_player']
                           }
        utils_game.save_rating(db, profile_ratings)

        profile_ratings = {'id': None,
                           'user_id': db_create_scores.s_id,
                           'score_id': dict_data['score'],
                           'rating': dict_data['new_rating_second_player'],
                           'rd': dict_data['new_stability_second_player']
                           }
        utils_game.save_rating(db, profile_ratings)

        current_user.rating = dict_data['new_rating_first_player']
        create_bd(db=db, db_profile=current_user)
        profile_user = authentication.get_user_id(
            db, str(db_create_scores.s_id))
        profile_user.rating = dict_data['new_rating_second_player']
        create_bd(db=db, db_profile=current_user)
        return utils.answer_user_data(True, "Отлично, счет внесен. Ваша сила изменилась.",  {
            "matchId": db_create_scores.id,
            "powerOld": math.ceil(rating_1),
            "powerNew": math.ceil(current_user.rating)
        })
    else:
        return utils.answer_user(False, "Ошибка подключения к базе данных.")


@game.get("/matches/history")
async def scores_history(
        id: int,
        page: int = 1,
        fromDate: int = None,
        isWon: bool = None,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает информацию обо всех матчах пользователя (история игр) """
    all_match = []

    queries = [or_(Scores.f_id == id, Scores.s_id == id)]
    limit_page = 40
    if page <= 0:
        page = 1
    offset_page = (page - 1) * limit_page

    if fromDate:
        date_match = utils.time_save(fromDate)
        queries.append(Scores.played_at >= date_match)

    if isWon:
        queries.append(Scores.match_won == isWon)

    db_all_math = db.query(Scores).filter(*queries).\
        order_by(desc(Scores.played_at)).offset(
            offset_page).limit(limit_page).all()

    for i_match in db_all_math:
        inf_match = utils_game.preparing_response(db, i_match)
        all_match.append(inf_match)

    if all_match:
        return utils.answer_user_data(True, "Ok",  all_match)
    else:
        return utils.answer_user(True, "История игр отсутствует")


@game.post("/matches/evaluationGame")
async def evaluation_game(
        evaluation: schema.SchemaEvaluation,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция оценки игры """

    return utils.answer_user_data(True, "Ok",  evaluation)


@game.get("/matches/gameSchedule")
async def game_schedule(matchId: int,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает url графика """

    db_math = db.query(Scores).get(matchId)
    profile_user_1 = authentication.get_user_id(db, str(db_math.s_id))
    profile_user_2 = authentication.get_user_id(db, str(db_math.f_id))
    registration_ident = 1 if profile_user_1.registered_at < profile_user_2.registered_at else 0

    url = f'http://bugz.su:8086/match/power-graph/' \
          f'{profile_user_1.id}/' \
          f'{profile_user_1.registered_at.strftime("%Y")}/' \
          f'{profile_user_1.registered_at.strftime("%m")}/' \
          f'{profile_user_1.initial_rating}/' \
          f'{profile_user_1.name}/' \
          f'{profile_user_2.id}/' \
          f'{profile_user_2.registered_at.strftime("%Y")}/' \
          f'{profile_user_2.registered_at.strftime("%m")}/' \
          f'{profile_user_2.initial_rating}/' \
          f'{profile_user_2.name}/{registration_ident}'
    url = "http://bugz.su:8086/match/power-graph/429491457/2022/3/1030.0/Евгений Решетник/76897637/2022/10/1120.0/Ivan Kolesnikov/1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.content
        str_data = str(data, 'UTF-8').strip('"')
        answer = utils.answer_user_data(True, "Ok", {"url": str_data})
    else:
        answer = utils.answer_user(False, "Невозможно получить график")
    return answer
