from sqlalchemy import Column, Text, Integer
from sql_app.db import Base


class Racquet(Base):
    __tablename__ = 'racquet'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(Text, autoincrement=False, nullable=True)


class Strings(Base):
    __tablename__ = 'strings'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(Text, autoincrement=False, nullable=True)