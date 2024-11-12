from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_

from app.models import Article, SectionName, User
from app.schemas.article import ArticlePublic
from app.logger import logger  # noqa: F401


def get_articles_by_title(db: Session, title: str | None) -> ArticlePublic:
    if title is None:
        articles = db.query(Article).all()
    else:
        articles = db.query(Article).filter(Article.title.ilike(f"%{title}%")).all()

    return articles


def get_articles_by_content(
    db: Session, content: str, section: SectionName | None = None
) -> ArticlePublic:
    query = (
        db.query(Article)
        .options(joinedload(Article.user))
        .filter(or_(Article.content.ilike(f"%{content}%"), Article.title.ilike(f"%{content}%")))
    )

    if section is not None:
        query = query.filter(Article.section == section.name)

    articles = query.all()

    return [
        ArticlePublic(
            id=article.id,
            title=article.title,
            content=article.content,
            preview=article.preview,
            section=article.section,
            updated_at=article.updated_at,
            created_at=article.created_at,
            author_name=article.user.full_name if article.user else None,
        )
        for article in articles
    ]


def get_articles_by_author_name_search(
    db: Session, author: str, section: SectionName | None = None
) -> ArticlePublic:
    query = (
        db.query(Article)
        .join(User)
        .options(joinedload(Article.user))
        .filter(User.full_name.ilike(f"%{author}%"))
    )

    if section is not None:
        query = query.filter(Article.section == section.name)

    articles = query.all()

    return [
        ArticlePublic(
            id=article.id,
            title=article.title,
            content=article.content,
            preview=article.preview,
            section=article.section,
            updated_at=article.updated_at,
            created_at=article.created_at,
            author_name=article.user.full_name if article.user else None,
        )
        for article in articles
    ]


def get_articles_by_author_id(db: Session, user_id: str) -> ArticlePublic:
    query = db.query(Article).filter(Article.author_id == user_id)

    articles = query.all()

    return [
        ArticlePublic(
            id=article.id,
            title=article.title,
            content=article.content,
            preview=article.preview,
            section=article.section,
            updated_at=article.updated_at,
            created_at=article.created_at,
            author_name=article.user.full_name if article.user else None,
        )
        for article in articles
    ]


def get_articles_by_section(db: Session, section: SectionName | None) -> ArticlePublic:
    query = db.query(Article).options(joinedload(Article.user))

    if section is not None:
        query = query.filter(Article.section == section.name)

    articles = query.all()

    return [
        ArticlePublic(
            id=article.id,
            title=article.title,
            content=article.content,
            preview=article.preview,
            section=article.section,
            updated_at=article.updated_at,
            created_at=article.created_at,
            author_name=article.user.full_name if article.user else None,
        )
        for article in articles
    ]


def get_article_by_id(db: Session, id: str) -> Article:
    article = db.query(Article).filter(Article.id == id).first()
    return article


def create_article(db: Session, article: Article) -> Article:
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(db: Session, id: str, new_article_data: Article) -> Article:
    article = get_article_by_id(
        db=db, id=id
    )  # Nao sei se eh a melhor ideia as funcoes do crud dependerem umas das outras

    article.title = new_article_data.title
    article.section = new_article_data.section
    article.preview = new_article_data.preview
    article.content = new_article_data.content
    article.updated_at = new_article_data.updated_at

    db.commit()
    db.refresh(article)
    return article
