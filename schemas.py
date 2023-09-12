from pydantic import BaseModel,EmailStr
from fastapi import UploadFile
from datetime import date
#person_base
class PersonBase(BaseModel):
    id:int | None =None
    Name: str
    Mobile_Number: int
    Email:EmailStr
    Age:int
    Gender:str
    Address:str
    Status:str
    # Imagess:UploadFile = File(...)

class PersonImageBase(BaseModel):
    id:int
    person_id : int
    image:UploadFile 
    # face_encoder : bytes  
