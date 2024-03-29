import fileinput
from pydantic import BaseModel,EmailStr,Field,conint,model_validator,validator,ValidationError
from fastapi import Form, UploadFile,File
from datetime import date,time
from typing import Optional, Union
from datetime import datetime
import json
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
class PoliceStation_only(BaseModel):
    id:int
    PoliceStation:str
    create_date:datetime=None
    update_date:datetime=None
    class config:
        orm_mode=True
class DesignationGet(BaseModel):
    id:int
    Designation:str
    create_date:datetime=None
    update_date:datetime=None 
class District_only(BaseModel):
    id:int
    Distric:str
    create_date:datetime
    update_date:datetime           
        
class TokenData(BaseModel):
    username : Union[str,None] = None
class UserBase(BaseModel):
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str=None
    User_Designation:int=None
    Posting_Distric:int=None
    UserPassword: str   
    Role:int=1
    disabled: Union[bool, None] = None
class hash_password(BaseModel): 
    id:int
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:Optional[str]=None
    Designation_id:Optional[int]=None
    User_Designation:str=None
    UserPassword:str
    pstation_id:Optional[int]=None
    police_station:Union[str,None]=None
    district_id:Union[int,None]=None
    Posting_Distric:Union[str,None]=None
    Role:Optional[int]=None
    disabled: Union[bool, None] = None   
   
class UserBaseGet(BaseModel):
    id:int
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str=None
    designation:DesignationGet
    district:District_only
    Role:int=1
    disabled: Union[bool, None] = None    
class Pstation_loginBase(BaseModel):
    Pstation_id:int
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str
    User_Designation:int
    Role:int=0
    disabled: Union[bool, None] = None
    UserPassword:str
#____________________admin_creation_signup_________________
class Admin_Base(BaseModel):
    UserName:str
    UserEmail:EmailStr
    Mobile_Number:str
    Pstation_id:int
    User_Designation:int
    UserPassword:str
    Role:int=2
    disabled:Union[bool,None]=None   
class Admin_BaseGet(BaseModel):
    id:int
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str
    police_station:PoliceStation_only
    designation:DesignationGet
class Pstation_loginBaseGet(BaseModel):
    id:int
    police_station:PoliceStation_only
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str
    designation:DesignationGet
    Role:int=0
    disabled: Union[bool, None] = None
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
    # state:StateGet
    region:RegionGet
    create_date: datetime = None
    update_date: datetime = None 
    class config:
        orm_mode:True 
class RegionDistric(BaseModel):# it is use for find destrict with the help of region id
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
class TalukaPolicestation(BaseModel):
    id:int
    PoliceStation:str 
class outside_policestation(BaseModel):
    id:int
    PoliceStation:str
    create_date:datetime=None
    update_date:datetime=None
    state:StateGet
    distric:District_only
    
           
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


#---------crime_type-----------------------
class CrimeType_Base(BaseModel):
    Crime_Type:str
    Description:str 
class CrimeType_Get(CrimeType_Base):
    id:int
    create_date:datetime
    update_date:datetime  
#--------------information_mode------------
class Infomode_Base(BaseModel):
    Info_Mode:str
class infomode_BaseGet(Infomode_Base):
    id:int
    create_date:datetime=None
    update_date:datetime=None              
#-------------complaint_schema---------------
class Comp_Accused_Address_Base(BaseModel):
    Address_Type:str
    Address:str 
class Com_Accused_Addres_Get(BaseModel):
   id:int
   Address_Type:str
   Address:str 
   create_date:datetime
   update_date:datetime        
class ComAccused_Base(BaseModel):
    complaint_id:int
    Accused_Name:str
    Aliase:str
    Father_Name:str
    Mobile_Number:Optional[str]=None
    DOB:Optional[date]=None
    Accused_Age:Optional[int]=None  
    relation:str
    Remark:str
    Accused_Imgpath:Optional[str]=None
    addresses:list[Comp_Accused_Address_Base]
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value    
                     
