from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import crud, models, schemas
from app.db.database import SessionLocal, engine, get_db
import app.oauth2 as oauth2

from sqlalchemy.exc import IntegrityError

app = FastAPI()

#routes

@app.get("/")
async def index():
    return {"response": "try different routes"}


@app.post("/users/login", response_model=schemas.Token)
async def login(user: schemas.UserAuthenticate, db:Session = Depends(get_db)):
    user_to_auth = crud.get_user_by_username(db=db, username=user.username)
    
    if not user_to_auth:
        raise HTTPException(status_code=404, detail="Invalid credentials")
    
    if not crud.verify_password(plain_password=user.password, 
                            hashed_password=user_to_auth.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"username": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"} 


# @app.post("/company/login", response_model=schemas.Token)
# async def login_company(company: schemas.CompanyAuthenticate, db: Session = Depends(get_db)):
#     company_to_auth = db.query(models.Company).filter(models.Company.company_name == company.company_name).first()

#     if not company_to_auth:
#         raise HTTPException(status_code=404, detail="Invalid credentials")
    
#     # if not crud.#


@app.post("/users/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="try different username")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="try different email")


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


@app.post("/company/", response_model=schemas.CompanyCreate)
def create_company(company: schemas.CompanyCreate, db: Session =  Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.company_name == company.company_name).first()

    if db_company is not None:
        raise HTTPException(status_code=403, detail=f"Company with name '{company.company_name}' is already registered")

    new = crud.create_company(db=db, company=company)
    return new


@app.get("/company/employees")
def count_employees(db: Session = Depends(get_db)):
    return crud.count_company_employees(db=db)


@app.get("/employee/{employee_id}", response_model=schemas.EmployeeProfile)
def get_profile(employee_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=employee_id)
    employee = db.query(models.Employee).filter(models.Employee.user_id == employee_id).first()
    response = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "salary": employee.salary,
        "company": employee.company
    }
    return response


@app.post("/jobs/", response_model=schemas.JobPostOut)
def create_job(data: schemas.CreateJob, db: Session = Depends(get_db), api_key = Security(oauth2.get_api_key)):

    currentCompany = db.query(models.Company).filter(models.Company.company_name == data.company_name).first()

    try:
        location = models.JobLocation(
            address=data.address,
            city=data.city,
            country=data.country,
            postcode=data.postcode
        )

        db.add(location)
        db.commit()
        db.refresh(location)

        post = models.JobPost(
            posted_by_id=currentCompany.id,
            job_type_id=data.job_type_id,
            job_location_id=location.id,
            job_description=data.job_description,
            is_active=True
        )
        db.add(post)
        db.commit()
        db.refresh(post)
    
        post_skill = models.JobSkill(
            skill_id=data.skill_id,
            job_post_id=post.id,
            skill_level=data.skill_level
        )
        db.add(post_skill)
        db.commit()
        db.refresh(post_skill)
    
    except IntegrityError:
        raise HTTPException(status_code=403, detail="Try different data")

    return post


@app.get("/jobs/") #list all active jobs
def list_jobs(db: Session = Depends(get_db)):
    return crud.list_jobs(db=db)


@app.get("/jobs/{username}/") #avaliable jobs based on user data, funkcja biznesowa 1
def list_taken_jobs(username: str):
    return {}


@app.post("/jobs/{job_id}") #funkcja biznesowa 2, musi sprawdzic duzo rzeczy
def take_jobs(job_id: int):
    return {}


@app.post("/jobs/skill/")
def create_skill():
    return {}


@app.post("/jobs/complete/")
def finish_job():
    return {}