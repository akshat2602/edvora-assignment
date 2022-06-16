from pydantic import BaseModel
from typing import Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    hashed_password: Union[str, None] = None


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str


class UserRequest(BaseModel):
    username: str
    password: str
