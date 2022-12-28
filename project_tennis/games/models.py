from sqlalchemy import Column, Boolean, Integer, TIMESTAMP, ForeignKey, BIGINT, String, Date
from sql_app.db import Base
from datetime import datetime


class GameOrders(Base):
    __tablename__ = 'game_orders'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=True)
    loc_szao = Column(Boolean, autoincrement=False, nullable=True)
    loc_sao = Column(Boolean, autoincrement=False, nullable=True)
    loc_svao = Column(Boolean, autoincrement=False, nullable=True)
    loc_zao = Column(Boolean, autoincrement=False, nullable=True)
    loc_cao = Column(Boolean, autoincrement=False, nullable=True)
    loc_vao = Column(Boolean, autoincrement=False, nullable=True)
    loc_uzao = Column(Boolean, autoincrement=False, nullable=True)
    loc_uao = Column(Boolean, autoincrement=False, nullable=True)
    loc_uvao = Column(Boolean, autoincrement=False, nullable=True)
    game_type = Column(Integer, autoincrement=False, nullable=False)
    game_date = Column(Date, autoincrement=False, nullable=True)
    game_time = Column(Integer, autoincrement=False, nullable=True)
    duration = Column(Integer, autoincrement=False, nullable=True)
    tennis_site = Column(String(255), autoincrement=False, nullable=True)
    pay = Column(Integer, autoincrement=False, nullable=False)
    game_time_hh = Column(Boolean, autoincrement=False, nullable=True)

class DoublesScores(Base):
    __tablename__ = 'doubles_scores'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    f_one_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    f_two_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    s_one_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    s_two_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    match_won = Column(Boolean, autoincrement=False, nullable=False)
    first_set_f = Column(Integer, autoincrement=False, nullable=False)
    first_set_s = Column(Integer, autoincrement=False, nullable=False)
    first_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    first_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    second_set_f = Column(Integer, autoincrement=False, nullable=True)
    second_set_s = Column(Integer, autoincrement=False, nullable=True)
    second_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    second_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    third_set_f = Column(Integer, autoincrement=False, nullable=True)
    third_set_s = Column(Integer, autoincrement=False, nullable=True)
    third_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    third_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    status = Column(Integer, autoincrement=False, nullable=False)
    played_at = Column(TIMESTAMP, autoincrement=False, nullable=True, default=datetime.utcnow())
    fourth_set_f = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_s = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_f = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_s = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    sets = Column(Integer, autoincrement=False, nullable=True)

class Scores(Base):
    __tablename__ = 'scores'

    id = Column(BIGINT, primary_key=True, index=True, unique=True)
    f_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    s_id = Column(Integer, ForeignKey("players.id", ondelete='CASCADE'), autoincrement=False, nullable=False)
    match_won = Column(Boolean, autoincrement=False, nullable=False)
    first_set_f = Column(Integer, autoincrement=False, nullable=False)
    first_set_s = Column(Integer, autoincrement=False, nullable=False)
    first_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    first_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    second_set_f = Column(Integer, autoincrement=False, nullable=True)
    second_set_s = Column(Integer, autoincrement=False, nullable=True)
    second_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    second_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    third_set_f = Column(Integer, autoincrement=False, nullable=True)
    third_set_s = Column(Integer, autoincrement=False, nullable=True)
    third_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    third_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    status = Column(Integer, autoincrement=False, nullable=False)
    played_at = Column(TIMESTAMP, autoincrement=False, nullable=True, default=datetime.utcnow())
    fourth_set_f = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_s = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    fourth_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_f = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_s = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_tie_f = Column(Integer, autoincrement=False, nullable=True)
    fifth_set_tie_s = Column(Integer, autoincrement=False, nullable=True)
    sets = Column(Integer, autoincrement=False, nullable=True)


class Ratings(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    user_id = Column(Integer, autoincrement=False, nullable=True)
    score_id = Column(Integer, autoincrement=False, nullable=True)
    rating = Column(Integer, autoincrement=False, nullable=True)
    rd = Column(Integer, autoincrement=False, nullable=True)
