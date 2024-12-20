from pydantic import BaseModel
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models import SectionName


class ArticlePublic(BaseModel):
    id: UUID
    title: str
    preview: str
    section: str
    author_name: str
    created_at: datetime
    updated_at: datetime


class ArticleSearchResponse(BaseModel):
    articles: list[ArticlePublic]
    total: int


class ArticleSearch(PyEnum):
    AUTHOR = "author name"
    CONTENT = "content"


class ArticleMain(BaseModel):
    title: str
    section: str
    content: str
    updated_at: datetime


class ArticleCreate(BaseModel):
    title: str
    section: SectionName
    content: str


class ArticleUpdate(BaseModel):
    id: UUID
    title: Optional[str]
    section: Optional[SectionName]
    content: Optional[str]
