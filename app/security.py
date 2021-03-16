from typing import *
from resources.user import UserModel
from werkzeug.security import safe_str_cmp

def authenticate(username: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(password.encode('utf-8'), user.password.encode('utf-8')):
        return user
    else:
        return None

def identity(payload: Dict) -> Optional[UserModel]:
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)