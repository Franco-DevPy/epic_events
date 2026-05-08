from sqlalchemy.orm import sessionmaker
from .connection import engine

SessionLocal = sessionmaker(autocommit=False, bind=engine)


def get_db_session():
    return SessionLocal()
