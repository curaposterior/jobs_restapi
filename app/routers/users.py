from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.database import get_db
import app.oauth2 as oauth2

from sqlalchemy.exc import IntegrityError


router = APIRouter()


@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    """
    Creates a user
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="try different username")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="try different data")


@router.get("/users/", response_model=list[schemas.UserOut])
async def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    Returns a list of all users (limited by limit variable)
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}/", response_model=schemas.UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """
    Returns user data
    """
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.patch("/users/{user_id}", response_model=schemas.UserOut)
async def patch_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """
    Update user profile (authentication token is required to perform this action)
    """
    query_user = db.query(models.User).filter(models.User.id == user_id)
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID={user_id} doesn't exist.")

    if db_user.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform this action.")

    query_user.update(user.dict(exclude_unset=True), synchronize_session=False)
    db.commit()
    return query_user.first()


@router.delete("/users/{user_id}/")
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """
    Deletes user (authentication token is required to perform this action)
    """
    db_user = crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    session_user = crud.get_user_by_username(db=db, username=current_user.username)

    if (db_user.id != session_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"response": "user deleted"}