import time
from profile import authentication
from profile import utils

def dictionary_save(create_scores, user_id):
    """ Функция подготовки данных об игре к записи в БД """

    dict_instance = {
        "f_id": user_id,
        "s_id": create_scores.playerId,
        "match_won": create_scores.isUserWon,
        "played_at": time.strftime('%Y-%m-%d', time.localtime(int(create_scores.gameDate))),
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


def preparing_response(db, all_math, user_id):
    """ Функция возвращает информацию для ответа приложению """

    user_instance = authentication.get_user_id(db, str(all_math.f_id))
    name = utils.name_user(user_instance.name)
    player_avatar = utils.add_avatar(user_instance.__dict__)
    dict_answer = {
        "playerId": user_instance.id,
        "playerFirstName": name[0],
        "playerLastName": name[1],
        "playerAvatarUrl": f"{player_avatar['urlAvatar']}",
        "playerOldPower": 2222,
        "playerNewPower": 3333,
        "userOldPower": 3333,
        "userNewPower": 2222,
        "isUserWin": all_math.match_won,
        "gameDate": 222222222,
        "first_set_f": all_math.first_set_f,
        "first_set_s": all_math.first_set_s,
        "first_set_tie_f": all_math.first_set_tie_f,
        "first_set_tie_s": all_math.first_set_tie_s,
        "second_set_f": all_math.second_set_f,
        "second_set_s": all_math.second_set_s,
        "second_set_tie_f": all_math.second_set_tie_f,
        "second_set_tie_s": all_math.second_set_tie_s,
        "third_set_f": all_math.third_set_f,
        "third_set_s": all_math.third_set_s,
        "third_set_tie_f": all_math.third_set_tie_f,
        "third_set_tie_s": all_math.third_set_tie_s,
        "four_set_f": all_math.fourth_set_f,
        "four_set_s": all_math.fourth_set_s,
        "four_set_tie_f": all_math.fourth_set_tie_f,
        "four_set_tie_s": all_math.fourth_set_tie_s,
        "fifth_set_f": all_math.fifth_set_f,
        "fifth_set_s": all_math.fifth_set_s,
        "fifth_set_tie_f": all_math.fifth_set_tie_f,
        "fifth_set_tie_s": all_math.fifth_set_tie_s
    }

    return dict_answer
