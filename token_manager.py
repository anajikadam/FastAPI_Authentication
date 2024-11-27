from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

class TokenManager:
    def __init__(self,):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM
        self.expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token.

        Args:
            data (dict): The data to include in the token payload.
        Returns:
            str: The encoded JWT token.
        """
        expires_delta = timedelta(minutes=self.expires_delta)
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta)
        to_encode.update({"exp": expire})
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_access_token(self, token):
        SECRET_KEY = self.secret_key
        ALGORITHM = self.algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload


