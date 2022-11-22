from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    surname: str


class UserCreate(BaseModel):
    password_hash: str
    api_key: str


class User(BaseModel):
    id: int
    address: str
    username: str

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