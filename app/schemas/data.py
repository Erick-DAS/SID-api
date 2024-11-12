from pydantic import BaseModel
from enum import Enum as PyEnum
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models import SectionName


class SJRPCasesSearch(BaseModel):
    start_date: datetime | None
    end_date: datetime | None
