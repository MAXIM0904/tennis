from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends
from sql_app.db import get_db
from .models import Racquet, Strings
from profile import utils
from profile import authentication


inventory = APIRouter()


@inventory.get("/racquet")
async def get_racquet(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    """ Получить список всех ракеток """
    list_racquet = db.query(Racquet).all()
    return utils.answer_user_data(True, "", list_racquet)


@inventory.get("/strings")
async def get_racquet(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    """ Получить список всех сеток ракетки """
    list_racquet = db.query(Strings).all()
    return utils.answer_user_data(True, "", list_racquet)
