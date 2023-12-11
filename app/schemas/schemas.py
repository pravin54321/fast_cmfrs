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
#-----------master_region--------------------
class RegionBase(BaseModel):
    Region: str
    create_date: datetime = None
    update_date: datetime = None
class RegionGet(RegionBase):
    id: int
#------------master_distric-------------
class DistricBase(BaseModel):
    Distric: str
    create_date: datetime = None
    update_date: datetime = None
class DistricGet(DistricBase):
    id:int  
#----------head_office----------
class HeadOfficeBase(BaseModel):
    HeadOffice: str
    State_id:int
    Region_id:int
    Distric_id:int
    create_date:datetime = None
    update_date:datetime = None
class HeadOfficeGet(BaseModel):
    id: int
    HeadOffice:str
    create_date:datetime = None
    update_date:datetime = None
    state:StateGet
    region:RegionGet
    distric:DistricGet
    class config:
        orm_mode =True
class SubdivisionBase(BaseModel):
    Subdivision:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int
    create_date:datetime=None
    update_date:datetime=None
class SubdivisionGet(BaseModel):
    id:int
    Subdivision:str
    create_date:datetime=None
    update_date:datetime=None
    state:StateGet
    region:RegionGet
    distric:DistricGet
    headoffice:HeadOfficeGet
    class config:
        orm_mode=True
       

class PoliceStationBase(BaseModel):
    PoliceStation_Name : str
    PoliceStation_Subdivision:int
    PoliceStation_Village : int
    PoliceStation_Taluka: int
    PoliceStation_Distric:int            




