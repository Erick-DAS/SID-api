import bcrypt
import jwt
from jwt.exceptions import InvalidTokenError

from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Annotated
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

import app.core.config as cfg
from app.database import get_db
from app.crud.user import get_user_by_email
from app.models import User, UserRole

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 2  # 2 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


def get_password_hash(password):
    return bcrypt.hashpw(password, bcrypt.gensalt(12))


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password, hashed_password)


def check_password_format(password: str):
    validations = [
        len(password) >= 8,
        len(password) <= 20,
        any(char.isdigit() for char in password),
        any(char.isupper() for char in password),
        any(char.islower() for char in password),
    ]

    if not all(validations):
        return False

    return True


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, cfg.JWT_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, cfg.JWT_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(session, username=token_data.email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.role == UserRole.WAITING:
        raise HTTPException(status_code=400, detail="User not yet approved")
    return current_user
