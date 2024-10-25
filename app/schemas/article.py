from pydantic import BaseModel
from enum import Enum as PyEnum
from datetime import datetime


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
