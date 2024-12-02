from pydantic import BaseModel

from typing import Optional
from app.models import UserRole

from uuid import UUID


class UserPublic(BaseModel):
    full_name: str
    email: str
    role: UserRole
    profile_picture: Optional[str] = None
    bio: str
    profession: str
    id: UUID


class UserADMView(UserPublic):
    full_name: str
    email: str
    role: UserRole
    motivation: str
    id: UUID


class UserADMViewWithPagination(BaseModel):
    users: list[UserADMView]
    total: int


class UserForm(BaseModel):
    full_name: str
    email: str
    password: str
    motivation: str
    bio: str
    profession: str


class UserUpdateAdminForm(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None


class UserUpdateNonAdminForm(BaseModel):
    email: Optional[str] = None
    bio: Optional[str] = None
    profession: Optional[str] = None
