from pydantic import BaseModel

class UserPublic(BaseModel):
    full_name: str
