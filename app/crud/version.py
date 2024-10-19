from sqlalchemy.orm import Session

from app.models import Version


def create_version(db: Session, version: Version):
    db.add(version)
    db.commit()
    db.refresh(version)
    return version
