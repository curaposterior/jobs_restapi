from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_username(db: Session, username: int):
    return db.query(models.User).filter(models.User.username == username).first()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password_hash)
    fake_api_key="verystrongapikey" #implement method that generates api key
    db_user = models.User(name=user.name,
                          surname=user.surname,
                          address=user.address,
                          username=user.username,
                          password_hash=hashed_password,
                          api_key=fake_api_key
                          )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#to do
def get_employees(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Employee).offset(skip).limit(limit).all()
