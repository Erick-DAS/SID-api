from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List

from app.models import User, UserRole
from app.logger import logger


def get_user_by_id(db: Session, id: str) -> User:
    user = db.query(User).filter(User.id == id).first()
    return user


def get_user_by_email(db: Session, email: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> User:
    db.delete(user)
    db.commit()
    return user


def list_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    role: UserRole | None = None,
    search: str | None = None,
) -> List[User]:
    query = db.query(User).order_by(User.full_name.asc()).offset(skip).limit(limit)

    if role is not None:
        query = query.filter(User.role == role)

    if search is not None:
        query = query.filter(
            or_(User.full_name.ilike(f"%{search}%"), User.email.ilike(f"%{search}%"))
        )

    users = query.all()

    return users
