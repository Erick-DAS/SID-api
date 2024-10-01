from sqlalchemy.orm import Session
from app.models import User


def get_user_by_id(db: Session, id: str):
    user = db.query(User).filter(User.id==id).first()
    return user
