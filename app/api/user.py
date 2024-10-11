from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.crud.user import get_user_by_id, get_user_by_email
from app.models import User
from app.schemas.user import UserPublic
from app.core.auth import get_current_user, verify_password, create_access_token, Token, ACCESS_TOKEN_EXPIRE_MINUTES

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/{id_user}", response_model=UserPublic)
def get_user(id_user: str, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        found_user = get_user_by_id(db=db, id=id_user)
        if found_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserPublic(**found_user.__dict__)
    except HTTPException as e:
        raise e 
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@app.get("/users/me", response_model=UserPublic)
def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return current_user
    except HTTPException as e:
        raise e 
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)) -> Token:
    user = get_user_by_email(session, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=access_token, token_type="bearer")
