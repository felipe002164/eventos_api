from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:clave123@localhost:5435/eventos")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_tablas():
    Base.metadata.create_all(engine) 