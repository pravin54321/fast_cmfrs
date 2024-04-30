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
    class config:
        orm_mode=True
class District_only(BaseModel):
    id:int
    Distric:str
    create_date:datetime
    update_date:datetime 
    class config:
        orm_mode=True          
        
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
    ps_state_id:Optional[int]=None
    ps_district_id:Optional[int]=None 
   
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
    create_date: datetime = None
    update_date: datetime = None
    state:StateGet   
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
    create_date: datetime = None
    update_date: datetime = None 
    # state:StateGet
    region:RegionGet
   
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
    # state:StateGet
    # region:RegionGet
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
    # state:StateGet
    # region:RegionGet
    # distric:DistricGet
    headoffice:HeadOfficeGet
   
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
    # state:StateGet
    # region:RegionGet
    # distric:DistricGet
    # headoffice:HeadOfficeGet
    subdivision:SubdivisionGet
    class config:
        orm_mode=True   
    
class SubdivisionTaluka(BaseModel):
    id:int
    Taluka:str              
#_____police_station_________
class PoliceStationBase(BaseModel):
    """
       this schema  use to create/update new policestation
    """
    PoliceStation:str
    State_id:int
    Region_id:int
    Distric_id:int
    HeadOffice_id:int
    Subdivision_id:int
    Taluka_id:int  
    class config:
        orm_mode=True   
class PoliceStationGet(BaseModel):
    """
          this schema use to get response post/put/delete 
    """
    id:int
    PoliceStation:str
    create_date:datetime=None
    update_date:datetime=None
    taluka:TalukaGet
    # state:StateGet
    # region:RegionGet
    # distric:DistricGet
    # headoffice:HeadOfficeGet
    # subdivision:SubdivisionGet
   
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
    taluka:TalukaGet
    # state:StateGet
    # distric:District_only
    class config:
        orm_mode=True   
    
           
#_______post_________
class PostBase(BaseModel):
    Post:str
    # State_id:int
    # Region_id:int
    # Distric_id:int
    # HeadOffice_id:int
    # Subdivision_id:int
    # Taluka_id:int
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
#   state_id:int    those values take from  policestation
#   distric_id:int
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
    Fir_No:str
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
class langues_from_enq_form_schema(BaseModel):#input schema
    """ Input schema representing the language ID spoken by the accused."""
    langues_id:int
class langues_from_enq_form_get(BaseModel):#output schema
    """
        Output schema representing details of the accused's spoken language from the enquiry table.
    """
    id:int
    accused_langues:LanguesGet
    create_date:datetime
    update_date:datetime  
class enq_accused_relatives_shema(BaseModel):
    """it's accused realative shema.which is link to enquiry_table""" 
    enq_form_id:int
    name:Optional[str]=None
    age:Optional[int]=None
    mobile_number:Optional[str]=None
    address:Optional[str]=None
    status:Optional[str]=None
    occupation_id:Optional[int]=None
    relation:Optional[str]=None
    remark:Optional[str]=None  
class enq_accused_relatives_get(enq_accused_relatives_shema):
    id:int
    create_date:datetime
    update_date:datetime 
class enq_accused_known_schema(BaseModel):
    """
    it's represent person data.who are identified/known to enquiry_form accused
    """
    enq_form_id:int
    name:str
    age:int
    mobile_number:str
    address:str
    relation:str
    remark:str
class enq_accused_known_get(enq_accused_known_schema):
    """
        response schema represent above schema
    """ 
    id:int
    create_date:datetime
    update_date:datetime  
class enq_form2_known_criminal_schema(BaseModel):
    name:str
    age:int
    mobile_number:str
    address:str
    remark:str   
class enq_form2_known_criminal_schema_02(enq_form2_known_criminal_schema):# this schema use for update model
    enq_form2_id:int
           
class enq_form2_known_criminal_get(enq_form2_known_criminal_schema):
    id:int
    enq_form2_id:int
    create_date:datetime
    update_date:datetime 
class enq_form_03_shema(BaseModel):
    enq_form_id:int
    did_you_rob_other_district:str
    do_you_have_partner_village:str  
    how_did_learn_commit_crime:str
    which_village_gang_activate:str
    where_is_gang_adda:str
    which_town_visited_often:str
    do_know_about_next_robbery:str
    is_there_any_addiction_in_gang:str
    why_are_you_left_prev_gang:str
    how_does_steal_in_new_village:str
    have_you_taken_photo_anywhere:str
    when_did_police_see_you:str
    which_langues_use_to_crime:int
    do_you_steal_every_day:str
    where_sleep_night:str
    where_take_shelter:str
class enq_form_03_get(enq_form_03_shema):
    id:int
    create_date:datetime
    update_date:datetime    
   
    
class enq_form_02_schema(BaseModel):
    enq_form_id:int
    occupation_before_criminal_id:int
    was_arrested_before:str# have you been arrested before
    was_sentence_before:str# have you been sentence before
    sentence_details:str#if yest then details about sentence
    from_where_stolen_goods_sized:str #from  where were stolen goods sized
    po_details_sized:str #police officer details who was sized stolen goods
    are_staying_another_place:str # are you staying in another place
    po_details:str #police officer details where you are stying in another place
    did_commite_crime_before:str #did you commite a crime before
    reason_commited_crime:str # resone for commited a crime
    when_started_crime:str # when you have started a crime
    have_gang_group:str #have you a gang or group
    have_commited_crime_another_gang:str # have ypu commited a crime with any gang
    where_commited_crime:str # which place you have commited a crime
    how_much_money_was_stolen:str #how much money was stolen
    where_did_go_before_crime:str # wher did you go before crime
    where_did_stop_ofter_crime:str# where did you stop ofter crime
    who_sold_stolen_assest:str # who sold stolen assests
