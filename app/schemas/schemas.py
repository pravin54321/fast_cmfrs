from pydantic import BaseModel,EmailStr
from fastapi import UploadFile
from datetime import date
from typing import Union
from datetime import datetime
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
class TokenData(BaseModel):
    username : Union[str,None] = None

class UserBase(BaseModel):
    UserName:str
    UserEmail: EmailStr
    disabled: Union[bool, None] = None
class hash_password(UserBase):    
    UserPassword: str    

#-----------------group_img----------------------
class GroupImg(BaseModel):
    id:int
    ImgPath:str
    original_img:str
#------------master_policestattion--------------
class StateBase(BaseModel):
    State: str
    create_date: datetime = None
    update_date: datetime = None 
class StateGet(StateBase):
    id:int    


class PoliceStationBase(BaseModel):
    PoliceStation_Name : str
    PoliceStation_Subdivision:int
    PoliceStation_Village : int
    PoliceStation_Taluka: int
    PoliceStation_Distric:int            




