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
from sqlalchemy import or_, desc

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
        order_by(desc(Scores.played_at)).offset(offset_page).limit(limit_page).all()

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
async def game_schedule(
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает url графика """

    return utils.answer_user_data(True, "Ok", {'url': "http://bugz.su:8000/image/media/Schedule/Schedule.PNG"})