class ComAccused_BaseGet(BaseModel):
    id:int
    complaint_id:int
    Accused_Name:str
    Aliase:str
    Father_Name:str
    Mobile_Number:Optional[str]=None
    DOB:Optional[date]=None
    Accused_Age:Optional[int]=None  
    relation:str
    Remark:str
    Accused_Imgpath:Optional[str]=None
    addresses:list[Com_Accused_Addres_Get]
    create_date:datetime=None
    update_date:datetime=None
class ComWitness_Base(BaseModel):
    complaint_id:int
    Witness_Name:str
    Witnes_age:int
    Witness_Address:str
    Relation:str
    Witness_Imgpath:Optional[str]=None
    Remark:str 
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value    
class ComWitness_BaseGet(ComWitness_Base):
    id:int
    create_date:datetime
    update_date:datetime 
class ComVictime_Base(BaseModel):
    complaint_id:int
    Victime_Name:str
    Victime_Age:int
    Victime_Address:str
    Relation:str
    Remark:str
    Victime_Imgpath:Optional[str]=None
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value    
class ComVictime_BaseGet(ComVictime_Base):
    id:int
    create_date:datetime=None
    update_date:datetime=None 
class ComEvidenceBase(BaseModel):
    id:int
    Complaint_id:int
    File_Path:str
    File_Type:str 
class ComEvidenceGet(ComEvidenceBase):
   id:int      

class ComplaintBase(BaseModel):
   state_id:int
   distric_id:int
   Station_id:int
   Complainant_Name:str
   Mob_Number:str  
   Complainant_Age:int
   Email:EmailStr                       
   Address:str
   Pin_Code:int
   Adhar_Number:str
   Auth_Person:str
   Complaint_Date:datetime
   Designation_id:int
   Occurance_date_time:datetime
   Place_Occurance:str
   Dfrom_Pstation:str
   Relation_Victim:str
   Mode_Complaint_id:int
   Crime_type_id:int
   Dutty_Officer:str
   do_designation_id:int
   Preliminary_enq_Officer:str
   pio_designation_id:int
   Investing_Officer:str
   io_designation_id:int
   Complainant_Imgpath:Optional[str]=None
   Complaint_Desc:str
   status_for_fir:Optional[str]=None
   user_id:Optional[int]=None 
   @model_validator(mode='before')
   @classmethod
   def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value      

class ComplaintGet(BaseModel):
   id:int
   policestation:outside_policestation
   Complaint_uid:str
   Complainant_Name:str
   Complainant_Age:int
   Mob_Number:str  
   Email:EmailStr|None=None
   Address:str
   Pin_Code:int
   Complaint_Date:datetime
   Adhar_Number:str
   Auth_Person:str
   designation:DesignationGet   
   Place_Occurance:str
   Occurance_date_time:datetime
   Dfrom_Pstation:str
   Relation_Victim:str
   mode_complaint:infomode_BaseGet
   crime_type:CrimeType_Get
   Dutty_Officer:str
   do_designation:DesignationGet
   Preliminary_enq_Officer:str
   pio_designation:DesignationGet
   Investing_Officer:str
   io_designation:DesignationGet
   Complainant_Imgpath:Optional[str]=None
   Complaint_Desc:str
   status_for_fir:Optional[str]=None
   evidence:list[ComEvidenceGet]=None
   victime:list[ComVictime_BaseGet]=None
   witness:list[ComWitness_BaseGet]=None
   accuse:list[ComAccused_BaseGet]=None
   create_date:datetime
   update_date:datetime  

#---------NCR_SCHEMA------------------
class NCRBase(BaseModel):
    police_station_id:int
    Complaint_id:Optional[int]=None
    info_recive:datetime
    GD_No:str=None
    GD_Date_Time:datetime=None
    Occurrence_Date_Time:datetime
    Place_Occurrence:str
    Occurance_from:time=None
    Occurance_to:time=None
    Name_Complainant:str
    Complainant_Mob_Number:str
    Complainant_Age:int
    Complainant_imgpath:str
    Complainant_Description:str
    complaint_or_Ncr:int # from complaint set 0 or diret Ncr set 1
    user_id:Optional[int]=None
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value
class CompAddressBase(BaseModel):# for ncr
    Address_Type:Optional[str]=None
    Address:str 
   
