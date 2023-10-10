from pydantic import BaseModel,EmailStr
from fastapi import UploadFile
from datetime import date
from typing import Union
class ImageBase(BaseModel):
  
    Person_id : int
    file_path:str
  
class image(ImageBase):
    id:int
    class Config:
        orm_mode:True

    

#person_base
class PersonBase(BaseModel):
    Name: str
    Mobile_Number: str
    Email:EmailStr|None =None
    Age:int
    Gender:str
    Address:str
    Status:str
  
    # # Imagess:UploadFile = File(...)
class PersonImage(PersonBase):
    id:int
    Image: list[image] = []
    class Config:
        orm_mode = True

#______person_result_with__distance_______________
class PersonBase2(BaseModel):
    id:int
    Name: str
    Mobile_Number: str
    Email:EmailStr|None =None
    Age:int
    Gender:str
    Address:str
    Status:str
    class config:
        orm_mode = True
             
class imagedata(ImageBase):
    id:int
    distance :float | None = None
    Person:PersonBase2
    class config:
        orm_mode =True

#--------------------user_schema--------------------------
class UserBase(BaseModel):
    UserName:str
    UserEmail: EmailStr
class hash_password(UserBase):    
    UserPassword: str        




