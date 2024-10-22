from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
from app.database import get_db
from app.schemas.article import ArticlePublic

app = APIRouter()

@app.get("/article/search/", response_model=List[ArticlePublic])
def search_articles(title: str | None = None, db: Session = Depends(get_db)):
    articles = article_crud.get_articles_by_title(db=db, title=title)
    public_articles = []

    for article in articles:
        public_articles.append(ArticlePublic(**article.__dict__))

    if not articles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No articles found"
        )
    
    return articles
    