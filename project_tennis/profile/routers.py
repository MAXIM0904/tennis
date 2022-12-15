from fastapi import APIRouter
from sqlalchemy.orm import Session
from . import schema
from fastapi import Depends
from sql_app.db import get_db, create_bd, delete_bd
from .models import Players, Favorite
from . import authentication
from . import utils
from sqlalchemy import and_

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

    # тестовая функция
    if user.phone == 79150000000:
        answer = utils.answer_user_data(True, "Код отправлен", {
            "phone": 79150000000,
            "code": 1111
        })
        return answer

    answer = utils.answer_user(False, "Пользователь с данным номер телефона уже зарегистрирован. Войдите в аккаунт")
    return answer


@router.post("/confirmCode")
async def confirm_code(profile: schema.ProfileCreate, db: Session = Depends(get_db)):
    """ Функция проверки ввода кода верификации и регистрации пользователя """
    user = utils.get_confirmation(db, profile.phone)

    # тестовый пользователь
    if profile.phone == 79150000000 and profile.code == 1111:
        user = authentication.get_user_phone(db=db, phone=str(profile.phone))
        password_hash = authentication.get_password_hash(password=profile.password)
        user.password = password_hash
        create_bd(db=db, db_profile=user)
        access_token = authentication.create_access_token(data={"sub": str(user.id)})
        token = schema.Token(id=user.id, token=access_token).dict()
        answer = utils.answer_user_data(True, "Код введен верно", token)
        return answer

    if user:
        if user.code == profile.code:
            profile = utils.preparing_profile_recording(profile=profile)

            # временная функция генерации id
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
async def read_users_me(current_user: Players = Depends(authentication.get_current_user),
                        db: Session = Depends(get_db)):
    """ Получить информацию о пользователе для ЛК """
    preparing_response = utils.preparing_user_profile(current_user, db)
    utils.add_avatar(preparing_response)
    answer = utils.answer_user_data(True, "", preparing_response)
    return answer


@router.get("/")
async def all_users(
        page: int = 1,
        cityId: int = None,
        powerMin: int = None,
        powerMax: int = None,
        name: str = None,
        districtId: int = None,
        isMale: bool = None,
        isFavorite: bool = None,
        current_user: dict = Depends(authentication.get_current_user),
        db: Session = Depends(get_db)
):
    """ Функция возвращает всех пользователей """
    user_list = []
    queries = [Players.id != current_user.id]
    limit_page = 40
    if page <= 0:
        page = 1
    offset_page = (page - 1) * limit_page

    if name:
        queries.append(Players.name.ilike(f"%{name}%"))

    if cityId:
        queries.append(Players.city_id == cityId)

    if powerMax or powerMin:
        if powerMin and not powerMax:
            powerMax = 99999999999999
        elif powerMax and not powerMin:
            powerMin = 0
        queries.append(Players.rating >= powerMin)
        queries.append(Players.rating <= powerMax)

    if isMale is not None:
        queries.append(Players.is_male == isMale)

    if districtId:
        queries.append(Players.district_id == districtId)

    if isFavorite:
        user_profile = []
        favorite = db.query(Favorite).filter(Favorite.id_user == current_user.id).all()
        for i in favorite:
            profile_favorite = authentication.get_user_id(db, str(i.id_favorite))
            user_profile.append(profile_favorite)
    elif len(queries) > 1:
        user_profile = db.query(Players).filter(*queries).offset(offset_page).limit(limit_page).all()
    else:
        user_profile = db.query(Players).offset(offset_page).limit(limit_page).all()

    for i_user_profile in user_profile:
        schema_profile = utils.preparing_user_profile(i_user_profile, db, current_user.id)
        utils.add_avatar(schema_profile)
        schema_profile = schema.ShemaAnotherPlayer(**schema_profile).dict()
        if isFavorite is False:
            if schema_profile["isFavorite"]:
                continue
        user_list.append(schema_profile)

    answer = utils.answer_user_data(True, "", user_list)
    return answer


@router.get("/{user_id}")
async def users_user(user_id: int,
                     current_user: Players = Depends(authentication.get_current_user),
                     db: Session = Depends(get_db)):
    """ Функция возвращает пользователя по id """

    user_profile = authentication.get_user_id(db=db, user_id=str(user_id))
    if user_profile:
        schema_profile = utils.preparing_user_profile(user_profile, db, current_user.id)
        utils.add_avatar(schema_profile)
        answer = utils.answer_user_data(True, "", schema_profile)
        return answer

    answer = utils.answer_user(False, "Пользователь не найден")
    return answer


@router.put("/profile")
async def users_update(user_update: schema.ProfileUpdate,
                       current_user: Players = Depends(authentication.get_current_user),
                       db: Session = Depends(get_db)):
    """ Изменение данных пользователя"""

    update_data = user_update.dict(exclude_unset=True)
    update_user = utils.user_update(update_data=update_data, current_user=current_user)
    create_bd(db=db, db_profile=update_user)

    preparing_response = utils.preparing_user_profile(current_user, db)
    utils.add_avatar(preparing_response)
    answer = utils.answer_user_data(True, "", preparing_response)
    return answer


@router.post("/favorite")
async def create_favorite(favorite_id: schema.SchemaFavorite,
                          current_user: Players = Depends(authentication.get_current_user),
                          db: Session = Depends(get_db)):
    """ Функция добавления фаворитов """
    db_profile = authentication.get_user_id(db=db, user_id=str(favorite_id.favoriteId))
    if db_profile:
        favorite = Favorite(id_user=str(current_user.id), id_favorite=str(db_profile.id))
        create_bd(db=db, db_profile=favorite)
        answer = utils.answer_user(True, "Запись успешно сохранена.")
        return answer

    answer = utils.answer_user(False, "Пользователь не найден.")
    return answer


@router.delete("/deleteFavorite")
async def delete_favorite(favorite_id: schema.SchemaFavorite,
                          current_user: Players = Depends(authentication.get_current_user),
                          db: Session = Depends(get_db)):
    """ Функция удаления фаворитов """
    db_profile = authentication.get_user_id(db=db, user_id=str(favorite_id.favoriteId))

    favorite = db.query(Favorite).filter(
        and_(Favorite.id_user == current_user.id, Favorite.id_favorite == db_profile.id)
    ).first()

    if favorite:
        delete_bd(db, favorite)
        answer = utils.answer_user(True, "Запись успешно удалена")
        return answer

    answer = utils.answer_user(False, "Ошибка удаления")
    return answer
