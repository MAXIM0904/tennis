from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import relationship
from sql_app.db import Base


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

    # connection_user_id = relationship("Players", back_populates="connection_game_orders")
