import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

import app.core.config as cfg

# URL de conexão ao banco de dados padrão

DATABASE_URL = f"postgresql://{cfg.POSTGRES_USER}:{cfg.POSTGRES_PASSWORD}@localhost/{cfg.POSTGRES_DB}"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()