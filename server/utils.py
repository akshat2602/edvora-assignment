from typing import Union
from datetime import datetime, timedelta

from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from database.crud import create_user, get_user, check_token_authenticity
from database.schemas import TokenData, UserCreate
from database.conn import SessionLocal


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600


# Exception for checking credentials
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# OAuth2 scheme for FastAPI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Password context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Get password hash
def get_password_hash(password):
    return pwd_context.hash(password)


# Check if user exists and password is correct
def authenticate_user(username: str, password: str):
    user = get_user(get_db(), username)
    if user is None:
        user = create_user(get_db(), UserCreate(username=username, hashed_password=get_password_hash(password)))
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# Create access token
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Get current user for the JWT token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        if check_token_authenticity(token):
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(get_db(), username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
