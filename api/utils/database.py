from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from api.core.settings import settings


db_uri = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_DB}"
engine = create_engine(db_uri)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
