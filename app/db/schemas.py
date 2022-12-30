from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

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


class EmployeeProfile(BaseModel):
    name: str
    surname: str
    email: EmailStr
    salary: int
    company: str

    class Config:
        orm_mode = True