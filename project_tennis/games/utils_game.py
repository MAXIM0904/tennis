from random import randint

from sqlalchemy import desc
from games.models import Ratings
from profile import authentication
from profile import utils
from sql_app.db import create_bd


def dictionary_save(create_scores, user_id):
    """ Функция подготовки данных об игре к записи в БД """

    dict_instance = {
        "f_id": user_id,
        "s_id": create_scores.playerId,
        "match_won": create_scores.isUserWon,
        "played_at": utils.time_save(create_scores.gameDate),
        "sets": len(create_scores.result),
        "status": 1,
    }

    for i_result in create_scores.result:
        if i_result["numberSet"] == 1 and not i_result["isTie"]:
            dict_instance["first_set_f"] = i_result["countUser"]
            dict_instance["first_set_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 1 and i_result["isTie"]:
            dict_instance["first_set_tie_f"] = i_result["countUser"]
            dict_instance["first_set_tie_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 2 and not i_result["isTie"]:
            dict_instance["second_set_f"] = i_result["countUser"]
            dict_instance["second_set_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 2 and i_result["isTie"]:
            dict_instance["second_set_tie_f"] = i_result["countUser"]
            dict_instance["second_set_tie_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 3 and not i_result["isTie"]:
            dict_instance["third_set_f"] = i_result["countUser"]
            dict_instance["third_set_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 3 and i_result["isTie"]:
            dict_instance["third_set_tie_f"] = i_result["countUser"]
            dict_instance["third_set_tie_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 4 and not i_result["isTie"]:
            dict_instance["fourth_set_f"] = i_result["countUser"]
            dict_instance["fourth_set_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 4 and i_result["isTie"]:
            dict_instance["fourth_set_tie_f"] = i_result["countUser"]
            dict_instance["fourth_set_tie_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 5 and not i_result["isTie"]:
            dict_instance["fifth_set_f"] = i_result["countUser"]
            dict_instance["fifth_set_s"] = i_result["countPlayer"]

        elif i_result["numberSet"] == 5 and i_result["isTie"]:
            dict_instance["fifth_set_tie_f"] = i_result["countUser"]
            dict_instance["fifth_set_tie_s"] = i_result["countPlayer"]

    return dict_instance


def user_power(user_profile, id_match, db):
    # убрать после получения реальных данных
    id_match = "507"
    user_profile.id = '23392545'

    db_user_ratings = db.query(Ratings).filter(
        Ratings.user_id == user_profile.id).order_by(desc(Ratings.score_id)).all()
    db_user_match = db.query(Ratings).filter(
        Ratings.score_id == id_match).first()

    index = db_user_ratings.index(db_user_match)
    OldPower = db_user_ratings[index].rating
    NewPower = db_user_ratings[index - 1].rating
    return OldPower, NewPower


def preparing_response(db, all_match):
    """ Функция возвращает информацию для ответа приложению """

    user_1 = authentication.get_user_id(db, all_match.f_id)
    user_2 = authentication.get_user_id(db, all_match.s_id)
    name_user_1 = utils.name_user(user_1.name)
    name_user_2 = utils.name_user(user_2.name)
    player_avatar1 = utils.add_avatar(user_1.__dict__)
    player1OldPower, player1NewPower = user_power(user_1, all_match.id, db)
    player_avatar2 = utils.add_avatar(user_2.__dict__)
    player2OldPower, player2NewPower = user_power(user_2, all_match.id, db)

    if all_match.played_at:
        date_match = utils.changing_time_format(all_match.played_at)
    else:
        date_match = None

    dict_answer = {
        "matchId": all_match.id,
        "player1Id": user_1.id,
        "player1FirstName": name_user_1[0],
        "player1LastName": name_user_1[1],
        "player1AvatarUrl": f"{player_avatar1['urlAvatar']}",
        "player1OldPower": 2222,
        "player1NewPower": 3333,

        "player2Id": user_2.id,
        "player2FirstName": name_user_2[0],
        "player2LastName": name_user_2[1],
        "player2AvatarUrl": f"{player_avatar2['urlAvatar']}",
        "player2OldPower": 156,
        "player2NewPower": 1256,


        "isPlayer1Win": all_match.match_won,
        "gameDate": date_match,
        "result": [
            {
                "numberSet": 1,
                "countPlayer": all_match.first_set_f,
                "countUser": all_match.first_set_s,
                "isTie": False,
                "isSuperTie": False
            },
            {
                "numberSet": 1,
                "countPlayer": all_match.first_set_tie_f,
                "countUser": all_match.first_set_tie_s,
                "isTie": True,
                "isSuperTie": False
            },
            {
                "numberSet": 2,
                "countPlayer": all_match.second_set_f,
                "countUser": all_match.second_set_s,
                "isTie": False,
                "isSuperTie": False
            },
            {
                "numberSet": 2,
                "countPlayer": all_match.second_set_tie_f,
                "countUser": all_match.second_set_tie_s,
                "isTie": True,
                "isSuperTie": False
            },
            {
                "numberSet": 3,
                "countPlayer": all_match.third_set_f,
                "countUser": all_match.third_set_s,
                "isTie": False,
                "isSuperTie": False
            },
            {
                "numberSet": 3,
                "countPlayer": all_match.third_set_tie_f,
                "countUser": all_match.third_set_tie_s,
                "isTie": True,
                "isSuperTie": False
            },
            {
                "numberSet": 4,
                "countPlayer": all_match.fourth_set_f,
                "countUser": all_match.fourth_set_s,
                "isTie": False,
                "isSuperTie": False
            },
            {
                "numberSet": 4,
                "countPlayer": all_match.fourth_set_tie_f,
                "countUser": all_match.fourth_set_tie_s,
                "isTie": True,
                "isSuperTie": False
            },
            {
                "numberSet": 5,
                "countPlayer": all_match.fifth_set_f,
                "countUser": all_match.fifth_set_s,
                "isTie": False,
                "isSuperTie": False
            },
            {
                "numberSet": 5,
                "countPlayer": all_match.fifth_set_tie_f,
                "countUser": all_match.fifth_set_tie_s,
                "isTie": True,
                "isSuperTie": False
            }
        ]
    }

    return dict_answer


def profile_ratings_id(db, profile):
    """ Временная функция генерации id"""
    while True:
        id_user = randint(500, 9999999)
        user = db.query(Ratings).get(id_user)
        if not user:
            profile['id'] = id_user
            return profile


def save_rating(db, profile_ratings):
    profile_ratings_id(db, profile_ratings)
    db_create_ratings = Ratings(**profile_ratings)
    create_bd(db=db, db_profile=db_create_ratings)
    return True
