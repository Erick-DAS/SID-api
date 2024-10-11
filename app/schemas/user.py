from pydantic import BaseModel


class UserPublic(BaseModel):
    full_name: str


class UserForm(BaseModel):
    full_name: str
    email: str
    password: str
    motivation: str
