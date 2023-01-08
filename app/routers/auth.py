from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from app.db import crud, schemas
from app.db.database import get_db
import app.oauth2 as oauth2


router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserAuthenticate, db: Session = Depends(get_db)):
    """
    Returns JWT token after a successful validation of user credentials
    """
    user_to_auth = crud.get_user_by_username(db=db, username=user.username)
    
    if not user_to_auth:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    if not crud.verify_password(plain_password=user.password, 
                            hashed_password=user_to_auth.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"username": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"} 