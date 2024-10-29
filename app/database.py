from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import app.core.config as cfg

# URL de conexão ao banco de dados padrão

DATABASE_URL = cfg.POSTGRES_URL

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
