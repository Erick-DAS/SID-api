from pydantic import BaseModel


class ArticlePublic(BaseModel):
    title: str
    preview: str
    section: str
