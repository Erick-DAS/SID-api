from pydantic import BaseModel

class CensitaryValue(BaseModel):
    censitary_code: str
    value: int
