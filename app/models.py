import sqlalchemy as sa
import sqlalchemy.orm as orm

from uuid import uuid4
from enum import Enum as PyEnum

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(PyEnum):
    ADMIN = "admin"
    USER = "user"
    WAITING = "waiting for approval"


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))
    full_name = sa.Column(sa.String)
    email = sa.Column(sa.String, unique=True)
    hashed_password = sa.Column(sa.String, nullable=False)
    role = sa.Column(sa.Enum(UserRole), default=UserRole.WAITING, nullable=False)
    motivation = sa.Column(sa.Text, nullable=False)


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
    section = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False)
    preview = sa.Column(sa.String, nullable=False)
    tags = sa.Column(sa.String, nullable=True)

    user_id = sa.Column(sa.ForeignKey("users.id"), nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])

    current_version_id = sa.Column(sa.ForeignKey("versions.id"), nullable=False)
    current_version = orm.relationship("Version", foreign_keys=[current_version_id])

class Version(Base):
    __tablename__ = "versions"

    id = sa.Column(sa.UUID, primary_key=True, default=lambda: str(uuid4()))

    created_at = sa.Column(sa.DateTime, nullable=False)
    content = sa.Column(sa.Text, nullable=False)

    article_id = sa.Column(sa.ForeignKey("articles.id"), nullable=False)
    article = orm.relationship("Article", foreign_keys=[article_id])

    user_id = sa.Column(sa.ForeignKey("users.id"), nullable=False)
    user = orm.relationship("User", foreign_keys=[user_id])
