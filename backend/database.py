# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:motdepasse@localhost/films_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)  # Crée toutes les tables

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
