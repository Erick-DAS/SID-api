from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

import app.crud.user as user_crud
from app.database import get_db
from app.models import User, UserRole
from app.schemas.user import UserPublic, UserForm, UserUpdateForm, UserADMView
from app.core.auth import (
    get_current_user,
    get_current_approved_user,
    get_current_admin,
    get_password_hash,
    verify_password,
    create_access_token,
    check_password_format,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.logger import logger

app = APIRouter()


@app.get("/me", response_model=UserPublic)
async def get_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        logger.debug(f"current user email: {current_user.email}")
        return current_user
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: str,
    _: Annotated[str, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        logger.debug(f"Found user email: {found_user.email}")
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return UserPublic(**found_user.__dict__)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.post("/token", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_db),
) -> Token:
    user = user_crud.get_user_by_email(session, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("Password is correct, generating token")

    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    logger.debug("Token succesfully generated")

    return Token(access_token=access_token, token_type="bearer")


@app.post("", response_model=UserPublic)
async def create_user(form: UserForm, session: Session = Depends(get_db)):
    user_by_email = user_crud.get_user_by_email(session, form.email)
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The given e-mail is already registered",
        )

    if not check_password_format(form.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password does not meet the requirements: must be between 8 and 20 characters, contain at least one digit, one uppercase letter and one lowercase letter",
        )

    hashed_password = get_password_hash(form.password)

    user = User(
        full_name=form.full_name,
        email=form.email,
        hashed_password=hashed_password,
        role=UserRole.ESPERANDO_APROVACAO,
        motivation=form.motivation,
    )

    user_in_db = user_crud.create_user(session, user)

    return UserPublic(**user_in_db.__dict__)


@app.delete("/{user_id}", response_model=UserPublic)
async def delete_user(
    user_id: str,
    _: Annotated[str, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        user_crud.delete_user(db=db, user=found_user)

        return UserPublic(**found_user.__dict__)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.put("/{user_id}")
async def update_user(
    user_id: str,
    form: UserUpdateForm,
    _: Annotated[str, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        if form.password:
            if not check_password_format(form.password):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Password does not meet the requirements: must be between 8 and 20 characters, contain at least one digit, one uppercase letter and one lowercase letter",
                )

            found_user.hashed_password = get_password_hash(form.password)

        if form.full_name:
            found_user.full_name = form.full_name

        if form.role:
            found_user.role = form.role

        db.commit()
        db.refresh(found_user)

        return UserPublic(**found_user.__dict__)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@app.get("", response_model=List[UserADMView])
async def get_users(
    _: Annotated[str, Depends(get_current_admin)],
    skip: int | None = None,
    limit: int | None = None,
    filter_by_role: UserRole | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    users = user_crud.list_users(db=db, skip=skip, limit=limit, role=filter_by_role, search=search)

    return [UserADMView(**user.__dict__) for user in users]
