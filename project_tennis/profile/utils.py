import os
from random import randint

from games.models import Scores
from .models import ConfirmationCodes, Favorite
from . import schema
from . import authentication
import time
import datetime
from geo.models import Cities, District, Countries
from geo.schema import SchemaCountry, SchemaDistrict
from inventory.models import Racquet, Strings
from inventory.schema import SchemaInventory
from sqlalchemy import and_


#временная функция
from .models import Players


def profile_id(db, profile):
    """ Временная функция генерации id Players"""
    while True:
        id_user = randint(7000000000, 99999999999999)
        user = db.query(Players).get(id_user)
        if not user:
            profile['id'] = id_user
            return profile


def random_code():
    """Функция генерации проверочного кода"""
    return randint(1000, 9999)


def user_update(update_data, current_user):
    if update_data.get('lastName') is not None or update_data.get('firstName') is not None:
        if update_data.get('lastName') is not None and update_data.get('firstName') is not None:
            current_user.name = f"{update_data['lastName']} {update_data['firstName']}"

        elif update_data.get('lastName') is not None:
            name = current_user.name.split()
            if len(name) <= 0:
                name.append(update_data['lastName'])
            else:
                name[0] = update_data['lastName']
        else:
            name = current_user.name.split()
            if len(name) <= 1:
                name.append(update_data['firstName'])
            else:
                name[1] = update_data['firstName']

            current_user.name = str(" ".join(name))

    if update_data.get('phone') is not None:
        current_user.phone = update_data['phone']
    if update_data.get('telegram') is not None:
        current_user.username = update_data['telegram']
    if update_data.get('cityId') is not None:
        current_user.city_id = update_data['cityId']
    if update_data.get('districtId') is not None:
        current_user.district_id = update_data['districtId']
    if update_data.get('birthDate') is not None:
        current_user.birthDate = update_data['birthDate']
    if update_data.get('is_male') is not None:
        current_user.is_male = update_data['is_male']
    if update_data.get('gameStyle') is not None:
        current_user.game_style = update_data['gameStyle']
    if update_data.get('isRightHand') is not None:
        current_user.is_right_hand = update_data['isRightHand']
    if update_data.get('isOneBackhand') is not None:
        current_user.is_one_backhand = update_data['isOneBackhand']
    if update_data.get('ground') is not None:
        current_user.ground = update_data['ground']
    if update_data.get('shoesName') is not None:
        current_user.shoes_name = update_data['shoesName']
    if update_data.get('racquetId') is not None:
        current_user.racquet = update_data['racquetId'][0]
    if update_data.get('stringsId') is not None:
        current_user.strings_id = update_data['stringsId'][0]
    if update_data.get('birthDate') is not None:
        time_user = int(update_data['birthDate'])
        time.strftime('%Y-%m-%d', time.localtime(time_user))
        current_user.birth_date = time.strftime('%Y-%m-%d', time.localtime(time_user))
    return current_user


def get_confirmation(db, phone: int):
    """ Функция поиска пользователя по номеру телефона в таблице ConfirmationCodes"""
    confirmation = db.query(ConfirmationCodes).filter(ConfirmationCodes.phone == phone).first()
    if confirmation:
        return confirmation
    else:
        return False


def confirmation_controll(db, phone_dict: dict):
    """
    Функция контролирует наличие одинаковых записей в таблице ConfirmationCodes.
    При наличии повторов перезаписывается код верификации (code)
    """
    db_profile = get_confirmation(db=db, phone=phone_dict['phone'])
    if not db_profile:
        db_profile = ConfirmationCodes(**phone_dict)
    else:
        db_profile.code = phone_dict['code']

    return db_profile


def answer_user_data(success: bool, message: str, data: [dict|list]):
    """ Функция генерации ответа пользователю c data """
    answer = schema.PositiveResponseModel(
        success=success,
        message=message,
        data=data
    )
    return answer


def answer_user(success: bool, message: str):
    """ Функция генерации ответа пользователю без data """
    answer = schema.ErrorResponseModel(
        success=success,
        message=message
    )
    return answer


def preparing_profile_recording(profile):
    """ Функция подготовки информации о пользователе к записи в базу данных"""
    profile = profile.dict()
    del profile['code']
    hash_password = authentication.get_password_hash(password=profile['password'])
    profile['password'] = hash_password
    return profile


