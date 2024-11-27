import uvicorn, os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world"}

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
