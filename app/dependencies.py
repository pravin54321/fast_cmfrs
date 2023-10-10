from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Form,Query,status
from .schemas.schemas import *
from .models.models import *
from sqlalchemy.orm import Session
from .database import getdb
from pydantic import ValidationError
from fastapi.responses import JSONResponse
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
oauth_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



db: Session = Depends(getdb)

class MyCustomeException(HTTPException):
    def __init__(self, detail:str):
        super().__init__(status_code=400,detail=detail)

tags_metadata = [
    {
        "name": "singale_image",
        "description": "Operations with singale image only",
    },
     {
        "name": "Person",
        "description": "CRUD Operation with Person data",
    },
   
]        




