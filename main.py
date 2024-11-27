import uvicorn, os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from user_manager import UserManager, User, UserInDB, TokenData, Token
from token_manager import TokenManager, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()

user_manager = UserManager()
token_manager = TokenManager()

oauth2_scheme_ = token_manager.oauth2_scheme
async def get_current_user(token: str = Depends(oauth2_scheme_)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials or Invalid token",
                                         headers={"WWW-Authenticate": "Bearer"})
    # Exception for expired JWT signature
    jwt_expired_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Signature or Token has expired",
                                          headers={"WWW-Authenticate": "Bearer"}
                                          )
    try:
        payload = token_manager.decode_access_token(token)
        # payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except jwt.ExpiredSignatureError as ex_s:
        print("ExpiredSignatureError:", ex_s)
        raise jwt_expired_exception  # Raise the custom exception
    except JWTError as ex:
        print("JWTError:", ex)
        raise credential_exception

    user = user_manager.get_user(username=token_data.username)
    if user is None:
        raise credential_exception

    return user


async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # user = authenticate_user(db, form_data.username, form_data.password)
    username = form_data.username
    password = form_data.password
    flag, status_user = user_manager.authenticate_user(username, password)
    if flag==False:
        if status_user==404:
            # Exception for User Not Found
            user_not_found_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                                    detail="User not found",
                                                    headers={"WWW-Authenticate": "Bearer"})
            raise user_not_found_exception
        if status_user==401:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    else:
        user = status_user
        
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"username": user.username}
    access_token = token_manager.create_access_token(data=payload)
    # access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user}]

@app.post("/create/")
async def create(data: User):
    return {'data': data}

@app.get("/test/{item_id}")
async def test(item_id: str, query: int = 1):
    return {"item_id": item_id,
            "query": query,
            "message": "Hello world"}


if __name__ == "__main__":
    print("App Started...!!!!!")
    ip = '127.0.0.1'
    port = 8181
    print(f"Starting server on {ip}:{port}")
    uvicorn.run(
                "__main__:app",  # Reference the app in the same file
                host = ip, 
                port = port,
                reload=True,    #reload_flag          # Enable reload for development
                limit_concurrency=3,      # Limit concurrent connections
                # workers=4                 # Set the number of worker processes
                )
    