class enq_form_02_get(enq_form_02_schema): 
    """schema is use to generate forme_02 response"""
    id:int
    known_criminal:list[enq_form2_known_criminal_get]
    create_date:datetime
    update_date:datetime   

class enq_form_01_address_schema(BaseModel):
    """
       adddress schema link to enq_form_01
    """
    Type:str
    address:str
class enq_form_01_address_get(enq_form_01_address_schema):
    id:int
    create_date:datetime
    update_date:datetime    
class enq_form_01_schema(BaseModel):
    """
         enq_form_01_schema basic info off accused
    """
    state_id:int
    distric_id:int
    Police_Station_id:int
    accused_name:str  
    aliase:str
    age:int
    mob_number:str
    height:str
    body_complexion:str
    body_type:str
    eyes_color:str
    hair_color:str
    identification_mark:str
    subcast_id:int
    occupation_id:int
    How_long_Current_Address:str
    birth_place:str
    education:str
    own_property_details:str
    is_drink_alcohol:str
    entertainment_media:str
    user_id:int
class enq_form_01_get(BaseModel):
    id:int
    enq_policestation:PoliceStationGet
    accused_name:str  
    aliase:str
    age:int
    mob_number:str
    height:str
    body_complexion:str
    body_type:str
    eyes_color:str
    hair_color:str
    identification_mark:str
    subcast_id:int
    occupation_id:int
    How_long_Current_Address:str
    birth_place:str
    education:str
    own_property_details:str
    is_drink_alcohol:str
    entertainment_media:str
    create_date:datetime
    update_date:datetime
    enq_accused_langues:list[langues_from_enq_form_get]
    accused_address:list[enq_form_01_address_get] 
    enq_form_02:enq_form_02_get
    # enq_form_03:enq_form_03_get     





#---------------yellow card----------------  
class accused_partner_schema(BaseModel):#criminal partner  they are involved in crimme
    """ from yellow_card"""
    yellow_card_id:int
    name:str
    age:int
    address:str
    MOB_Number:str
    remark:str
class accused_partner_get(accused_partner_schema):
    """get request data  from accused parter in yellow card"""
    id:int
    create_date:datetime
    update_date:datetime

class friend_relative_schema(BaseModel):#accused relative_or_friend 
    """
    friens and relative model shema it belong to yellow card model
    """
    yellow_card_id:int
    name:str
    age:int
    address:str
    relation:str
    remark:str  
class friend_relative_get(friend_relative_schema):
    """
    it is use to create responce to friend_relative_scheama
    """ 
    id:int
    create_date:datetime
    update_date:datetime
class criminal_history_act_schema(BaseModel):
    """act_section  is use to create act and section for the criminal_history_schema"""
    act:Optional[int]=None
    section:Optional[list[str]]=None    
class criminal_history_act_get(BaseModel):
    """it is criminal_history_act response schema"""
    act:int
    section:list[str] 
    create_date:datetime
    update_date:datetime 
    @validator('section',pre=True)
    def parse_section(cls,v):
        if isinstance(v,str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                #raise ValidationError('invalid JSON string for section field')
                return[v]
        return v             
       
class criminal_history_schema(BaseModel):# accused crime history
    """from yellow_card"""
    yellow_card_id:int
    state_id:int
    district_id:int
    police_station_id:int
    crime_number:str
    punishment:str
    remark:str
    act:Optional[list[criminal_history_act_schema]]=None
class criminal_history_get(BaseModel):
    """
    response schema for criminal_history_schema
    """ 
    id:int
    yellow_card_id:int
    state_id:int
    district_id:int
    criminal_history_police_station:Optional[PoliceStationGet]=None
    crime_number:str
    punishment:str
    remark:str
    create_date:datetime
    update_date:datetime 
    criminal_act:list[criminal_history_act_get]
    
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
    user_id:Optional[int]=None
    @model_validator(mode='before')
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value 
class Yellow_CardBaseGet(BaseModel):
    """ yellow card response schema"""
    id:int
    Accused_Name:str 
    Accused_Age:int
    ycard_police_station:Optional[outside_policestation]=None
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
    Accused_ImgPath:Optional[str]=None
    Caddress_Saddress:str#current address and permanent address
    Moment_Oinfo:str#movment information
    Pofficer_who_Iaccused:str
    Accused_Father_Name:str
    Accused_Father_Age:int
    Accused_Father_Address:str
    Wife_or_Husband:str
    create_date:datetime
    update_date:datetime
    friend_relative:Optional[list[friend_relative_get]]=None# show data from friend  reletive model
    partner:Optional[list[accused_partner_get]]=None
    criminal_history:Optional[list[criminal_history_get]]=None
  
    


  



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
                     
            



      
   
   


    






      









