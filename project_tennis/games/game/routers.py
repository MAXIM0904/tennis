from fastapi import APIRouter
from sqlalchemy.orm import Session
from sql_app.db import get_db
from fastapi import Depends
from . import schema
from profile import authentication
from .models import GameOrders, DoublesScores, Scores
from fastapi.responses import JSONResponse


game = APIRouter()


@game.get("/request/")
async def read_own_items(userId: int,
                         current_user: dict = Depends(authentication.get_current_user),
                         db: Session = Depends(get_db)):
    """ Функция отбирает все заявки """
    user_profile = db.query(GameOrders).all()
    schema_profile = schema.ApplicationModel(requests=user_profile)
    return ({"success": True,
            "data": schema_profile})


@game.post("/request/add")
async def application_create(application_create: schema.ApplicationCreate,
                             current_user: dict = Depends(authentication.get_current_user),
                             db: Session = Depends(get_db)):
    """ Функция создания заявок """
    create_data = application_create.dict(exclude_unset=True)
    create_data['user_id'] = current_user["message"].id
    db_application = GameOrders(**create_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return JSONResponse({
        "success": True,
        "message": "Ваша заявка успешно принята"
    })

@game.post("/matches/doubles_create", response_model=schema.DoublesScoresSchemasInf)
async def doubles_scores_create(
        doubles_scores_create: schema.DoublesScoresCreate,
        current_user: dict = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция создает запись игры с 4-мя играками """
    create_doubles_scores = doubles_scores_create.dict(exclude_unset=True)
    create_doubles_scores['f_one_id'] = current_user["message"].id
    db_create_doubles = DoublesScores(**create_doubles_scores)
    db.add(db_create_doubles)
    db.commit()
    db.refresh(db_create_doubles)
    return db_create_doubles


@game.post("/matches/create", response_model=schema.ScoresSchemasInf)
async def scores_create(
        scores_create: schema.ScoresSchemasCreate,
        current_user: dict = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)):
    """ Функция создает запись игры с 2-мя играками """
    create_scores = scores_create.dict(exclude_unset=True)
    create_scores['f_id'] = current_user["message"].id
    db_create_scores = Scores(**create_scores)
    db.add(db_create_scores)
    db.commit()
    db.refresh(db_create_scores)
    return db_create_scores
