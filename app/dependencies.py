from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Form,Query
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




