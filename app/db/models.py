from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
import datetime
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    address = Column(String)
    username = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    is_active = Column(Boolean)


class Employee(Base):
    __tablename__ = 'employee_profile'

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, index=True)
    company = Column(String, ForeignKey("company.company_name"), index=True)
    salary = Column(Integer)
    currency = Column(String)


class Skill(Base):
    __tablename__ = 'skill'

    id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String, unique=True)


class EmployeeSkill(Base):
    __tablename__ = 'employee_skills'

    user_id = Column(Integer, ForeignKey("employee_profile.user_id"), primary_key=True, index=True)
    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True, index=True)
    skill_level = Column(Integer)


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, unique=True)
    company_description = Column(String)
    establishment_date = Column(Date)
    website = Column(String)


class ApiKey(Base):
    __tablename__ = 'api_keys'

    company_id = Column(Integer, ForeignKey("company.id"), primary_key=True, index=True)
    api_key = Column(String(length=64), unique=True, index=True)


class JobLocation(Base):
    __tablename__ = 'job_location'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    city = Column(String)
    country = Column(String)
    postcode = Column(String)


class JobType(Base):
    __tablename__ = 'job_type'
    
    id = Column(Integer, primary_key=True, index=True)
    job_type = Column(String)


class JobPost(Base):
    __tablename__ = 'job_post'

    id = Column(Integer, primary_key=True, index=True)
    posted_by_id = Column(Integer, ForeignKey("company.id"), index=True)
    job_type_id = Column(Integer, ForeignKey("job_type.id"), index=True)
    job_location_id = Column(Integer, ForeignKey("job_location.id"), index=True)
    job_description = Column(String)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.utcnow)
    is_active = Column(Boolean)
    taken_by_id = Column(Integer, default=0)
    salary = Column(Integer)



class JobSkill(Base):
    __tablename__ = 'job_post_skill'

    skill_id = Column(Integer, ForeignKey("skill.id"), primary_key=True, index=True)
    job_post_id = Column(Integer, ForeignKey("job_post.id"), primary_key=True, index=True)
    skill_level = Column(Integer)


class UserAudit(Base):
    __tablename__ = 'user_audit'

    stamp = Column(DateTime, primary_key=True)
    operation = Column(String(length=1))
    userid = Column(Integer)
    username = Column(String)
    email = Column(String)