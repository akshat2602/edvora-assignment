from sqlalchemy import Column, Integer, String, Boolean, DateTime

from .conn import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)



class User_Token(Base):
    __tablename__ = "usertoken"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String)
    blacklisted = Column(Boolean)
    created_at = Column(DateTime)