from sqlalchemy.orm import Session

from app.models import Version
from typing import List


def create_version(db: Session, version: Version) -> Version:
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


def get_versions_by_article_id(db: Session, article_id: str) -> List[Version]:
    versions = db.query(Version).filter(Version.article_id == article_id).all()
    return versions


def get_latest_version_by_article_id(db: Session, article_id: str) -> Version:
    latest_version = (
        db.query(Version)
        .filter(Version.article_id == article_id)
        .order_by(Version.created_at.desc())
        .first()
    )
    return latest_version