class Com_address_Schema(BaseModel):
    com_address:list[CompAddressBase]  
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value  
class CompAddressBaseGet(CompAddressBase):# for ncr
    id:int  
    NCR_id:int     
class AccuAddressBase(BaseModel):# for ncr
    Address_Type:Optional[str]=None
    Address:str  
class Accused_Address_Get(AccuAddressBase):
    id:int
    Accused_id:int
class NCR_ACTBase(BaseModel):
    Act_id:int
    Section:list[str] 
class ncr_Actupdate(BaseModel):
    accused_id:int
    Act_id:int
    Section:list[str] 
class accused_for_act(BaseModel):#ncr accused
    id:int
    NCR_id:int
    Name:str
    Aliase_Name:Optional[str]=None
    Father_Name:Optional[str]=None
    DOB:Optional[date]=None
    Age:Optional[int]=None
    Mobile_Number:Optional[str]=None
    Accused_Description:Optional[str]=None
    accus_address:list[Accused_Address_Get]    
class NCR_ACTGet(BaseModel):
    id:int
    accused:Optional[accused_for_act]=None
    kalam:CrimeKalamGet    
    Section:list[str]
    create_date:datetime
    update_date:datetime
    @validator('Section', pre=True)
    def parse_section(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # raise ValidationError("Invalid JSON string for Section field")
                return [v]  # Return the value as a list with a single element
        return v   
class AccusedBase(BaseModel):#for ncr
    NCR_id:int
    Name:str
    Aliase_Name:str=None
    Father_Name:str
    Age:int
    DOB:date=None
    Mobile_Number:str=None
    Accused_Description:str=None
    Addresses:list[AccuAddressBase]
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value  
class AccusedBaseGet(BaseModel):#ncr accused
    id:int
    NCR_id:int
    Name:str
    Aliase_Name:Optional[str]=None
    Father_Name:Optional[str]=None
    DOB:Optional[date]=None
    Age:Optional[int]=None
    Mobile_Number:Optional[str]=None
    Accused_Description:Optional[str]=None
    accus_address:list[Accused_Address_Get]
    act:list[NCR_ACTGet]
class NCRBaseGet(BaseModel):
    id:int
    NCR_uid:str
    Complaint_id:Optional[int]=None
    police_station:PoliceStation_only
    info_recive:datetime 
    GD_No:Optional[str]=None
    GD_Date_Time:Optional[datetime]=None
    Occurrence_Date_Time:datetime=None
    Place_Occurrence:str
    Occurance_from:Optional[time]=None
    Occurance_to:Optional[time]=None
    Name_Complainant:str
    Complainant_Mob_Number:str
    Complainant_Age:int
    Complainant_imgpath:str
    Complainant_Description:str
    complainant_address:list[CompAddressBaseGet]=None  
    accused:list[AccusedBaseGet]=None
    
#--------------fir_schema--------------------
class FirBase(BaseModel):
    ps_state_id:int # for police station state
    ps_district_id:int # for police station district
    P_Station:int # police station 
    Year: conint(ge=1900, le=2100) # type: ignore
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
    Beat_no:str
    Type_Information_id:int
    Dir_distance_From_Ps:str
    Occurrence_Address:str
    State_id:Optional[int]=None
    Distric_id:Optional[int]=None
    outside_ps:Optional[int]=None
    status:int # 0 for complaint and 1 for  mannually
    user_id:int=None
class Fir_Accused_Address_Base(BaseModel):
    Address_Type:str
    Address:str     
class Fir_accused_address_Get(BaseModel):
      id:int
      Address_Type:str
      Address:str 
      create_date:datetime
      update_date:datetime
class Fir_ActBase(BaseModel):
    Fir_Act:int
    Fir_Section:list[str]  
class fir_act_update(Fir_ActBase):
    accused_id:int
class fir_accused_act(BaseModel):#this shema only for fir_act   
    id:int
    fir_id:int
    Name:str
    Alias_Name:str
    Father_Name:str
    DOB:datetime
    Age:int
    Mobile_Number:str
    Accused_Description:str
    Image_Path:Optional[str]=None
    addresses:Optional[list[Fir_accused_address_Get]]=None
    create_date:datetime
    update_date:datetime           
class Fir_ActBaseGet(BaseModel):
    id:int
    kalam:CrimeKalamGet=None
    Fir_Section:Optional[list[str]]=None
    fir_accused_info:fir_accused_act
    @validator('Fir_Section',pre=True)
    def parse_section(cls,v):
        if isinstance(v,str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                #raise ValidationError('invalid JSON string for section field')
                return[v]
        return v           
class Fir_accused_Base(BaseModel):
    fir_id:int
    Name:str
    Alias_Name:str
    Father_Name:str
    DOB:datetime
    Age:int
    Mobile_Number:str
    Accused_Description:str
    Image_Path:str
    addresses:Optional[list[Fir_Accused_Address_Base]]=None
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value 
    class Config:
        orm_mode = True

class fir_accused_Get(BaseModel):
    id:int
    fir_id:int
    Name:str
    Alias_Name:str
    Father_Name:str
    DOB:datetime
    Age:int
    Mobile_Number:str
    Accused_Description:str
    Image_Path:Optional[str]=None
    addresses:Optional[list[Fir_accused_address_Get]]=None
    accused_act:Optional[list[Fir_ActBaseGet]]=None
    create_date:datetime
    update_date:datetime    

           
class FirBaseGet(BaseModel):
    id:int
    police_station:outside_policestation
    Year: Optional[conint(ge=1900, le=2100)]=None # type: ignore
    Day:Optional[str]=None
    Time_Period:Optional[time]=None
    Date_From:Optional[date]=None
    Date_To:Optional[date]=None
    Time_From:Optional[time]=None 
    Time_To:Optional[time]=None
    Info_Recived_Date:Optional[date]=None
    Info_Recived_Time:Optional[time]=None
    Diary_Entery_No:Optional[int]=None
    Diary_Date:Optional[date]=None
    Diary_Time:Optional[time]=None
    mode_information:Optional[infomode_BaseGet]=None
    Dir_distance_From_Ps:Optional[str]=None
    Occurrence_Address:Optional[str]=None
    Beat_no:Optional[str]=None
    # outside_state:Optional[StateGet]=None
    # outside_distric:Optional[DistricGet]=None
    out_side_ps:Optional[outside_policestation]=None
    fir_accused:Optional[list[fir_accused_Get]]=None
#------------chargesheet_shema-------------
class ChargeSheet_ActBase(BaseModel):
    ChargeSheet_Act:int
    ChargeSheet_Section:Optional[list[str]]=None 
class ChargeSheet_ActBaseGet(BaseModel):
    id:int
    kalam:CrimeKalamGet
    ChargeSheet_Section:list[str] 
    create_date:datetime
    update_date:datetime  
    @validator('ChargeSheet_Section',pre=True)
    def parse_section(cls,v):
        if isinstance(v,str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                #raise ValidationError('invalid JSON string for section field')
                return[v]
        return v                     
class ChargeSheetBase(BaseModel):
    State_id:int
    District_id:int
    ps_id:int
    Year:conint(ge=1900,le=2100) # type: ignore
    Fir_No:str
    Fir_Date:date  
    ChargeSheet_Date:date
    Type_Final_Report:str
    If_FIR_Unoccured:str      
    If_ChargeSheet:str
    Name_IO:str
    IO_Rank:int
    Name_Complainant:str
    Father_Name:str
    Detail_Properties:str
    user_id:int=None
class ChargeSheetBaseGet(BaseModel):
    id:int
    police_station:Optional[outside_policestation]=None
    Year:conint(ge=1900,le=2100) # type: ignore
    Fir_No:Optional[str]=None
    Fir_Date:Optional[date]=None  
    ChargeSheet_Date:Optional[date]=None
    Type_Final_Report:Optional[str]=None
    If_FIR_Unoccured:Optional[str]=None      
    If_ChargeSheet:Optional[str]=None
    Name_IO:Optional[str]=None
    IO_Rank:Optional[int]=None
    Name_Complainant:Optional[str]=None
    Father_Name:Optional[str]=None
    Detail_Properties:Optional[str]=None
    charge_sheet_act:Optional[list[ChargeSheet_ActBaseGet]]=None
    create_date:datetime
    update_date:datetime

#Enquiry_Namuna_Form
class Enquiry_Form_Base_01(BaseModel):
    state_id:int
    distric_id:int
    Police_Station_id:int
    Accused_Name:str
    Nick_Name:str
    Father_or_Wife_Name:str
    Age:int
    Mob_Number:str
    Height:str
    Body_Complexion:str
    Body_Type:str
    Eyes_Colur:str
    Hair_Colur:str
    Langues_id:int
    Identification_Mark:str
    Subcast_id:int
    Occupation_id:int
    Address:str
    Residence_Address:str
    Birth_Place:str
    Is_Father_Alive:str
    Father_Name:str
    Father_Address:str
    Father_Occupation_id:int
    Is_Father_Property:str
    Fater_Property_detail:str
    Is_Mother_Alive:str
    Mother_Details:str   
    user_id:int  
class Enquiry_Form_Get_01(BaseModel):
    id:int
    state_id:int
    distric_id:int
    Police_Station_id:int
    Accused_Name:str
    Nick_Name:str
    Father_or_Wife_Name:str
    Age:int
    Mob_Number:str
    Height:str
    Body_Complexion:str
    Body_Type:str
    Eyes_Colur:str
    Hair_Colur:str
    Langues_id:int
    Identification_Mark:str
    Subcast_id:int
    Occupation_id:int
    Address:str
    Residence_Address:str
    Birth_Place:str
    Is_Father_Alive:str
    Father_Name:str
    Father_Address:str
    Father_Occupation_id:int
    Is_Father_Property:str
    Fater_Property_detail:str
    Is_Mother_Alive:str
    Mother_Details:str 
class Enquiry_Form_Base_02(BaseModel):
    Brother_or_Sister:str
    Brother_Sister_Details:str
    Relative_or_Friends:str
    Relative_Friends_Details:str
    Is_Own_Property:str
    Own_Property_Details:str
    Is_Education:str
    Education_Details:str
    Is_Married:str
    Wife_or_Husband_Details:str
    How_long_Current_Address:str
    Who_Knows_You:str
    Know_Other_Than_Relative:str
    Proffession_Before_Coming:str
    Arrested_Before:str 
    Is_Sentence_before:str
    Sentence_Details:str
    is_CommitedCrime_Arrested_anyone:str
    Details_Anyone:str
    Stolen_Goodes_Sized_From:str
    PO_Details_Accused:str
    Stay_Other_Place:str
    PO_Emp:str
    Is_commited_Crime_Before:str
    Reason_Commited_Crime:str
    Started_Crime:str
    Gang_or_Group:str
    Crime_to_Other_Gang:str
    Where_Crime_Commited:str  
class Enquiry_Form_Get_02(BaseModel):
    id:int
    state_id:int
    distric_id:int
    Police_Station_id:int
    Accused_Name:str
    Nick_Name:str
    Father_or_Wife_Name:str
    Age:int
    Mob_Number:str
    Height:str
    Body_Complexion:str
    Body_Type:str
    Eyes_Colur:str
    Hair_Colur:str
    Langues_id:int
    Identification_Mark:str
    Subcast_id:int
    Occupation_id:int
    Address:str
    Residence_Address:str
    Birth_Place:str
    Is_Father_Alive:str
    Father_Name:str
    Father_Address:str
    Father_Occupation_id:int
    Is_Father_Property:str
    Fater_Property_detail:str
    Is_Mother_Alive:str
    Mother_Details:str 
    Brother_or_Sister:str
    Brother_Sister_Details:str
    Relative_or_Friends:str
    Relative_Friends_Details:str
    Is_Own_Property:str
    Own_Property_Details:str
    Is_Education:str
    Education_Details:str
    Is_Married:str
    Wife_or_Husband_Details:str
    How_long_Current_Address:str
    Who_Knows_You:str
    Know_Other_Than_Relative:str
    Proffession_Before_Coming:str
    Arrested_Before:str 
    Is_Sentence_before:str
    Sentence_Details:str
    is_CommitedCrime_Arrested_anyone:str
    Details_Anyone:str
    Stolen_Goodes_Sized_From:str
    PO_Details_Accused:str
    Stay_Other_Place:str
    PO_Emp:str
    Is_commited_Crime_Before:str
    Reason_Commited_Crime:str
    Started_Crime:str
    Gang_or_Group:str
    Crime_to_Other_Gang:str
    Where_Crime_Commited:str   
class Enquiry_Form_Base_03(BaseModel):
    DoYouKnow_OtherCriminal:str
    HowMuch_MonyStolen:str
    Where_Go_Before_Crime:str
    Where_Stop_Ofter_Crime:str
    Whose_sold_Stolen_Assets:str
    Robbery_Other_Distric:str
    Patner_in_Villege:str
    How_Learn_Commiting_Crime:str
    Which_Village_Gang_Activate:str
    Gang_Main_Adda:str
    Which_Town_Visited_Often:str
    Know_Robbery_Next:str
    Gang_any_Addiction:str
    Why_left_PrevGang:str
    How_Steal_NewVillage:str
    Clicked_Photes_Where:str
    When_Police_ShowUp:str
    Which_langues_use_Crime:int
    Steal_Everyday:str
    is_Drink_Alchol:str
    Entertainment_Media:str
    Where_Sleep_Night:str
    Where_Take_Shelter:str
    Image_Path:str 
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value  
class Enquiry_Form_Get_03(BaseModel):
    id:int
    # state_id:int
    # distric_id:int
    police_station:outside_policestation
    Accused_Name:str
    Nick_Name:str
    Father_or_Wife_Name:str
    Age:int
    Mob_Number:str
    Height:str
    Body_Complexion:str
    Body_Type:str
    Eyes_Colur:str
    Hair_Colur:str
    accuse_langues:LanguesGet
    Identification_Mark:str
    subcast:SubcastGet
    accused_occupation:OccupationGet
    Address:str
    Residence_Address:str
    Birth_Place:str
    Is_Father_Alive:str
    Father_Name:str
    Father_Address:str
    father_occupation:OccupationGet
    Is_Father_Property:str
    Fater_Property_detail:str
    Is_Mother_Alive:str
    Mother_Details:str 
    Brother_or_Sister:str
    Brother_Sister_Details:str
    Relative_or_Friends:str
    Relative_Friends_Details:str
    Is_Own_Property:str
    Own_Property_Details:str
    Is_Education:str
    Education_Details:str
    Is_Married:str
    Wife_or_Husband_Details:str
    How_long_Current_Address:str
    Who_Knows_You:str
    Know_Other_Than_Relative:str
    Proffession_Before_Coming:str
    Arrested_Before:str 
    Is_Sentence_before:str
    Sentence_Details:str
    is_CommitedCrime_Arrested_anyone:str
    Details_Anyone:str
    Stolen_Goodes_Sized_From:str
    PO_Details_Accused:str
    Stay_Other_Place:str
    PO_Emp:str
    Is_commited_Crime_Before:str
    Reason_Commited_Crime:str
    Started_Crime:str
    Gang_or_Group:str
    Crime_to_Other_Gang:str
    Where_Crime_Commited:str   
    DoYouKnow_OtherCriminal:str
    HowMuch_MonyStolen:str
    Where_Go_Before_Crime:str
    Where_Stop_Ofter_Crime:str
    Whose_sold_Stolen_Assets:str
    Robbery_Other_Distric:str
    Patner_in_Villege:str
    How_Learn_Commiting_Crime:str
    Which_Village_Gang_Activate:str
    Gang_Main_Adda:str
    Which_Town_Visited_Often:str
    Know_Robbery_Next:str
    Gang_any_Addiction:str
    Why_left_PrevGang:str
    How_Steal_NewVillage:str
    Clicked_Photes_Where:str
    When_Police_ShowUp:str
    crime_langues:LanguesGet
    Steal_Everyday:str
    is_Drink_Alchol:str
    Entertainment_Media:str
    Where_Sleep_Night:str
    Where_Take_Shelter:str
    Image_Path:str 
    create_date:datetime
    update_date:datetime    
#---------------yellow card----------------  
class accused_partner_schema(BaseModel):#criminal partner  they are involved in crimme
    """ from yellow_card"""
    yellow_card_id:int
    name:str
    age:int
    address:str
    MOB_Number:str
    remark:str
class friend_relative_schema(BaseModel):#accused relative_or_friend 
    """from yellow card"""
    yellow_card_id:int
    name:str
    age:int
    address:str
    relation:str
    remark:str  
class criminal_history_schema(BaseModel):# accused crime history
    """from yellow_card"""
    yellow_card_id:int
    state_id:int
    district_id:int
    police_station_id:int
    crime_number:str
    punishment:str
    act_id:int
    section:list[str]
    remark:str
class Yellow_CardBase(BaseModel):
    """yellow card schema"""
    Accused_Name:str
    Accused_Age:int
    state_id:int
    district_id:int
    PS_id:int
    Accused_Bplace:str
    Accused_Height:str
    Accused_Bcomplexion:str
    Accused_Btype:str
    Accuse_Ecolur:str
    Accused_Hcolur:str
    Occupation_id:int
    Accused_Imark:str
    Scast_id:int
    Accused_Education:str
    Pstation_Rnumber:str
    CRD_Number:str
    Accused_Address:str
    Accused_ImgPath:Optional[str]=None
    Caddress_Saddress:str=None
    Moment_Oinfo:str
    Pofficer_who_Iaccused:str
    Accused_Father_Name:str
    Accused_Father_Age:int
    Accused_Father_Address:str
    Wife_or_Husband:str
    user_id:int
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value 
class Yellow_CardBaseGet(BaseModel):
    Accused_Name:str 
    Accused_Age:int
    police_station:PoliceStation_only
    Accused_Bplace:str
    Accused_Height:str
    Accused_Bcomplexion:str
    Accused_Btype:str
    Accuse_Ecolur:str
    Accused_Hcolur:str
    occupation:OccupationGet
    Accused_Imark:str
    ycard_subcast:SubcastGet
    Accused_Education:str
    Pstation_Rnumber:str
    CRD_Number:str
    Accused_Address:str
    Accused_ImgPath:str
    Caddress_Saddress:str
    Moment_Oinfo:str
    Pofficer_who_Iaccused:str
    Relativ_Friends:str
    Accused_Fdetails:str
    Wife_Details:str
    Apartner_MOBnumber:str
    prv_pstation:PoliceStation_only
    Crime_Number:str
    Crime_Date:datetime
    Pcrime_Sentence:str
    Pcrime_Date:date
      
#-------------------information_mode_model---------------


class AnyForm(BaseModel):
    any_param: str
    any_other_param: int = 1

    @classmethod
    def as_form(
        cls,
        any_param: str = Form(...),
        any_other_param: int = Form(1)
    ):
        return cls(any_param=any_param, any_other_param=any_other_param)
class test_01(BaseModel):
    name:str
    age:int   
class Rate(BaseModel):
    id1: list[test_01]
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value    
                     
            



      
   
   


    






      









