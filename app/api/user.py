from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

import app.crud.user as user_crud
from app.database import get_db
from app.models import User
from app.schemas.user import UserPublic, UserForm
from app.core.auth import get_current_user, get_password_hash, verify_password, create_access_token, check_password_format, Token, ACCESS_TOKEN_EXPIRE_MINUTES

app = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/users/{id_user}", response_model=UserPublic)
def get_user(id_user: str, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=id_user)
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
    user = user_crud.get_user_by_email(session, form_data.username)

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

@app.post("/users")
async def create_user(form: UserForm, session: Session = Depends(get_db)):
    user_by_email = user_crud.get_user_by_email(session, form.email)
    if user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The given e-mail is already registered")
    
    if not check_password_format(form.password):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Password does not meet the requirements: must be between 8 and 20 characters, contain at least one digit, one uppercase letter and one lowercase letter")
    
    hashed_password = get_password_hash(form.password)

    user = User(full_name=form.full_name, email=form.email, hashed_password=hashed_password, role="waiting for approval")

    user_in_db = user_crud.create_user(session, user)

    return UserPublic(**user_in_db.__dict__)
