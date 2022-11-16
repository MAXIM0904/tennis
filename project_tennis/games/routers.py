from fastapi import APIRouter
from sqlalchemy.orm import Session
from sql_app.db import get_db
from fastapi import Depends
from games import schema
from profile import authentication
from games.models import GameOrders, DoublesScores, Scores
from fastapi.responses import JSONResponse
from profile import utils
from profile.models import Players
from sql_app.db import create_bd


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
        doubles_scores_create: schema.DoublesScoresCreate,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция создает запись игры с 4-мя играками """
    create_doubles_scores = doubles_scores_create.dict(exclude_unset=True)
    create_doubles_scores['f_one_id'] = current_user.id
    db_create_doubles = DoublesScores(**create_doubles_scores)
    create_bd(db=db, db_profile=db_create_doubles)
    schema_profile = schema.SchemaDoublesScores(requests=db_create_doubles)
    return utils.answer_user_data(True, "Отлично, счет внесен. Ваша сила изменилась:", schema_profile.dict())


@game.post("/matches/create")
async def scores_create(
        scores_create: schema.ScoresSchemasCreate,
        current_user: Players = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция создает запись игры с 2-мя играками """
    create_scores = scores_create.dict(exclude_unset=True)
    create_scores['f_id'] = current_user.id
    db_create_scores = Scores(**create_scores)
    create_bd(db=db, db_profile=db_create_scores)
    schema_profile = schema.SchemaScores(requests=db_create_scores)
    return utils.answer_user_data(True, "Отлично, счет внесен. Ваша сила изменилась:", schema_profile.dict())
