from datetime import datetime
from typing import List, Annotated
from uuid import uuid4

import csv

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.crud.article as article_crud
import app.crud.version as version_crud
from app.core.auth import get_current_approved_user
from app.database import get_db
from app.schemas.data import (
    SJRPCasesSearch,
)
from app.models import Article, SectionName, Version, User

from app.logger import logger  # noqa: F401

from uuid import UUID

app = APIRouter()


sjrp_csv_path = "data/casos_sjrp.csv"


@app.get("/")
async def get_sjrp_cases(start_date: datetime | None = None, end_date: datetime | None = None):
    with open(sjrp_csv_path, newline="") as csvfile:
        spamreader = csv.reader(csvfile)

        interested_rows = []
        total_cases = 0
        current_month = None
        cases_this_month = 0
        cases_per_month = []

        for row in spamreader:

            if row[0] == "mes_ano":
                continue

            # print(", ".join(row))

            if start_date is not None:
                if start_date > datetime.strptime(row[0], "%Y%m"):
                    continue

                if end_date < datetime.strptime(row[0], "%Y%m"):
                    print(f"end_date: {end_date}")
                    print(f"csv date: {datetime.strptime(row[0], '%Y%m')}")
                    continue

            if current_month is None:
                current_month = row[0]
            
            if row[0] == current_month:
                cases_this_month = cases_this_month + int(row[1])
            else:
                cases_per_month.append((current_month, cases_this_month))
                current_month = row[0]
                cases_this_month = int(row[1])
            
            interested_rows.append(row)
            total_cases = total_cases + int(row[1])
        
        cases_per_month.append((current_month, cases_this_month))    

    return {"total_cases": total_cases, "cases_per_month": cases_per_month, "cases": interested_rows}
