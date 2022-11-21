from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sql_app.db import Base
from datetime import datetime


class UserSurvey(Base):
    __tablename__ = 'user_survey'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    question = Column(String(255), autoincrement=False, nullable=False)
    answer_0 = Column(String(255), autoincrement=False, nullable=False)
    answer_1 = Column(String(255), autoincrement=False, nullable=False)
    answer_2 = Column(String(255), autoincrement=False, nullable=True)
    answer_3 = Column(String(255), autoincrement=False, nullable=True)
    published = Column(Boolean, autoincrement=False, nullable=False, default=True)

