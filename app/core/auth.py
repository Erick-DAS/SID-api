from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.schemas.user import UserPublic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return UserPublic(
        full_name=token + "fakedecoded"
    )

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user
