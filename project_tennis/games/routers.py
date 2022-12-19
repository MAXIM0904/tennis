from fastapi import APIRouter
from sqlalchemy.orm import Session
from sql_app.db import get_db
from fastapi import Depends
from games import schema
from profile import authentication
from games.models import GameOrders, DoublesScores, Scores
from profile import utils
from profile.models import Players
from sql_app.db import create_bd
from . import utils_game
from sqlalchemy import or_

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
                             current_user: Players = Depends(authentication.get_current_user),
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
    return utils.answer_user_data(True, "Отлично, счет внесен. Ваша сила изменилась.",  {
        "matchId": db_create_scores.id,
        "powerOld": 456,
        "powerNew": 5555
    })


@game.get("/matches/history")
async def scores_history(
        id: int,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает информацию обо всех матчах пользователя """
    all_math = []
    db_all_math = db.query(Scores).filter(or_(Scores.f_id == id, Scores.s_id == id)).all()

    for i_math in db_all_math:
        inf_math = utils_game.preparing_response(db, i_math)
        all_math.append(inf_math)

    if all_math:
        return utils.answer_user_data(True, "Ok",  all_math)
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
async def game_schedule(
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает url графика """

    return utils.answer_user_data(True, "Ok", {'url': "http://bugz.su:8000/image/media/Schedule/Schedule.PNG"})