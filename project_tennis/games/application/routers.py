from fastapi import APIRouter
from sqlalchemy.orm import Session
from sql_app.db import get_db
from fastapi import Depends
from .schema import ApplicationCreate, ApplicationInf
from profile import authentication
from .models import GameOrders
from typing import List

application = APIRouter()


@application.get("/all_application/", response_model=List[ApplicationInf])
async def read_own_items(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    user_profile = db.query(GameOrders).all()
    return user_profile

@application.post("/application_create/", response_model=ApplicationInf)
async def application_create(application_create: ApplicationCreate, current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    create_data = application_create.dict(exclude_unset=True)
    create_data['user_id'] = current_user.id
    db_application = GameOrders(**create_data)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application
