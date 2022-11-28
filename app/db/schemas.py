from pydantic import BaseModel, EmailStr
from typing import Optional


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
    password_hash: str
    email: EmailStr

    class Config:
        orm_mode = True

class UserOut(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
    

class UserChange(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    address: Optional[str]
    username: Optional[str]
    password: Optional[str]
    email: Optional[EmailStr]

    class Config:
        orm_mode = True


class JobInformation(BaseModel):
    id: int
    job_description: str
    skills: str


class Job(BaseModel):
    job_id: int
    user_id: int
    completed: bool


class Employee(BaseModel):
    user_id: int
    company_id: int


class Company(BaseModel):
    id: int
    name: str
    field: str

    contractors: list[Employee] = []

    class Config:
        orm_mode = True