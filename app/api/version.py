from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.core.auth import get_current_approved_user
import app.crud.version as version_crud
from app.database import get_db
from app.schemas.version import VersionPublic

app = APIRouter()


@app.get("/{article_id}", response_model=List[VersionPublic])
def search_articles(
    article_id: str,
    _: Annotated[User, Depends(get_current_approved_user)],
    db: Session = Depends(get_db),
):
    versions = version_crud.get_versions_by_article_id(db=db, article_id=article_id)
    public_versions = []

    for version in versions:
        public_versions.append(VersionPublic(**version.__dict__))

    if not versions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no past versions to this article",
        )

    return versions
