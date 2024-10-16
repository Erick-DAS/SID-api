from sqlalchemy.orm import Session

from app.models import Article


def get_articles_by_title(db: Session, title: str):
    articles = db.query(Article).filter(Article.title.ilike(f"%{title}%")).all()
    return articles
