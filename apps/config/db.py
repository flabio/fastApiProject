from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path

import os

env_path=Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


SQLALCHEMY_DATABASE_URL=f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SEVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()