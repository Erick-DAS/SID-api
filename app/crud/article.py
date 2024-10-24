from sqlalchemy.orm import Session

from app.models import Article, SectionName


def get_articles_by_title(db: Session, title: str | None):
    if title is None:
        articles = db.query(Article).all()
    else:
        articles = db.query(Article).filter(Article.title.ilike(f"%{title}%")).all()

    return articles

def get_articles_by_content(db: Session, content: str, section: SectionName | None = None):
    
    query = db.query(Article).filter(Article.content.ilike(f"%{content}%"))

    if section is not None:
        query = query.filter(Article.section == section)

    articles = query.all()

    return articles

def get_articles_by_author(db: Session, author: str, section: SectionName | None = None):

    query = db.query(Article).filter(Article.user.full_name.ilike(f"%{author}%"))

    if section is not None:
        query = query.filter(Article.section == section)

    articles = query.all()

    return articles

def get_articles_by_section(db: Session, section: SectionName | None):

    query = db.query(Article)

    if section is not None:
        query = query.filter(Article.section == section)

    articles = query.all()

    return articles
