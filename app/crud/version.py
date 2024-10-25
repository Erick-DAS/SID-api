from sqlalchemy.orm import Session

from app.models import Version


def create_version(db: Session, version: Version):
    db.add(version)
    db.commit()
    db.refresh(version)
    return version

def get_versions_by_article_id(db: Session, article_id: str):
    versions = db.query(Version).filter(Version.article_id == article_id).all()
    return versions