from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Form,Query,status,Response,Body
from fastapi.exceptions import ResponseValidationError,RequestValidationError
from .schemas.schemas import *
from .models.models import *
from sqlalchemy.orm import Session
from .database import getdb
from pydantic import ValidationError
from fastapi.responses import JSONResponse,PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError
import os
import uuid
from datetime import datetime
import json
import matplotlib.pyplot as plt
import numpy as np
# from typing import Annotated,TypeAlias
from fastapi.middleware.cors import CORSMiddleware
from deepface import DeepFace
from retinaface import RetinaFace
import cv2
import tensorflow as tf
import tensorflow_hub as hub
import aiofiles
import mediapipe
from fastapi import HTTPException
import pandas as pd
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime,timedelta
from decouple import config
from typing import Annotated,Any,List




oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = config('SECREAT_KEY') 
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("TIME",cast=int)
db: Session = Depends(getdb)

class MyCustomeException(HTTPException):
    def __init__(self, detail:str):
        super().__init__(status_code=400,detail=detail)






