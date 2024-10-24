from pydantic import BaseModel
from enum import Enum as PyEnum


class ArticlePublic(BaseModel):
    title: str
    preview: str
    section: str
    author_name: str
    created_at: str
    updated_at: str


class ArticleSearch(PyEnum):
    AUTHOR = "author name"
    CONTENT = "content"
