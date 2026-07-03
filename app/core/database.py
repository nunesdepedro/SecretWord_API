from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker, declarative_base

from sqlalchemy import create_engine
from app.core.config import settings

#creatng connection
db = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()


