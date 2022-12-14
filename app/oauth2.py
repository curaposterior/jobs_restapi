from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.db import schemas, models
from app.db.database import get_db
from app.config import settings

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import APIKeyHeader, APIKeyQuery
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.access_token_expire_minutes)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token = verify_access_token(token)

    user = db.query(models.User).filter(models.User.username == token.username).first()

    return user


def get_api_key(db: Session = Depends(get_db), api_key_query: str = Depends(api_key_query), api_key_header: str = Depends(api_key_header)):
    """
    Validate api key with a simple lookup to the database
    """
    try:
        if api_key_header == None and api_key_query == None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            )

        apiKey = db.query(models.ApiKey).filter(models.ApiKey.api_key == (api_key_query or api_key_header)).first()

        if api_key_query == apiKey.api_key:
            return api_key_query

        if api_key_header == apiKey.api_key:
            return api_key_header    

    except AttributeError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

