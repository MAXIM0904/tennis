from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from .schema import ProfileCreate, Token, ProfileAuth, ProfileUnf, ProfileUpdate, PhoneCreate, SmsCode, ProfilenModel
from fastapi import Depends
from sql_app.db import get_db
from .models import Players
from fastapi.responses import JSONResponse
from . import authentication
from . import utils


router = APIRouter()


@router.post("/create")
async def read_users(profile: ProfileCreate, db: Session = Depends(get_db)):
    """ Pегистрация пользователя """
    if profile.password == profile.verification_password:
        profile = profile.dict()
        del profile['verification_password']
        hash_password = authentication.get_password_hash(password=profile['password'])
        profile['password'] = hash_password
        db_profile = Players(**profile)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return JSONResponse({
            "success": True,
            "message": "Регистрация пройдена. Подтвердите номер телефона через СМС",
            "data": {
                "userId": db_profile.id,
                "sms_code": "123"
            }
        })
    else:
        return JSONResponse({
            "success": False,
            "message": "Пароли не совпадают"
        })


@router.post("/confirmCode", response_model=Token)
async def confirmcode(sms_message: SmsCode, db: Session = Depends(get_db)):
    """ Подтверждение кода по смс"""
    if sms_message.code != 123:
        return JSONResponse({
            "success": False,
            "message": "Код из смс введен неверно"
        })
    user = authentication.get_user_id(db=db, user_id=str(sms_message.id))
    if not user["success"]:
        return JSONResponse(user)
    #первичная регистрация
    if sms_message.password is None and sms_message.verification_password is None:
        access_token = authentication.create_access_token(data={"sub": str(user["message"].id)})
        return Token(data={
            "userId": user["message"].id,
            "token": access_token
        })

    #восстановление пароля
    if sms_message.password == sms_message.verification_password:
        password_hash = authentication.get_password_hash(password=sms_message.password)
        user.password = password_hash
        db.add(user)
        db.commit()
        db.refresh(user)
        return JSONResponse({
            "success": True,
            "message": "Пароль изменен"
        })
    else:
        return JSONResponse({
            "success": False,
            "message": "Пароли не совпадают"
        })


@router.post("/auth", response_model=Token)
async def login_for_access_token(form_data: ProfileAuth, db: Session = Depends(get_db)):
    """ Авторизация существующего пользователя """
    user = authentication.authenticate_user(db=db, phone=form_data.phone, password=form_data.password)
    if not user["success"]:
        return JSONResponse(user)
    access_token = authentication.create_access_token(
        data={"sub": str(user["message"].id)})
    return Token(data={
            "userId": user["message"].id,
            "token": access_token
        })


@router.get("/{userId}/get/info")
async def read_users_me(userId: int, current_user: Players = Depends(authentication.get_current_user)):
    """ Получить информацию о пользователе для ЛК """
    schema_profile = ProfilenModel(data=current_user['message'])
    return (schema_profile)


@router.post("/{userId}/edit/personalInfo", response_model=ProfileUnf)
async def users_update(user_update: ProfileUpdate,
                       current_user: Players = Depends(authentication.get_current_user),
                       db: Session = Depends(get_db)):
    """ Изменение данных пользователя"""
    update_data = user_update.dict(exclude_unset=True)
    update_user = utils.user_update(update_data=update_data, current_user=current_user["message"])
    db.add(update_user)
    db.commit()
    db.refresh(update_user)
    return JSONResponse({
        "success": True,
        "message": "Данные успешно сохранены"
    })


@router.post("/password_recovery")
async def password_recovery(phone_user: PhoneCreate, db: Session = Depends(get_db)):
    """ Функция восстановления пароля """
    user = authentication.get_user(db=db, phone=phone_user.phone)
    if not user["success"]:
        return JSONResponse(user)
    return JSONResponse({
            "success": True,
            "message": "Пользователь найден. Подтвердите номер телефона через СМС",
            "data": {
                "userId": user["message"].id,
                "sms_code": "123"
            }
        })


@router.get("/all_users", response_model=List[ProfileUnf])
async def all_users(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    """ Функция возвращает всех пользователей """
    user_profile = db.query(Players).all()
    return user_profile


@router.get("/user/{user_id}", response_model=ProfileUnf)
async def users_user(user_id: int,
                     current_user: dict = Depends(authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает пользователя по id """
    user_profile = authentication.get_user_id(db=db, user_id=str(user_id))
    if not user_profile:
        return JSONResponse({'error': 'Пользователь не найден'})
    return user_profile["message"]
