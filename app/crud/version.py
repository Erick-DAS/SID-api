import re
from typing import List

from sqlalchemy.orm import Session, joinedload

from app.models import Version
from app.schemas.version import VersionMain, VersionPublic


def create_version(db: Session, version: Version) -> Version:
    db.add(version)
    db.commit()
    db.refresh(version)
    return version


def get_version_by_id(db: Session, id: str) -> VersionMain:
    version = db.query(Version).filter(Version.id == id).first()

    plain_content = re.sub(r'<[^>]*>', '', version.content)

    return VersionMain (
        title=version.title,
        content=plain_content,
        version_number=version.version_number,
        created_at=version.created_at
    )


def get_versions_by_article_id(db: Session, article_id: str) -> VersionPublic:
    versions = (
        db.query(Version)
        .options(joinedload(Version.user))
        .filter(Version.article_id == article_id)
        .order_by(Version.created_at.desc())
        .all()
    )

    return [
        VersionPublic(
            id=version.id,
            title=version.title,
            preview=version.preview,
            version_number=version.version_number,
            created_at=version.created_at,
            editor_name=version.user.full_name if version.user else None,
        )
        for version in versions
    ]


def get_latest_version_by_article_id(db: Session, article_id: str) -> Version:
    latest_version = (
        db.query(Version)
        .filter(Version.article_id == article_id)
        .order_by(Version.created_at.desc())
        .first()
    )
    return latest_version
