from typing import Dict, Optional
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from passlib.context import CryptContext


# Sample database (in-memory)
get_db = {
    "tim": {
        "username": "tim",
        "hashed_password": "$1$kAJjfHL7$LWpRchwuZzjubuO0T3s/A0",
        "disabled": False
    }
}

get_db = {'anaji': {'username': 'anaji',
  'hashed_password': '$1$RP.n.HiP$HRmfExuEE4vZK3eiB9SjL.',
  'disabled': False},
 'sagar': {'username': 'sagar',
  'hashed_password': '$1$rsQMBcxj$9mFFzap7XZB1bmBF57eKi/',
  'disabled': False},
 'vikram': {'username': 'vikram',
  'hashed_password': '$1$H2yVfRaW$c3N4yBhc.OfnXEc8QpPer.',
  'disabled': False},
 'rahul': {'username': 'rahul',
  'hashed_password': '$1$esKtkSwy$ueGquLt1f/vxQKIyfGQZE/',
  'disabled': False}}


# Define Models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    # email: Optional[str] = None
    # full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


# UserManager Class
class UserManager:
    def __init__(self,):
        self.db = get_db
        self.pwd_context = CryptContext(schemes=["md5_crypt"])

    def get_user(self, username: str) -> Optional[UserInDB]:
        """Retrieve a user from the database by username."""
        if username in self.db:
            user_data = self.db[username]
            return UserInDB(**user_data)
        return None

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plaintext password against its hashed version."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Generate a hash for a given password."""
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str) -> Optional[UserInDB]:
        """Authenticate a user by username and password."""
        user = self.get_user(username)
        if not user:
            print("User Not Found.....")
            return False, 404
        if not self.verify_password(password, user.hashed_password):
            print("Username and password NOT verified...")
            return False, 401
        return True, user



