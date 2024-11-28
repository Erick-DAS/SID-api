from datetime import datetime
from typing import List, Dict
from pathlib import Path
import csv
import requests

from fastapi import APIRouter, HTTPException

from app.schemas.data import CensitaryValue

app = APIRouter()

BASE_CSV_DIR = Path("data/notification_count") 
sisa_web_api_url = "https://vigent.saude.sp.gov.br/sisaweb_api/dados.php"

@app.get("/sjrp_notifications", response_model=List[CensitaryValue])
async def get_sjrp_notifications(
    start_date: datetime,
    end_date: datetime
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="The start date must be before the end date."
        )

    aggregated_data: Dict[str, int] = {}

    current_date = start_date
    while current_date <= end_date:
        file_date = current_date.strftime("%Y%m")
        file_path = BASE_CSV_DIR / f"{file_date}.csv"

        if not file_path.exists():
            current_date = increment_month(current_date)
            continue

        try:
            with file_path.open("r", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    censitary_code = row.get("censitario")
                    value = int(row.get("notificacoes", 0))

                    if censitary_code in aggregated_data:
                        aggregated_data[censitary_code] += value
                    else:
                        aggregated_data[censitary_code] = value
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error processing file {file_path.name}: {str(e)}"
            )

        current_date = increment_month(current_date)

    result = [
        CensitaryValue(censitary_code=key, value=value)
        for key, value in aggregated_data.items()
    ]

    return result

@app.get("/sisa_web_properties", response_model=List[CensitaryValue])
async def get_sisa_web_data(
    start_date: datetime,
    end_date: datetime
):
    
    inicio = start_date.strftime("%Y-%m-%d")
    final = end_date.strftime("%Y-%m-%d")

    response = requests.get(url=f"{sisa_web_api_url}?tipo=4&id=471&exec=2&censitario=1&inicio={inicio}&final={final}")

    if response.status_code == 200:
        data = response.json()
    else:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching data from SISA Web API: {response.text}"
        )
    
    censitary_values = []

    for data_piece in data:
        censitary_code = data_piece["censitario"] + "P"
        censitary_values.append(
            CensitaryValue(censitary_code=censitary_code, value=data_piece["trabalhados"])
        )

    return censitary_values



def increment_month(date: datetime) -> datetime:
    year = date.year + (date.month // 12)
    month = date.month % 12 + 1
    return date.replace(year=year, month=month, day=1)
