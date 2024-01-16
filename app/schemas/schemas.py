import fileinput
from pydantic import BaseModel,EmailStr,Field,conint
from fastapi import Form, UploadFile,File
from datetime import date,time
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
class StateGet(StateBase):
    id:int 
    create_date: datetime = None
    update_date: datetime = None  
#-----------master_region--------------------
class RegionBase(BaseModel):
    Region: str
    State_id:int   
class RegionGet(BaseModel):
    id: int
    Region:str
    state:StateGet
    create_date: datetime = None
    update_date: datetime = None
    class config:
        orm_mode:True
class StateRegion(BaseModel):
    id:int
    Region:str        
#------------master_distric-------------
class DistricBase(BaseModel):
    Distric: str
    State_id:int
    Region_id:int
class DistricGet(BaseModel):
    id:int
    Distric:str
    state:StateGet
    region:RegionGet
    create_date: datetime = None
    update_date: datetime = None 
    class config:
        orm_mode:True 
class RegionDistric(BaseModel):
    id:int
    Distric:str        
#----------head_office----------
class HeadOfficeBase(BaseModel):
    HeadOffice: str
    State_id:int
    Region_id:int
    Distric_id:int
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
class DistricHeadoffice(BaseModel):
    id:int
    HeadOffice:str  
#-----------subdivision----------        
class SubdivisionBase(BaseModel):
    Subdivision:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int   
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
class HodSubdivision(BaseModel):
    id:int
    Subdivision:str        
#-------taluka------------
class TalukaBase(BaseModel):
    Taluka:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int
    Subdivision_id:int     
class TalukaGet(BaseModel):
    id:int
    Taluka:str
    create_date:datetime=None
    update_date:datetime=None
    state:StateGet
    region:RegionGet
    distric:DistricGet
    headoffice:HeadOfficeGet
    subdivision:SubdivisionGet
    class config:
        orm_mode=True 
class SubdivisionTaluka(BaseModel):
    id:int
    Taluka:str              
#_____police_station_________
class PoliceStationBase(BaseModel):
    PoliceStation:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int
    Subdivision_id:int
    Taluka_id:int  
class PoliceStationGet(BaseModel):
    id:int
    PoliceStation:str
    create_date:datetime=None
    update_date:datetime=None
    state:StateGet
    region:RegionGet
    distric:DistricGet
    headoffice:HeadOfficeGet
    subdivision:SubdivisionGet
    taluka:TalukaGet
    class config:
        orm_mode=True
class PoliceStation_only(BaseModel):
    id:int
    PoliceStation:str
    create_date:datetime=None
    update_date:datetime=None
    class config:
        orm_mode=True

class TalukaPolicestation(BaseModel):
    id:int
    PoliceStation:str        
#_______post_________
class PostBase(BaseModel):
    Post:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int
    Subdivision_id:int
    Taluka_id:int
    PoliceStation_id:int    
class PostGet(BaseModel):
    id:int
    Post:str
    create_date:datetime=None
    update_date:datetime=None
    state:StateGet  
    region:RegionGet
    distric:DistricGet
    headoffice:HeadOfficeGet
    subdivision:SubdivisionGet
    taluka:TalukaGet
    policestation:PoliceStationGet  

# __________caste_shema___________________
class ReligionBase(BaseModel):
    Religion:str
   
class ReligionGet(ReligionBase):
    id:int 
    create_date:datetime=None
    update_date:datetime=None 
    class config:
        orm_model:True 

 #_________cast_shema___________        
class CastBase(BaseModel):
    Cast:str
    Religion_id:int 
class CasteGet(BaseModel):
    id:int
    Cast:str
    religion:ReligionGet
    create_date:datetime=None       
    update_date:datetime=None
    class config:
        orm_mode=True   
class ReligionCast(BaseModel):
    id:int
    Cast:str            
#________subcast_________
class SubcastBase(BaseModel):
    Subcast:str
    Religion_id:int
    Cast_id:int
class SubcastGet(BaseModel):
    id:int
    Subcast:str
    religion:ReligionGet
    cast:CasteGet
    create_date:datetime=None
    update_date:datetime=None
    class config:
        orm_mode=True
#____langues_______
class LanguesBase(BaseModel):
    Langues:str
   
class LanguesGet(BaseModel):
    id:int
    Langues:str
    create_date:datetime=None
    update_date:datetime=None

#________Occupation________
class OccupationBase(BaseModel):
    Occupation:str
class OccupationGet(OccupationBase):
    id:int
    create_date:datetime=None
    update_date:datetime=None
#-----------outherise_person--------------
class OuthPersonBase(BaseModel):
    OuthPerson:str
class OuthPersonGet(OuthPersonBase):
    id:int
    create_date:datetime=None
    update_date:datetime=None    
#-------crime_kalam---------
class CrimeKalamBase(BaseModel):
    Kalam:str
class CrimeKalamGet(BaseModel):
    id:int
    Kalam:str
    create_date:datetime=None
    update_date:datetime=None

#-------------designation_schema-----------
class DesignationBase(BaseModel):
    Designation:str
class DesignationGet(BaseModel):
    id:int
    Designation:str
    create_date:datetime=None
    update_date:datetime=None

#--------policestation_logine---------
class PoliceLogineBase(BaseModel):
    PoliceStation_id:int
    User_Name:str
    Mob_Number:str
    Email:EmailStr|None=None
    Designation_id:int
    Password:str
class PoliceLogine_01(BaseModel):
    PoliceStation_id:int
    User_Name:str
    Mob_Number:str
    Email:EmailStr|None=None
    Designation_id:int
   
