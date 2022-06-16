from models import UserInDB

def get_user(username: str, hashed_password: str):
    # TODO: get user from database
    user = UserInDB(username=username, hashed_password=hashed_password)
    return user
