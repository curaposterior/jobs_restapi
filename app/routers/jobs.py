from fastapi import Depends, HTTPException, Security, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import crud, models, schemas
from app.db.database import get_db
import app.oauth2 as oauth2

import datetime

router = APIRouter()


@router.post("/jobs/", response_model=schemas.JobPostOut)
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
            is_active=True,
            salary=data.salary
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


@router.get("/jobs/") #list all active jobs
def list_jobs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_jobs(db=db, skip=skip, limit=limit)


@router.get("/jobs/{username}/") #dodac schemat
def list_jobs_personal(username: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)): #curr user add
    query_user = db.query(models.User).filter(models.User.username == username)
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=404, detail=f"Couldn't find this user")

    if db_user.username != current_user.username:
        raise HTTPException(status_code=403, detail="Unauthorized to perform this action.")
    
    #dokleic lokalizacje
    skill_level = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.user_id == db_user.id).first() #skill
    jobs = db.query(models.JobPost).join(models.JobSkill).filter(models.JobSkill.skill_id == skill_level.skill_id and models.JobSkill.skill_level <= skill_level.skill_level and models.JobPost.taken_by_id == 0).all()
    return jobs


@router.post("/jobs/{job_id}/", response_model=schemas.JobPostOut) #funkcja biznesowa 2, musi sprawdzic duzo rzeczy
def take_jobs(job_id: int, data: schemas.TakeJob, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query_user = db.query(models.User).filter(models.User.username == data.username) #zoba czy user istnieje ni
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=404, detail=f"Try different data.")

    # if db_user.username != current_user.username:
    #     raise HTTPException(status_code=403, detail="Unauthorized to perform this action.")

    job_query = db.query(models.JobPost).filter(models.JobPost.id == job_id)
    job = job_query.first()

    if job.taken_by_id != 0 or job.is_active != True: #sprawdzenie czy jest dostepna
        raise HTTPException(status_code=403, detail="Unable to take this job.")
    
    #gather user data
    jobSkillRequired = db.query(models.JobSkill).filter(job.id == models.JobSkill.job_post_id).first()
    # jobType = db.query(models.JobType).filter(job.job_type_id == models.JobType.id).first() #check job type
    userSkillLevel = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.user_id == db_user.id).first() #check user skilil level
    # skillName = db.query(models.Skill).filter(models.Skill.id == userSkillLevel.skill_id).first() #check required skill
    employeeProfile = db.query(models.Employee).filter(models.Employee.user_id == db_user.id).first() #check company
    companyName = db.query(models.Company).filter(models.Company.company_name == employeeProfile.company).first()

    if (companyName.id != job.posted_by_id):
        raise HTTPException(status_code=403, detail="You don't work for this company.")

    if (jobSkillRequired.skill_id != userSkillLevel.skill_id):
        raise HTTPException(status_code=403, detail="You don't have required skill to take this job.")

    if (jobSkillRequired.skill_level > userSkillLevel.skill_level):
        raise HTTPException(status_code=403, detail="You don't have enough experience to take this job.")
    

    job_query.update({"taken_by_id": db_user.id})
    db.commit()

    return job


@router.post("/jobs/create/skill/", response_model=schemas.SkillOut)
def create_skill(data: schemas.CreateSkill, db: Session = Depends(get_db), api_key: str = Security(oauth2.get_api_key)):
    try:
        skill = models.Skill(
            skill_name = data.skill_name
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
    except IntegrityError:
        raise HTTPException(status_code=403, detail="Try different data.")
    return skill


@router.post("/jobs/final/complete/", response_model=schemas.JobCompleteOut)
def finish_job(data: schemas.JobComplete, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    try:
        userQuery = db.query(models.Employee).filter(models.Employee.user_id == current_user.id)
        jobPostQuery = db.query(models.JobPost).filter(models.JobPost.id == data.job_id)
        jobPost = jobPostQuery.first()
        if jobPost is None or jobPost.is_active == False or jobPost.taken_by_id != current_user.id:
            raise HTTPException(status_code=404, detail=f"Job cannot be completed.")

    except IntegrityError:
        raise HTTPException(status_code=403, detail="Try different data.")


    jobPostQuery.update({"is_active": False})
    userQuery.update({"salary": models.Employee.salary + jobPost.salary})
    db.commit()

    return {"id": jobPost.id, "completed_date": datetime.datetime.now(), "is_active": jobPost.is_active}