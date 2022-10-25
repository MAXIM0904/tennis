from fastapi import APIRouter
from profile import authentication
from . import schema
from fastapi import Depends
from sqlalchemy.orm import Session
from sql_app.db import get_db
from .models import DoublesScores, Scores


scores = APIRouter()


@scores.post("/doubles_scores_create/", response_model=schema.DoublesScoresSchemasInf)
async def doubles_scores_create(
        doubles_scores_create: schema.DoublesScoresCreate,
        current_user: dict = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    create_doubles_scores = doubles_scores_create.dict(exclude_unset=True)
    create_doubles_scores['f_one_id'] = current_user.id

    print(create_doubles_scores)
    db_create_doubles = DoublesScores(**create_doubles_scores)
    db.add(db_create_doubles)
    db.commit()
    db.refresh(db_create_doubles)
    return db_create_doubles


@scores.post("/scores_create/", response_model=schema.ScoresSchemasInf)
async def scores_create(
        scores_create: schema.ScoresSchemasCreate,
        current_user: dict = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    create_scores = scores_create.dict(exclude_unset=True)
    create_scores['f_id'] = current_user.id
    db_create_scores = Scores(**create_scores)
    db.add(db_create_scores)
    db.commit()
    db.refresh(db_create_scores)
    return db_create_scores
