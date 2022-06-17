from sqlalchemy.orm import Session
import datetime

from . import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_token_authenticity(db: Session, token: str):
    db_token = db.query(models.User_Token).filter(models.User_Token.token == token, models.User_Token.blacklisted == False).first()
    if not db_token:
        return False
    return True


def add_access_token_to_db(db: Session, token: str, username: str):
    db_token = models.User_Token(token=token, blacklisted=False, created_at=datetime.datetime.now(), username=username)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def blacklist_token(db: Session, token: str):
    db_token = db.query(models.User_Token).filter(models.User_Token.token == token).first()
    db_token.blacklisted = True
    db.commit()
    return
