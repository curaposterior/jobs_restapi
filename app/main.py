from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#routes

@app.get("/")
async def index():
    return {"information": "try different routes"}


@app.post("/users/", response_model=schemas.UserOut)
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


@app.put("/users/{user_id}/")
def change_user(user_id: int, db: Session = Depends(get_db)):
    return None


@app.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return None


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

#maybe a route @app.post('token')