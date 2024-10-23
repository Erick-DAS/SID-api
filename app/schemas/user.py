from pydantic import BaseModel

from typing import Optional
from app.models import UserRole


class UserPublic(BaseModel):
    full_name: str
    email: str
    role: UserRole


class UserADMView(UserPublic):
    full_name: str
    email: str
    role: UserRole
    motivation: str


class UserForm(BaseModel):
    full_name: str
    email: str
    password: str
    motivation: str


class UserUpdateForm(BaseModel):
    full_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[UserRole]
