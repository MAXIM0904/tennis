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
