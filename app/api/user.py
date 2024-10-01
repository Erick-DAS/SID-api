from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.user import get_user_by_id
from app.schemas.user import UserPublic

app = APIRouter()

@app.get("/users/{id_user}", response_model=UserPublic)
def get_user(id_user: str, db: Session = Depends(get_db)):
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
