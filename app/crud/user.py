from sqlalchemy.orm import Session
from app.models import User


def get_user_by_id(db: Session, id: str):
    user = db.query(User).filter(User.id == id).first()
    return user


def get_user_by_email(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
