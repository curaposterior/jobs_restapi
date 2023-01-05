from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from passlib.context import CryptContext

import os
import hashlib


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserIn):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name,
                          surname=user.surname,
                          address=user.address,
                          username=user.username,
                          password=hashed_password,
                          email=user.email,
                          is_active=True
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    #check if company is valid

    profile = models.Employee(user_id = db_user.id,
        salary = 0,
        currency = "PLN",
        company = user.company
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    return db_user


def generate_api_key():
    """
    Generate a random API key based on `os.urandom`

    :return: the generated API key
    :rtype: str
    """
    return hashlib.sha256(os.urandom(64)).hexdigest()


def create_company(db: Session, company: schemas.CompanyCreate):
    new_company = models.Company(company_name=company.company_name,
                                 company_description=company.company_description,
                                 establishment_date=company.establishment_date,
                                 website=company.website
                                 )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)

    apiKey = models.ApiKey(company_id = new_company.id,
                           api_key = generate_api_key())
    db.add(apiKey)
    db.commit()
    db.refresh(apiKey)

    return new_company


def count_company_employees(db: Session):
    return db.query(models.Employee.company, func.count(models.Employee.user_id)).group_by(models.Employee.company)

def list_jobs(db: Session, skip: int, limit: int):
    return db.query(models.JobPost).filter(models.JobPost.is_active == True).offset(skip).limit(limit).all()