from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    address = Column(String, index=True)
    username = Column(String, index=True)
    password_hash = Column(String)
    api_key = Column(String)
    test_col = Column(Integer)

#cos nie dziala z "sqlalchemy.exc.ArgumentError: Mapper mapped class Job->jobs could not assemble any primary key columns for mapped table 'jobs'"

# class Company(Base):
#     __tablename__ = 'company'

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, unique=True, index=True)
#     field = Column(String, index=True)
    
#     contractors = relationship("Employee", back_populates="companies")

# class Employee(Base):
#     __tablename__ = 'employee'

#     user_id = Column(Integer, ForeignKey("users.id"))

#     company_id = Column(Integer, ForeignKey("company.id"))
#     companies = Column("Company", back_populates="contractors")


# class JobInformation(Base):
#     __tablename__ = 'jobs_information'

#     id = Column(Integer, primary_key=True, index=True)
#     job_description = Column(String, index=True)
#     skills = Column(String, index=True)


# class Job(Base):
#     __tablename__ = 'jobs'
#     job_id = Column(Integer, ForeignKey("jobs_information.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     completed = Column(Boolean, default=False)    

