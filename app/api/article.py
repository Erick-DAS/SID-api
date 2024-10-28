from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
import app.crud.version as version_crud
from app.core.auth import get_current_user
from app.database import get_db
from app.schemas.article import ArticleCreate, ArticlePublic, ArticleSearch, ArticleMain, ArticleUpdate
from app.models import Article, SectionName, Version

from uuid import UUID

app = APIRouter()


@app.get("", response_model=List[ArticlePublic])
def search_articles(
    search_type: ArticleSearch | None = None,
    search: str | None = None,
    section: SectionName | None = None,
    db: Session = Depends(get_db),
):
    if search_type == ArticleSearch.AUTHOR:
        articles = article_crud.get_articles_by_author_name_search(
            db=db, author=search, section=section
        )
    elif search_type == ArticleSearch.CONTENT:
        articles = article_crud.get_articles_by_content(
            db=db, content=search, section=section
        )
    else:
        articles = article_crud.get_articles_by_section(db=db, section=section)

    public_articles = []

    for article in articles:
        public_articles.append(ArticlePublic(**article.__dict__))

    return articles

@app.get("/{user_id}", response_model=List[ArticlePublic])
def get_user_articles(
    user_id: str | UUID,
    db: Session = Depends(get_db),
):
    articles = article_crud.get_articles_by_author_id(db=db, user_id=str(user_id))

    public_articles = []

    for article in articles:
        public_articles.append(ArticlePublic(**article.__dict__))

    return public_articles


@app.get("/article/show/{article_id}", response_model=ArticleMain)
def show_article(article_id: str, db: Session = Depends(get_db)):
    article = article_crud.get_article_by_id(db=db, id=article_id)

    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    return ArticleMain(**article.__dict__)


@app.post("/article/create/", response_model=ArticlePublic)
def create_article(article: ArticleCreate, db: Session = Depends(get_current_user)):
    preview = (
        article.content[:300] + " ..."
        if len(article.content) > 300
        else article.content
    )

    new_article = Article(
        id=str(uuid4()),
        title=article.title,
        section=article.section,
        content=article.content,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        preview=preview,
        author_id=article.author_id,
    )
    article_in_db = article_crud.create_article(db=db, article=new_article)

    return ArticlePublic(**article_in_db.__dict__)


@app.post("/article/update/{article_id}/", response_model=ArticlePublic)
def update_article(
    article_id: str,
    article_data: ArticleUpdate,
    db: Session = Depends(get_current_user),
):
    article = article_crud.get_article_by_id(db=db, id=article_id)
    if article is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    deprecated_article = article_crud.get_article_by_id(db=db, id=article_id)
    last_version = version_crud.get_latest_version_by_article_id(db=db, id=article_id)

    newest_version_number = (
        1 if last_version is None else last_version.version_number + 1
    )

    newest_version = Version(
        id=str(uuid4()),
        created_at=deprecated_article.updated_at,
        title=deprecated_article.title,
        preview=deprecated_article.preview,
        section=deprecated_article.section,
        content=deprecated_article.content,
        article_id=deprecated_article.id,
        editor_id=article_data.editor_id,
        version_number=newest_version_number,
    )
    version_in_db = version_crud.create_version(db=db, version=newest_version)

    preview = (
        article_data.content[:300] + " ..."
        if len(article_data.content) > 300
        else article_data.content
    )
    new_article_data = Article(
        id=None,
        title=article_data.title,
        section=article_data.section,
        content=article_data.content,
        created_at=None,
        updated_at=datetime.now(),
        preview=preview,
        author_id=None,
    )
    article_in_db = article_crud.update_article(
        db=db, id=article_id, new_article_data=new_article_data
    )

    return ArticlePublic(**article_in_db.__dict__)
