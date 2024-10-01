import sqlalchemy as sa

from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))
    full_name = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    role = sa.Column(sa.String)
