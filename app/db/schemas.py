from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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