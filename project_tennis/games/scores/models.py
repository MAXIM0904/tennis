from sqlalchemy import Column, Boolean, Integer, TIMESTAMP, ForeignKey, BIGINT
from sql_app.db import Base
from datetime import datetime


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


    # connection_f_one_id = relationship("Players", foreign_keys='connection_doubles_scores')
    # connection_f_two_id = relationship("Players", foreign_keys='DoublesScores.f_two_id')
    # connection_s_one_id = relationship("Players", foreign_keys='DoublesScores.s_one_id')
    # connection_s_two_id = relationship("Players", foreign_keys='DoublesScores.s_two_id')


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

    # connection_f_id = relationship("Players", back_populates="connection_scores")