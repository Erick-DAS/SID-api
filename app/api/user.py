from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.schemas import user
import app.crud.user as user_crud
from app.database import get_db

app = APIRouter()

@app.get("/users/{id_user}", response_model=user.UserBase)
def get_user(id_user: str, db: Session = Depends(get_db)):
    try:
        found_user = user_crud.get_user_by_id(db=db, id=id_user)
        if found_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return user.UserBase(**found_user.__dict__)
    except HTTPException as e:
        raise e 
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno do servidor")
