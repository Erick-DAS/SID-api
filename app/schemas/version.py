from datetime import datetime

from pydantic import BaseModel


class VersionPublic(BaseModel):
    title: str
    preview: str
    version_number: int
    created_at: datetime
