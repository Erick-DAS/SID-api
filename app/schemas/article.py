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

class ArticleCreate(BaseModel):
    title: str
    section: Optional[str]
    preview: str
    tags: Optional[str]
    user_id: str
    content: str

class ArticleUpdate(BaseModel):
    title: Optional[str]
    section: Optional[str]
    preview: Optional[str]
    tags: Optional[str]
    user_id: str
    content: str
