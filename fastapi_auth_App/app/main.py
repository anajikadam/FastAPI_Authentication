import asyncio

import time
import json
from typing import List, Optional
import shutil

import concurrent.futures
from fastapi import FastAPI, HTTPException
from fastapi import Form, Query, File, UploadFile, Response, status, Body
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

import pandas as pd
import aiofiles

from .routers import task1
from .config import logger

app = FastAPI()

# Include routers
app.include_router(task1.router)

app.mount("/static", StaticFiles(directory="fastapi_auth_App/app/static"), name="static")
# app.mount("/Output", StaticFiles(directory="Output"), name="Output")
templates = Jinja2Templates(directory="fastapi_auth_App/app/templates")

@app.get("/")
@app.get("/root")
@app.get("/api/")
def read_root(request: Request, ):
    sent = "--------/api/ In url redirect to index.html --------\n"
    print(sent)
    logger.info("Root endpoint called")  # Log info when root endpoint is accessed
    return templates.TemplateResponse("index.html", {"request": request,})

@app.get("/docMessage")
def read_root_docs():
    return {"message": "Welcome to the FastAPI app!"}





