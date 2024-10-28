from pydantic import BaseModel
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional


class ArticlePublic(BaseModel):
    title: str
    preview: str
    section: str
    author_name: str
    created_at: datetime
    updated_at: datetime


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
    section: Optional[str]
    author_id: str
    content: str


class ArticleUpdate(BaseModel):
    title: Optional[str]
    section: Optional[str]
    editor_id: str
    content: Optional[str]
