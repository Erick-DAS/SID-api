import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

# URL de conexão ao banco de dados padrão
TARGET_DATABASE = "teste"
DATABASE_URL = f"postgresql://teste:teste@localhost/{TARGET_DATABASE}"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
