from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'postgresql://bottestuser:iKa--Oka80@bugz.su:5432/tptestbot'

    # 'postgresql://postgres:12345@localhost:5432/bd_postgre'

# SQLALCHEMY_DATABASE_URL = "postgres://bottestuser:iKa--Oka80@bugz.su:5432/tptestbot"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
