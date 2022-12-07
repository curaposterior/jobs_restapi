from fastapi import FastAPI, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine, get_db
import oauth2

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#routes

@app.get("/")
async def index():
    return {"information": "try different routes"}


@app.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserAuthenticate, db:Session = Depends(get_db)):
    user_to_auth = crud.get_user_by_username(db=db, username=user.username)
    
    if not user_to_auth:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    if not crud.verify_password(plain_password=user.password, 
                            hashed_password=user_to_auth.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"username": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"} 


@app.post("/users/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.UserOut])
def read_users(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}/", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}/", response_model=schemas.UserOut)
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


@app.delete("/users/{user_id}/")
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


@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    employees = []
    return employees


@app.post("/employees/")
def create_employee():
    return None


@app.get("/jobs/")
def list_jobs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return None


@app.post("/jobs/{job_id}/")
def get_job(job_id: int, db: Session = Depends(get_db)):
    return None


@app.get("/jobs/{job_id}/")
def show_job(job_id: int, db: Session = Depends(get_db)):
    return None