from typing import Annotated

from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List

from uuid import UUID

import app.crud.user as user_crud
from app.database import get_db
from app.models import User, UserRole
from app.schemas.user import UserPublic, UserForm, UserUpdateForm, UserADMView, UserADMViewWithPagination
from app.schemas.article import ArticlePublic
import app.crud.article as article_crud
from app.core.auth import (
    get_current_user,
    get_current_admin,
    get_password_hash,
    verify_password,
    create_access_token,
    check_password_format,
    Token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.logger import logger  # noqa: F401

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
            detail="Erro interno do servidor",
        )


@app.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        logger.debug(f"Found user email: {found_user.email}")
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
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
            detail="Erro interno do servidor",
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
            detail="E-mail ou senha incorretos",
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
            detail="O e-mail dado já está registrado.",
        )

    if not check_password_format(form.password):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="A senha precisa entre 8 e 20 caracteres, conter pelo menos uma letra maiúscula, uma letra minúscula e um número",
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
    current_admin: Annotated[str, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )
        
        if found_user.role == UserRole.ADMIN and current_admin.email != found_user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Um usuário administrador só pode ser deletado por ele mesmo",
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
            detail="Erro interno do servidor",
        )


@app.put("/{user_id}")
async def update_user(
    user_id: str,
    form: UserUpdateForm,
    current_admin: Annotated[str, Depends(get_current_admin)],
    db: Session = Depends(get_db),
):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=user_id)
        if found_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
            )
        
        if found_user.role == UserRole.ADMIN and current_admin.email != found_user.email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Um usuário administrador só pode ser editado por ele mesmo",
            )

        if form.password:
            if not check_password_format(form.password):
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="A senha precisa entre 8 e 20 caracteres, conter pelo menos uma letra maiúscula, uma letra minúscula e um número",
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
            detail="Erro interno do servidor",
        )


@app.get("", response_model=UserADMViewWithPagination)
async def get_users(
    _: Annotated[str, Depends(get_current_admin)],
    skip: int | None = None,
    limit: int | None = None,
    filter_by_role: UserRole | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
):
    
    total_users = user_crud.list_users(
        db=db, role=filter_by_role, search=search
    )

    users = user_crud.list_users(
        db=db, skip=skip, limit=limit, role=filter_by_role, search=search
    )

    return UserADMViewWithPagination(users = [UserADMView(**user.__dict__) for user in users], total=len(total_users))

@app.get("/{user_id}/articles", response_model=List[ArticlePublic])
async def get_user_articles(
    user_id: str | UUID,
    db: Session = Depends(get_db),
):
    user_by_id = user_crud.get_user_by_id(db, user_id)

    if user_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
        )

    articles = article_crud.get_articles_by_author_id(db=db, user_id=str(user_id))

    public_articles = []

    for article in articles:
        public_articles.append(ArticlePublic(**article.__dict__))

    return public_articles
