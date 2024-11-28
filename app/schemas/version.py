from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VersionPublic(BaseModel):
    id: UUID
    title: str
    preview: str
    version_number: int
    created_at: datetime
    editor_name: str


class VersionMain(BaseModel):
    title: str
    content: str
    version_number: int
    created_at: datetime
