from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TokenDataCompany(BaseModel):
    company_name: str | None = None


class UserAuthenticate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

class UserIn(BaseModel):
    name: str
    surname: str
    address: str
    username: str
    password: str
    email: EmailStr
    company: str

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    username: str
    name: str
    surname: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserChange(BaseModel):
    username: str
    name: str
    surname: str
    email: EmailStr

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    company_name: str
    company_description: str
    establishment_date: datetime.date
    website: str

    class Config:
        orm_mode = True


class CreateEmployee(BaseModel):
    user_id: int
    salary: int
    currency: str
    company: str

    class Config: #why is that necessary?
        orm_mode = True


class CreateSkill(BaseModel):
    skill_name: str

    class Config:
        orm_mode = True

class SkillOut(CreateSkill):
    id: int


class EmployeeProfile(BaseModel):
    name: str
    surname: str
    email: EmailStr
    salary: int
    company: str

    class Config:
        orm_mode = True


class EmployeeSkills(BaseModel):
    user_id: int
    skill_id: int
    skill_level: int

    class Config:
        orm_mode = True


class CreateJob(BaseModel):
    company_name: str
    job_type_id: int
    address: str
    city: str
    country: str
    postcode: str
    job_description: str
    skill_id: int
    skill_level: int
    salary: int

    class Config:
        orm_mode = True


class TakeJob(BaseModel):
    username: str

    class Config:
        orm_mode = True


class JobPostOut(BaseModel):
    id: int
    created_date: datetime.date
    is_active: bool

    class Config:
        orm_mode = True


class JobCompleteOut(BaseModel):
    id: int
    completed_date: datetime.date
    is_active: bool

    class Config:
        orm_mode = True


class JobComplete(BaseModel):
    job_id: int

    class Config:
        orm_mode = True