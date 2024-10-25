from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
from app.database import get_db
from app.schemas.article import ArticlePublic, ArticleSearch
from app.models import SectionName

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
