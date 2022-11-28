import os
from random import randint
from .models import ConfirmationCodes
from . import schema
from . import authentication

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
    if update_data.get('name') is not None:
        current_user.name = update_data['name']
    if update_data.get('phone') is not None:
        current_user.phone = update_data['phone']
    if update_data.get('initial_rating') is not None:
        current_user.initial_rating = update_data['initial_rating']
    if update_data.get('is_male') is not None:
        current_user.is_male = update_data['is_male']
    if update_data.get('experience') is not None:
        current_user.experience = update_data['experience']
    if update_data.get('secondary_location') is not None:
        current_user.secondary_location = update_data['secondary_location']
    if update_data.get('primary_location') is not None:
        current_user.primary_location = update_data['primary_location']
    if update_data.get('is_full_reg') is not None:
        current_user.is_full_reg = update_data['is_full_reg']
    if update_data.get('rating') is not None:
        current_user.rating = update_data['rating']
    if update_data.get('is_bot_blocked') is not None:
        current_user.is_bot_blocked = update_data['is_bot_blocked']
    if update_data.get('username') is not None:
        current_user.username = update_data['username']
    if update_data.get('doubles_rating') is not None:
        current_user.doubles_rating = update_data['doubles_rating']
    if update_data.get('mixed_rating') is not None:
        current_user.mixed_rating = update_data['mixed_rating']
    if update_data.get('city_id') is not None:
        current_user.city_id = update_data['city_id']
    if update_data.get('referral') is not None:
        current_user.referral = update_data['referral']
    if update_data.get('referral_other') is not None:
        current_user.referral_other = update_data['referral_other']
    if update_data.get('racquet') is not None:
        current_user.racquet = update_data['racquet']
    if update_data.get('racquet_detail') is not None:
        current_user.racquet_detail = update_data['racquet_detail']
    if update_data.get('global_notification') is not None:
        current_user.global_notification = update_data['global_notification']
    if update_data.get('tournament_id') is not None:
        current_user.tournament_id = update_data['tournament_id']
    if update_data.get('corporation') is not None:
        current_user.corporation = update_data['corporation']
    if update_data.get('play_tennis_id') is not None:
        current_user.play_tennis_id = update_data['play_tennis_id']
    if update_data.get('city_other') is not None:
        current_user.city_other = update_data['city_other']
    if update_data.get('offline_tournament_id') is not None:
        current_user.offline_tournament_id = update_data['offline_tournament_id']
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


def answer_user_data(success: bool, message: str, data: dict):
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


def add_avatar(schema_profile):
    """ Функция добавления ссыдок на картинки """
    if schema_profile.get('data'):
        for i_schema_profile in schema_profile['data']:
            if os.path.exists(f"media/{i_schema_profile['id']}/userPhoto/{i_schema_profile['id']}.jpg"):
                i_schema_profile['photo'] = f"media/{i_schema_profile['id']}/userPhoto/{i_schema_profile['id']}.jpg"

    else:
        if os.path.exists(f"media/{schema_profile['id']}/userPhoto/{schema_profile['id']}.jpg"):
            schema_profile['photo'] = f"media/{schema_profile['id']}/userPhoto/{schema_profile['id']}.jpg"

    return schema_profile