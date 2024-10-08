import sqlalchemy as sa
import sqlalchemy.orm as orm

from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))
    full_name = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String)
    role = sa.Column(sa.String)

class Section(Base):
    __tablename__ = "sections"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))
    name = sa.Column(sa.String, unique=True, nullable=False)
    
    main_article_id = sa.Column(sa.ForeignKey("articles.id"), nullable=True)
    main_article = orm.relationship("Article", foreign_keys=[main_article_id])
    
class Article(Base):
    __tablename__ = "articles"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))
    title = sa.Column(sa.String, nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    section = sa.Column(sa.Text, nullable=True)
