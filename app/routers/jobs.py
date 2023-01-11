from fastapi import Depends, HTTPException, Security, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import crud, models, schemas
from app.db.database import get_db
import app.oauth2 as oauth2

import datetime

router = APIRouter()


@router.post("/jobs/type/create/")
def create_job_type(data: schemas.CreateJobType, db: Session = Depends(get_db), api_key = Security(oauth2.get_api_key)):
    jobType = models.JobType(
        job_type=data.job_type
    )
    db.add(jobType)
    db.commit()
    return {"response": f"created job type: {data.job_type}"}


@router.post("/jobs/", response_model=schemas.JobPostOut)
def create_job(data: schemas.CreateJob, db: Session = Depends(get_db), api_key = Security(oauth2.get_api_key)):
    """
    Function that creates job post
    """
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Try different data")

    return post


@router.get("/jobs/")
def list_jobs(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """
    List all active job posts
    :skip -> specify how many job posts you want to skip
    :limit -> specify output limit
    """
    return crud.list_jobs(db=db, skip=skip, limit=limit)


@router.get("/jobs/list/{username}/")
def list_jobs_personal(username: str, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)): #curr user add
    """
    List jobs that the specified user can take (requires authentication token)
    """
    query_user = db.query(models.User).filter(models.User.username == username)
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Couldn't find this user")

    if db_user.username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized to perform this action.")
    
    skill_level = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.user_id == db_user.id).first()
    
    jobs = db.query(models.JobPost, models.JobLocation).join(models.JobSkill).join(
        models.Company).outerjoin(models.JobLocation).filter(models.JobSkill.skill_id == skill_level.skill_id 
        and models.JobSkill.skill_level <= skill_level.skill_level 
        and models.JobPost.taken_by_id == 0 
        and models.Company.id == models.JobPost.taken_by_id).all() #business func 3
    
    return jobs


@router.post("/jobs/take/{job_id}/", response_model=schemas.JobPostOut)
def take_jobs(job_id: int, data: schemas.TakeJob, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """
    Take jobs (authentication token is required to verify the user)
    """
    query_user = db.query(models.User).filter(models.User.username == data.username)
    db_user = query_user.first()

    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Try different data.")


    job_query = db.query(models.JobPost).filter(models.JobPost.id == job_id)
    job = job_query.first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job post doesn't exist")

    if job.taken_by_id != 0 or job.is_active != True:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unable to take this job.")
    
    #gather user data
    jobSkillRequired = db.query(models.JobSkill).filter(job.id == models.JobSkill.job_post_id).first()
    userSkillLevel = db.query(models.EmployeeSkill).filter(models.EmployeeSkill.user_id == db_user.id).first() #check user skilil level
    employeeProfile = db.query(models.Employee).filter(models.Employee.user_id == db_user.id).first() #check company
    companyName = db.query(models.Company).filter(models.Company.company_name == employeeProfile.company).first()

    if (companyName.id != job.posted_by_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't work for this company.")

    if (jobSkillRequired.skill_id != userSkillLevel.skill_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have required skill to take this job.")

    if (jobSkillRequired.skill_level > userSkillLevel.skill_level):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You don't have enough experience to take this job.")
    

    job_query.update({"taken_by_id": db_user.id})
    db.commit()

    return job


@router.get("/jobs/location/{location_id}")
def get_job_location(location_id: int, db: Session = Depends(get_db)):
    """
    Check the location of a job.

    :location_id -> location id that is in the job post
    """
    location = db.query(models.JobLocation).filter(models.JobLocation.id == location_id).first()
    return location


@router.post("/jobs/create/skill/", response_model=schemas.SkillOut)
def create_skill(data: schemas.CreateSkill, db: Session = Depends(get_db), api_key: str = Security(oauth2.get_api_key)):
    """
    Create a specific skill. Only companies with their API Key can create a skill.
    """
    try:
        skill = models.Skill(
            skill_name = data.skill_name
        )
        db.add(skill)
        db.commit()
        db.refresh(skill)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Try different data.")
    return skill


@router.get("/jobs/skills/")
def list_all_skills(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Skill).offset(skip).limit(limit).all()


@router.post("/jobs/complete/", response_model=schemas.JobCompleteOut)
def finish_job(data: schemas.JobComplete, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    """
    Complete a job (authentication token is required)
    """
    try:
        userQuery = db.query(models.Employee).filter(models.Employee.user_id == current_user.id)
        jobPostQuery = db.query(models.JobPost).filter(models.JobPost.id == data.job_id)
        jobPost = jobPostQuery.first()
        if jobPost is None or jobPost.is_active == False or jobPost.taken_by_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job cannot be completed.")

    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Try different data.")


    jobPostQuery.update({"is_active": False})
    userQuery.update({"salary": models.Employee.salary + jobPost.salary})
    db.commit()

    return {"id": jobPost.id, "completed_date": datetime.datetime.now(), "is_active": jobPost.is_active}