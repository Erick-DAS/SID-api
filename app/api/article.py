from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
import app.crud.user as user_crud
import app.crud.version as version_crud
from app.database import get_db
from app.schemas.article import ArticleCreate, ArticlePublic, ArticleSearch, ArticleUpdate
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

    return articles

@app.post("/article/create/", response_model=Article)
def create_article(article: ArticleCreate, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db=db, id=article.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    new_article = Article(
        id=str(uuid4()),
        title=article.title,
        section=article.section,
        created_at=datetime.now(),
        preview=article.preview,
        tags=article.tags,
        user_id=article.user_id,
        current_version_id=None
    )
    article_in_db = article_crud.create_article(db=db, article=new_article)

    first_version = Version(
        id=str(uuid4()),
        created_at=datetime.now(),
        content=article.content,
        article_id=new_article.id,
        user_id=article.user_id
    )
    version_in_db = version_crud.create_version(db=db, version=first_version)

    article_in_db = article_crud.update_version(db=db, article=new_article, version=first_version)

    return article_in_db


@app.post("/article/update/{article_id}/", response_model=Article)
def update_article(article_id: str, article_data: ArticleUpdate, db: Session = Depends(get_db)):
    article = article_crud.get_article_by_id(db=db, id=article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Article not found"
        )

    new_version = Version(
        id=str(uuid4()),
        created_at=datetime.now(),
        content=article_data.content,
        article_id=article.id,
        user_id=article_data.user_id
    )
    version_in_db = version_crud.create_version(db=db, version=new_version)

    article_in_db = article_crud.update_version(db=db, article=article, version=new_version)

    return article_in_db
