from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import Session
from .schema import ProfileCreate, Token, ProfileAuth, ProfileUnf, ProfileUpdate, PhoneCreate, SmsCode
from fastapi import Depends, HTTPException, status
from sql_app.db import get_db
from .models import Players
from fastapi.responses import JSONResponse
from . import authentication
from . import utils


router = APIRouter()


@router.get("/")
async def read_users(db: Session = Depends(get_db)):
    return [{"username": "Rick"}, {"username": "Morty"}]


#регистрация пользователя
@router.post("/create", response_model=Token)
async def read_users(profile: ProfileCreate, db: Session = Depends(get_db)):
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
            'sms_code': '123',
            'id': db_profile.id
        })
    else:
        return JSONResponse({'error': 'Пароли не совпадают'})


#вход по логину и паролю
@router.post("/token/", response_model=Token)
async def login_for_access_token(form_data: ProfileAuth, db: Session = Depends(get_db)):
    user = authentication.authenticate_user(db=db, phone=form_data.phone, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = authentication.create_access_token(
        data={"sub": str(user.id)})
    return Token(access_token=access_token)


#информация о пользователе
@router.get("/users/me/", response_model=ProfileUnf)
async def read_users_me(current_user: dict = Depends(authentication.get_current_user)):
    return current_user


#изменение данных пользователя
@router.post("/update/", response_model=ProfileUnf)
async def users_update(user_update: ProfileUpdate, current_user: Players = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    update_data = user_update.dict(exclude_unset=True)
    update_user = utils.user_update(update_data=update_data, current_user=current_user)
    db.add(update_user)
    db.commit()
    db.refresh(update_user)
    return update_user


#восстановление пароля
@router.post("/password_recovery/")
async def password_recovery(phone_user: PhoneCreate, db: Session = Depends(get_db)):
    user_controll = authentication.get_user(db=db, phone=phone_user.phone)
    if user_controll:
        return JSONResponse({
            'sms_code': '123',
            'id': user_controll.id
        })
    return JSONResponse({'error': 'Пользователь с указанным телефоном не найден'})


#подтверждение по смс
@router.post("/confirmCode/", response_model=Token)
async def confirmCode(sms_message: SmsCode, db: Session = Depends(get_db)):
    if sms_message.sms_code == 123:
        user = authentication.get_user_id(db=db, user_id=str(sms_message.id))
        if not user:
            return JSONResponse({'error': 'Пользователь в приложении не зарегистрован'})

        if sms_message.password is None and sms_message.verification_password is None:
            return Token(access_token=authentication.create_access_token(data={"sub": str(user.id)}))

        if sms_message.password == sms_message.verification_password:
            password_hash = authentication.get_password_hash(password=sms_message.password)
            user.password = password_hash
            db.add(user)
            db.commit()
            db.refresh(user)
            return JSONResponse({'message': 'Пароль изменен'})
        else:
            return JSONResponse({'error': 'Пароли не совпадают'})
    else:
        return JSONResponse({'error': 'Ошибка кода'})


#возвращает всех пользователей
@router.get("/all_users/", response_model=List[ProfileUnf])
async def all_users(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    user_profile = db.query(Players).all()
    return user_profile


#возвращает пользователя по id
@router.get("/user/{user_id}", response_model=ProfileUnf)
async def users_user(user_id: int, current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    user_profile = authentication.get_user_id(db=db, user_id=str(user_id))
    if not user_profile:
        return JSONResponse({'error': 'Пользователь не найден'})
    return user_profile
