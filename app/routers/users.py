from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.database import get_db
import app.oauth2 as oauth2

from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post("/users/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="try different username")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="try different email")


@router.get("/users/", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}/", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/{user_id}/", response_model=schemas.UserOut)
async def change_user(user_id: int, user: schemas.UserChange, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    
    query_user = db.query(models.User).filter(models.User.id == user_id)
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=404, detail=f"User with ID={user_id} doesn't exist.")

    if db_user.username != current_user.username:
        raise HTTPException(status_code=403, detail="Unauthorized to perform this action.")
    
    
    query_user.update(user.dict(), synchronize_session=False)
    db.commit()

    return query_user.first()


@router.delete("/users/{user_id}/")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    session_user = crud.get_user_by_username(db=db, username=current_user.username)

    if (db_user.id != session_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to perform requested action")

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"response": "user deleted"} #change this to better response