from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status

from app.db import crud, models, schemas
from app.db.database import get_db
import app.oauth2 as oauth2

from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/company/", response_model=schemas.CompanyCreate)
def create_company(company: schemas.CompanyCreate, db: Session =  Depends(get_db)):
    """
    Creates a company
    """
    db_company = db.query(models.Company).filter(models.Company.company_name == company.company_name).first()

    if db_company is not None:
        raise HTTPException(status_code=403, detail=f"Company with name '{company.company_name}' is already registered")

    new = crud.create_company(db=db, company=company)
    return new


@router.get("/company/employees")
def count_employees(db: Session = Depends(get_db)):
    """
    Count employees by company
    """
    return crud.count_company_employees(db=db) #business func 1


@router.get("/company/employee/{employee_id}", response_model=schemas.EmployeeProfile)
def get_profile(employee_id: int, db: Session = Depends(get_db)):
    """
    Returns employee profile
    """
    user = crud.get_user(db=db, user_id=employee_id)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee doesn't exist")

    employee = db.query(models.Employee).filter(models.Employee.user_id == employee_id).first()
    response = {
        "name": user.name,
        "surname": user.surname,
        "email": user.email,
        "salary": employee.salary,
        "company": employee.company
    }
    return response


@router.post("/employee/skill", response_model=schemas.EmployeeSkills)
def create_employee_skill(data: schemas.EmployeeSkills, db: Session = Depends(get_db), api_key = Depends(oauth2.get_api_key)):
    """
    Add a skill to a specific employee. This can only be done using API Key.
    """
    try:
        skill = models.EmployeeSkill(
            user_id=data.user_id,
            skill_id=data.skill_id,
            skill_level=data.skill_level
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Try different data.")
    return skill


@router.get("/company/stats/avg_salary") #business func 2
def get_average_salary_by_company(db: Session = Depends(get_db)):

    q = db.query(models.Company.company_name, func.avg(models.Employee.salary).label("avg_salary")
    ).join(models.Employee, models.Employee.company == models.Company.company_name
    ).group_by(models.Company.company_name).all()

    return q