class PoliceLoginGet(BaseModel):
    id:int
    policestation:PoliceStationGet
    User_Name:str
    Mob_Number:str
    Email:EmailStr|None=None
    designation:DesignationGet  
    class config:
        orm_mode=True

#-------------complaint_schema---------------
class ComplaintBase(BaseModel):
   Complainant_Name:str=Form(...)
   Mob_Number:str=Form(...)  
   Email:EmailStr|None=Form(None)
   Address:str=Form(...)
   Pin_Code:int=Form(...)
   Station_id:int=Form(...)
   Auth_Person:str=Form(...)
   Designation_id:int=Form(...)   
   Complaint_Against:str=Form(...)
   Complaint_Desc:str=Form(...)
class ComplaintBase_01(BaseModel):
   Complainant_Name:str
   Complaint_uid:str
   Mob_Number:str  
   Email:EmailStr|None=None
   Address:str
   Pin_Code:int
   Station_id:int
   Auth_Person:str
   Designation_id:int   
   Complaint_Against:str
   Complaint_Desc:str   
class ComEvidenceBase(BaseModel):
    id:int
    Complaint_id:int
    File_Path:str
    File_Type:str       

class ComplaintGet(BaseModel):
   id:int
   Complainant_Name:str
   Mob_Number:str  
   Email:EmailStr|None=None
   Address:str
   Pin_Code:int
   policestation:PoliceStation_only
   Auth_Person:str
   designation:DesignationGet   
   Complaint_Against:str
   Complaint_Desc:str
   evidence:list[ComEvidenceBase]=None 
#---------NCR_SCHEMA------------------
class NCRBase(BaseModel):
    P_Station:int
    info_recive:datetime  
    GD_No:int
    GD_Date:datetime
    Occurrence_Date:datetime
    Place_Occurrence:str
    Name_Complainant:str  
    
class CompAddressBase(BaseModel):
    Address_Type:str
    Address:str 
class CompAddressBaseGet(BaseModel):
    id:int
    Address_Type:str
    Address:str     
class AccuAddressBase(BaseModel):
    Address_Type:str
    Address:str      
class AccusedBase(BaseModel):
    Name:str
    Father_Name:str
    Age:int
    Addresses:list[AccuAddressBase]
class AccusedBaseGet(BaseModel):
    id:int
    Name:str
    Father_Name:str
    Age:int
    accus_address:list[AccuAddressBase]
   
class NCR_ACTBase(BaseModel):
    Act_id:int
    Section:str 
class NCR_ACTGet(BaseModel):
    id:int
    kalam:CrimeKalamGet    
    Section:str
   
class NCRBaseGet(BaseModel):
    id:int
    police_station:PoliceStation_only
    info_recive:datetime  
    GD_No:int
    GD_Date:datetime
    Occurrence_Date:datetime
    Place_Occurrence:str
    Name_Complainant:str
    compl_address:list[CompAddressBaseGet]=None  
    accused:list[AccusedBaseGet]=None
    act:list[NCR_ACTGet]=None  
#--------------fir_schema--------------------
class FirBase(BaseModel):
    P_Station:int
    Year: conint(ge=1900, le=2100)
    Day:str
    Time_Period:time
    Date_From:date
    Date_To:date
    Time_From:time 
    Time_To:time
    Info_Recived_Date:date
    Info_Recived_Time:time
    Diary_Entery_No:int
    Diary_Date:date
    Diary_Time:time
    Type_Information:str
    Dir_distance_From_Ps:str
    Occurrence_Address:str
    outside_ps:int
class Fir_ActBase(BaseModel):
    Fir_Act:int
    Fir_Section:str        
class Fir_ActBaseGet(BaseModel):
    id:int
    kalam:CrimeKalamGet=None
    Fir_Section:str        
class FirBaseGet(BaseModel):
    id:int
    police_station:PoliceStation_only
    Year: conint(ge=1900, le=2100)
    Day:str
    Time_Period:time
    Date_From:date
    Date_To:date
    Time_From:time 
    Time_To:time
    Info_Recived_Date:date
    Info_Recived_Time:time
    Diary_Entery_No:int
    Diary_Date:date
    Diary_Time:time
    Type_Information:str
    Dir_distance_From_Ps:str
    Occurrence_Address:str
    out_side_ps:PoliceStation_only
    fir_act:list[Fir_ActBaseGet] 
#------------chargesheet_shema-------------
class ChargeSheet_ActBase(BaseModel):
    ChargeSheet_Act:int
    ChargeSheet_Section:str 
class ChargeSheet_ActBaseGet(BaseModel):
    id:int
    kalam:CrimeKalamGet
    ChargeSheet_Section:str 
    create_date:datetime
    update_date:datetime            
class ChargeSheetBase(BaseModel):
    P_Station:int
    Year:conint(ge=1900,le=2100)
    Fir_No:str
    Fir_Date:date  
    ChargeSheet_Date:date
    Type_FinalReport:str
    If_FIR_Unoccured:str      
    If_ChargeSheet:str
    Name_IO:str
    IO_Rank:int
    Name_Complainant:str
    Father_Name:str
    Detail_Properties:str
class ChargeSheetBaseGet(BaseModel):
    id:int
    police_station:PoliceStation_only
    Year:conint(ge=1900,le=2100)
    Fir_No:str
    Fir_Date:date  
    ChargeSheet_Date:date
    Type_FinalReport:str
    If_FIR_Unoccured:str      
    If_ChargeSheet:str
    Name_IO:str
    IO_Rank:int
    Name_Complainant:str
    Father_Name:str
    Detail_Properties:str
    create_date:datetime
    update_date:datetime
    charge_sheet_act:list[ChargeSheet_ActBaseGet]
                
            



      
   
   


    






      









