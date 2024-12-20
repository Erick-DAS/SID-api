import re
from datetime import datetime
from typing import Annotated, List
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
import app.crud.version as version_crud
from app.core.auth import get_current_approved_user, get_current_admin
from app.database import get_db
from app.logger import logger  # noqa: F401
from app.models import Article, SectionName, User, Version
from app.schemas.article import (
    ArticleCreate,
    ArticleMain,
    ArticlePublic,
    ArticleSearch,
    ArticleSearchResponse,
    ArticleUpdate,
)

app = APIRouter()


@app.get("", response_model=ArticleSearchResponse)
async def search_articles(
    skip: int | None = None,
    limit: int | None = None,
    search_type: ArticleSearch | None = None,
    search: str | None = None,
    section: SectionName | None = None,
    db: Session = Depends(get_db),
):
    if search_type == ArticleSearch.AUTHOR:
        total_articles = article_crud.get_articles_by_author_name_search(
            db=db, author=search, section=section
        )
        articles = article_crud.get_articles_by_author_name_search(
            db=db, author=search, section=section, skip=skip, limit=limit
        )
    elif search_type == ArticleSearch.CONTENT:
        total_articles = article_crud.get_articles_by_content(
            db=db, content=search, section=section
        )
        articles = article_crud.get_articles_by_content(
            db=db, content=search, section=section, skip=skip, limit=limit
        )
    else:
        total_articles = article_crud.get_articles_by_section(db=db, section=section)
        articles = article_crud.get_articles_by_section(
            db=db, section=section, skip=skip, limit=limit
        )

    public_articles = []

    for article in articles:
        public_articles.append(ArticlePublic(**article.__dict__))

    return ArticleSearchResponse(articles=public_articles, total=len(total_articles))


@app.get("/{article_id}", response_model=ArticleMain)
async def show_article(
    article_id: str, full_content: bool, db: Session = Depends(get_db)
):
    article = article_crud.get_article_by_id(
        db=db, id=article_id, full_content=full_content
    )

    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return ArticleMain(**article.__dict__)


@app.post("", response_model=ArticlePublic)
async def create_article(
    article: ArticleCreate,
    editor: Annotated[User, Depends(get_current_approved_user)],
    db: Session = Depends(get_db),
):
    plain_content = re.sub(r"<[^>]*>", "", article.content)
    preview = (
        plain_content[:100] + " ..." if len(plain_content) > 100 else plain_content
    )

    new_article = Article(
        id=str(uuid4()),
        title=article.title,
        section=article.section.name,
        content=article.content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        preview=preview,
        author_id=editor.id,
    )

    article_in_db = article_crud.create_article(db=db, article=new_article)

    return ArticlePublic(**article_in_db.__dict__, author_name=editor.full_name)


@app.put("/{article_id}", response_model=ArticleUpdate)
async def update_article(
    article_data: ArticleUpdate,
    editor: Annotated[User, Depends(get_current_approved_user)],
    db: Session = Depends(get_db),
):
    deprecated_article = article_crud.get_article_by_id(
        db=db, id=article_data.id, full_content=True
    )
    if deprecated_article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    plain_content = re.sub(r"<[^>]*>", "", article_data.content)
    preview = (
        plain_content[:100] + " ..." if len(plain_content) > 100 else plain_content
    )

    new_article_data = Article(
        title=article_data.title,
        section=article_data.section.name,
        content=article_data.content,
        updated_at=datetime.now(),
        preview=preview,
    )

    last_version = version_crud.get_latest_version_by_article_id(
        db=db, article_id=article_data.id
    )

    newest_version_number = (
        1 if last_version is None else last_version.version_number + 1
    )

    newest_version = Version(
        id=str(uuid4()),
        created_at=deprecated_article.updated_at,
        title=deprecated_article.title,
        preview=deprecated_article.preview,
        section=deprecated_article.section.name,
        content=deprecated_article.content,
        article_id=deprecated_article.id,
        editor_id=editor.id,
        version_number=newest_version_number,
    )

    version_crud.create_version(db=db, version=newest_version)

    article_in_db = article_crud.update_article(
        db=db, id=article_data.id, new_article_data=new_article_data
    )

    return ArticleUpdate(
        id=article_in_db.id,
        title=article_in_db.title,
        section=article_in_db.section,
        content=article_in_db.content,
        author_name=editor.full_name,
    )

@app.delete("/{article_id}", response_model=ArticleMain)
async def remove_article(
    article_id: str, _: Annotated[User, Depends(get_current_admin)], db: Session = Depends(get_db)
):
    article = article_crud.delete_article(db=db, id=article_id)

    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return ArticleMain(**article.__dict__)
