from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.user as user_crud
from app.database import get_db
from app.models import Article

app = APIRouter()

@app.get("/article/search/", response_model=List[Article])
def search_articles(title: str, db: Session = Depends(get_db)):
    articles = user_crud.get_articles_by_title(db=db, title=title)

    if not articles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No articles found"
        )
    
    return articles
    