def url_avatar(url):
    url_host = "http://127.0.0.1:8000" #"http://bugz.su:8000"
    return f"{url_host}/image/{url}"


def add_avatar(schema_profile):
    """ Функция добавления ссылок на картинки """

    if schema_profile.get('data'):
        for i_schema_profile in schema_profile['data']:
            if os.path.exists(f"media/{i_schema_profile['id']}/userPhoto/{i_schema_profile['id']}.jpg"):
                i_schema_profile['urlAvatar'] = url_avatar(f"media/{i_schema_profile['id']}/userPhoto/{i_schema_profile['id']}.jpg")

    else:
        if os.path.exists(f"media/{schema_profile['id']}/userPhoto/{schema_profile['id']}.jpg"):
            schema_profile['urlAvatar'] = url_avatar(f"media/{schema_profile['id']}/userPhoto/{schema_profile['id']}.jpg")

    if not schema_profile.get('urlAvatar'):
        schema_profile['urlAvatar'] = None

    return schema_profile


def name_user(name):
    """Функция преобразования имени"""
    name = name.split()
    if len(name) <= 1:
        name.append(None)
    return name


def changing_time_format(date_to_change):
    """Функция преобразования времени в прошедшее с 1970 года"""
    time_math = date_to_change.strftime('%Y-%m-%d')
    time_birth = str(time_math).split("-")
    dt = datetime.datetime(int(time_birth[0]), int(time_birth[1]), int(time_birth[2]))
    return int(dt.timestamp())


def preparing_user_profile(current_user, db, user_id=None):
    """Функция формирует профиль пользователя для приложения """
    name = name_user(current_user.name)
    country_id = None

    if current_user.birth_date:
        current_user.birth_date = changing_time_format(date_to_change=current_user.birth_date)

    if current_user.city_id:
        city = db.query(Cities).get(current_user.city_id)
        current_user.city_id = SchemaCountry(**city.__dict__).dict()
        country = db.query(Countries).get(city.country_id)
        country_id = SchemaCountry(**country.__dict__).dict()

    if current_user.district_id:
        district = db.query(District).get(current_user.district_id)
        current_user.district_id = SchemaDistrict(**district.__dict__).dict()

    if current_user.racquet:
        racquet = db.query(Racquet).get(current_user.racquet)
        if racquet:
            current_user.racquet = SchemaInventory(**racquet.__dict__).dict()
        else:
            current_user.racquet = None

    if current_user.strings_id:
        strings = db.query(Strings).get(current_user.strings_id)
        current_user.racquet = SchemaInventory(**strings.__dict__).dict()

    count_matches = len(db.query(Scores).filter(Scores.f_id == current_user.id).all())

    dict_answer = {
        "id": current_user.id,
        "firstName": name[0],
        "lastName": name[1],
        "phone": current_user.phone,
        "telegram": current_user.username,
        "country": country_id,
        "city": current_user.city_id,
        "district": current_user.district_id,
        "birthDate": current_user.birth_date,
        "isMale": current_user.is_male,
        "gameStyle": current_user.game_style,
        "isRightHand": current_user.is_right_hand,
        "isOneBackhand": current_user.is_one_backhand,
        "ground": current_user.ground,
        "shoesName": current_user.shoes_name,
        "racquet": current_user.racquet,
        "strings": current_user.racquet,
        "countOfMatches": count_matches,
        "power": round(current_user.rating),
        "lastGameDate": 486545,
        "lastActivityDate": 454655
    }
    if user_id:
        favorite = db.query(Favorite).filter(
            and_(Favorite.id_user == user_id, Favorite.id_favorite == current_user.id)
        ).first()

        if favorite:
            is_favorite = True
        else:
            is_favorite = False

        dict_answer['isFavorite'] = is_favorite

    return dict_answer


def create_bot_user(db, profile):
    """ Вспомогательная функция для быстрого добавления в базу данных пользователей """
    from sql_app.db import create_bd

    for i in range(150):
        #добавить пользователя в базу данных
        # profile['name'] = f"testuser{i}"
        # profile['phone'] += 1
        # profile['id'] += 1
        # db_profile = Players(**profile)
        # create_bd(db=db, db_profile=db_profile)

        #добавить поле
        name = f"testuser{i}"
        user_profile = db.query(Players).filter(Players.name == name).first()
        if user_profile:
            user_profile.username = f"@Vova1970.{i}"
        create_bd(db=db, db_profile=user_profile)
