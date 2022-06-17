from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .conn import Base


class User(Base):
    __tablename__ = "users"

    username = Column(String, index=True, primary_key=True)
    hashed_password = Column(String)

    access_tokens = relationship("User_Token", back_populates="user")


class User_Token(Base):
    __tablename__ = "usertoken"

    token = Column(String, primary_key=True)
    blacklisted = Column(Boolean)
    created_at = Column(DateTime)
    username = Column(String, ForeignKey("users.username"))

    user = relationship("User", back_populates="access_tokens")
