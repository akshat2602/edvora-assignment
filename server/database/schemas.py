from pydantic import BaseModel
from typing import Union, List


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    hashed_password: Union[str, None] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
