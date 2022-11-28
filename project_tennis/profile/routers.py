from fastapi import APIRouter
from sqlalchemy.orm import Session
from . import schema
from fastapi import Depends
from sql_app.db import get_db, create_bd, delete_bd
from .models import Players
from . import authentication
from . import utils


router = APIRouter()


@router.post("/registration_code")
async def registration_code(number_phone: schema.SchemaPhone, db: Session = Depends(get_db)):
    """ Функция направления кода верификации при регистрации """
    number_phone = number_phone.dict()
    user = authentication.get_user_phone(db=db, phone=number_phone['phone'])
    if not user:
        code = utils.random_code()
        number_phone['code'] = code
        db_profile = utils.confirmation_controll(db=db, phone_dict=number_phone)
        create_bd(db=db, db_profile=db_profile)
        answer = utils.answer_user_data(True, "Код отправлен", number_phone)
        return answer

    answer = utils.answer_user(False, "Пользователь с данным номер телефона уже зарегистрирован. Войдите в аккаунт")
    return answer


@router.post("/confirmCode")
async def confirmcode(profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """ Функция проверки ввода кода верификации и регистрации пользователя """
    user = utils.get_confirmation(db, profile.phone)
    if user:
        if user.code == profile.code:
            profile = utils.preparing_profile_recording(profile=profile)

            #временная функция генерации id
            profile = utils.profile_id(db, profile)

            db_profile = Players(**profile)
            create_bd(db=db, db_profile=db_profile)

            access_token = authentication.create_access_token(data={"sub": str(db_profile.id)})
            token = schema.Token(id=db_profile.id, token=access_token).dict()
            answer = utils.answer_user_data(True, "Код введен верно", token)
            delete_bd(db, user)
            return answer

        answer = utils.answer_user(False, "Вы ввели неверный код подтверждения")
        return answer

    answer = utils.answer_user(False, "Запрос на получение кода по СМС не направлялся")
    return answer


@router.post("/password_recovery")
async def password_recovery(number_phone: schema.SchemaPhone, db: Session = Depends(get_db)):
    """ Функция направления кода верификации при восстановлении пароля """
    number_phone = number_phone.dict()
    user = authentication.get_user_phone(db=db, phone=number_phone['phone'])
    if user:
        code = utils.random_code()
        number_phone['code'] = code
        db_profile = utils.confirmation_controll(db=db, phone_dict=number_phone)
        create_bd(db=db, db_profile=db_profile)
        answer = utils.answer_user_data(True, "Код отправлен", number_phone)
        return answer
    answer = utils.answer_user(False, "Пользователь с данным номер телефона не зарегистрирован. Зарегистрируйтесь.")
    return answer


@router.post("/change_password")
async def change_password(profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """ Функция проверки ввода кода верификации при изменении пароля """
    user = utils.get_confirmation(db, profile.phone)
    if user:
        if user.code == profile.code:
            db_profile = authentication.get_user_phone(db=db, phone=str(profile.phone))
            password_hash = authentication.get_password_hash(password=profile.password)
            db_profile.password = password_hash
            create_bd(db=db, db_profile=db_profile)
            answer = utils.answer_user(True, "Данные успешно сохранены")
            delete_bd(db, user)
            return answer

        answer = utils.answer_user(False, "Вы ввели неверный код подтверждения")
        return answer

    answer = utils.answer_user(False, "Запрос на получение кода по СМС не направлялся")
    return answer


@router.post("/auth")
async def login_for_access_token(form_data: schema.ProfileAuth, db: Session = Depends(get_db)):
    """ Авторизация существующего пользователя """
    db_profile = authentication.authenticate_user(db=db, phone=form_data.phone, password=form_data.password)
    if not isinstance(db_profile, str):
        access_token = authentication.create_access_token(data={"sub": str(db_profile.id)})
        token = schema.Token(id=db_profile.id, token=access_token).dict()
        answer = utils.answer_user_data(True, "Пользователь успешно авторизован", token)
        return answer

    answer = utils.answer_user(False, db_profile)
    return answer


@router.get("/profile")
async def read_users_me(current_user: Players = Depends(authentication.get_current_user)):
    """ Получить информацию о пользователе для ЛК """
    schema_profile = schema.ProfileUnf(**current_user.__dict__).dict()
    utils.add_avatar(schema_profile)
    answer = utils.answer_user_data(True, "", schema_profile)
    return answer


@router.get("/")
async def all_users(current_user: dict = Depends(authentication.get_current_user), db: Session = Depends(get_db)):
    """ Функция возвращает всех пользователей """
    user_profile = db.query(Players).all()
    schema_profile = schema.ProfileResponseModel(success=True, message="", data=user_profile).dict()
    utils.add_avatar(schema_profile)
    return schema_profile


@router.get("/{user_id}")
async def users_user(user_id: int,
                     current_user: Players = Depends(authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает пользователя по id """

    user_profile = authentication.get_user_id(db=db, user_id=str(user_id))
    if user_profile:
        schema_profile = schema.ProfileUnf(**current_user.__dict__).dict()
        utils.add_avatar(schema_profile)
        answer = utils.answer_user_data(True, "", schema_profile)
        return answer

    answer = utils.answer_user(False, "Пользователь не найден")
    return answer


@router.put("/profile")
async def users_update(user_update:schema.ProfileUpdate,
                       current_user: Players = Depends(authentication.get_current_user),
                       db: Session = Depends(get_db)):
    """ Изменение данных пользователя"""
    update_data = user_update.dict(exclude_unset=True)
    update_user = utils.user_update(update_data=update_data, current_user=current_user)
    create_bd(db=db, db_profile=update_user)
    answer = utils.answer_user(True, "Данные успешно сохранены")
    return answer
