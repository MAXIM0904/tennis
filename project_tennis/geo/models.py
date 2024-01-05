from sqlalchemy import Column, Integer, String, Text
from sql_app.db import Base


class Countries(Base):
    __tablename__ = 'countries'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String(50), autoincrement=False, nullable=False)
    flag = Column(Text, autoincrement=False, nullable=True)
    play_tennis_id = Column(String(50), autoincrement=False, nullable=True)
    code = Column(Text, autoincrement=False, nullable=True)


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, nullable=False)
    country_id = Column(Integer, autoincrement=False, nullable=False)
    name = Column(String(50), autoincrement=False, nullable=False)
    channel_id = Column(Integer, autoincrement=False, nullable=True)
    channel_name = Column(Text, autoincrement=False, nullable=True)
    chat_id = Column(Integer, autoincrement=False, nullable=True)
    chat_name = Column(Text, autoincrement=False, nullable=True)
    play_tennis_id = Column(String(100), autoincrement=False, nullable=True)


class District(Base):
    __tablename__ = 'district'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, nullable=False)
    cityid = Column(Integer, autoincrement=False, nullable=True)
    name = Column(Text, autoincrement=False, nullable=True)
