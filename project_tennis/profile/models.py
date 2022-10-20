from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.orm import relationship
from sql_app.db import Base
from datetime import datetime


class Players(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String(200), autoincrement=False, nullable=False)
    phone = Column(Integer, autoincrement=False, nullable=False)
    experience = Column(Integer, autoincrement=False, nullable=True, default=1) # num от 1 до 4, новичок, любитель, продвинутый, Мастерс
    initial_rating = Column(Float, autoincrement=False, nullable=False)
    primary_location = Column(Integer, autoincrement=False, nullable=True)
    secondary_location = Column(Integer, autoincrement=False, nullable=True)
    is_male = Column(Boolean, autoincrement=False, nullable=False)
    registered_at = Column(DateTime,  autoincrement=False, nullable=True, default=datetime.utcnow())
    is_full_reg = Column(Boolean, autoincrement=False, nullable=True, default=True)
    rating = Column(Float, autoincrement=False, nullable=False, default=0)
    is_bot_blocked = Column(Boolean, autoincrement=False, nullable=True, default=False)
    username = Column(Text, autoincrement=False, nullable=True)
    doubles_rating = Column(Float, autoincrement=False, nullable=True)
    mixed_rating = Column(Float, autoincrement=False, nullable=True)
    city_id = Column(Integer, autoincrement=False, nullable=False, default=1)
    referral = Column(Integer, autoincrement=False, nullable=True)
    referral_other = Column(Text, autoincrement=False, nullable=True)
    racquet = Column(Integer, autoincrement=False, nullable=True)
    racquet_detail = Column(Text, autoincrement=False, nullable=True)
    global_notification = Column(Boolean, autoincrement=False, nullable=True, default=False)
    tournament_id = Column(Integer, autoincrement=False, nullable=True)
    corporation = Column(Integer, autoincrement=False, nullable=True)
    play_tennis_id = Column(String(50), autoincrement=False, nullable=True)
    city_other = Column(Text, autoincrement=False, nullable=True)
    offline_tournament_id = Column(Integer, nullable=True)
    password = Column(String(100), autoincrement=False, nullable=True)

    # connection_game_orders = relationship("GameOrders", back_populates="connection_user_id")
    # connection_doubles_scores = relationship("DoublesScores", back_populates="connection_f_one_id")

    # connection_scores = relationship("Scores", back_populates="connection_f_id")
