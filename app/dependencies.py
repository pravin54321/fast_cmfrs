from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Form,Query,status,Response
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
from decouple import config


oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = config('SECREAT_KEY') 
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("TIME",cast=int)



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
        "name": "group_image",
        "description": "Operations with group image  only",
    },
     {
        "name": "Person",
        "description": "CRUD Operation with Person data",
    },
    {
        "name":"Authentication",
        "description":"login/signup"
    },
     {
        "name":"Master_state",
        "description":"crude operation with master state"
    },
     {
        "name":"Master_region",
        "description":"crude operation with master region"
    },
     {
        "name":"Master_Distric",
        "description":"crude operation with master distric"
    },
    {
        "name":"Master_HeadOffice",
        "description":"crude operation with master head_office"
    }
   
   
]        




