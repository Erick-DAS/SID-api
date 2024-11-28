from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.version as version_crud
from app.database import get_db
from app.schemas.version import VersionMain, VersionPublic

app = APIRouter()


@app.get("", response_model=List[VersionPublic])
async def search_versions(
    article_id: str,
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


@app.get("/{version_id}", response_model=VersionMain)
async def show_version(version_id: str, db: Session = Depends(get_db)):
    article = version_crud.get_version_by_id(db=db, id=version_id)

    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return VersionMain(**article.__dict__)