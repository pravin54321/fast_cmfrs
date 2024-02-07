import fileinput
from pydantic import BaseModel,EmailStr,Field,conint
from fastapi import Form, UploadFile,File
from datetime import date,time
from typing import Optional, Union
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
    # Pstation_id:int=None
    UserName:str
    UserEmail: EmailStr
    Mobile_Number:str=None
    User_Designation:int=None
    Posting_Distric:int=None
    Role:int=1
    disabled: Union[bool, None] = None
class hash_password(UserBase): 
    id:int   
    UserPassword: str   
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


#--------policestation_logine---------
# class PoliceLogineBase(BaseModel):
#     PoliceStation_id:int
#     User_Name:str
#     Mob_Number:str
#     Email:EmailStr|None=None
#     Designation_id:int
#     Password:str
# class PoliceLogine_01(BaseModel):
#     PoliceStation_id:int
#     User_Name:str
#     Mob_Number:str
#     Email:EmailStr|None=None
#     Designation_id:int
   
# class PoliceLoginGet(BaseModel):
#     id:int
#     policestation:PoliceStationGet
#     User_Name:str
#     Mob_Number:str
#     Email:EmailStr|None=None
#     designation:DesignationGet  
#     class config:
#         orm_mode=True

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
   user_id:Optional[int]=Form(None)
  
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
    user_id:int=None 
    
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
    user_id:int=None
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
    user_id:int=None
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

#Enquiry_Namuna_Form
class EnquiryNamunaBase(BaseModel):
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
    Is_Moter_Alive:str
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
    Which_langues_use_Crime:int
    Steal_Everyday:str
    is_Drink_Alchol:str
    Entertainment_Media:str
    Where_Sleep_Night:str
    Where_Take_Shelter:str 
    Image_Path:str=None   
    user_id:int=None 
class EnquiryNamunaBaseGet(BaseModel):
    id:int
    police_station:PoliceStation_only
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
    Is_Moter_Alive:str
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
    Image_Path:str=None  
class Yellow_CardBase(BaseModel):
    Accused_Name:str=Form(...) 
    Accused_Age:int=Form(...)
    PS_id:int=Form(...)
    Accused_Bplace:str=Form(...)
    Accused_Height:str=Form(...)
    Accused_Bcomplexion:str=Form(...)
    Accused_Btype:str=Form(...)
    Accuse_Ecolur:str=Form(...)
    Accused_Hcolur:str=Form(...)
    Occupation_id:int=Form(...)
    Accused_Imark:str=Form(...)
    Scast_id:int=Form(...)
    Accused_Education:str=Form(...)
    Pstation_Rnumber:str=Form(...)
    CRD_Number:str=Form(...)
    Accused_Address:str=Form(...)
    Accused_ImgPath:Optional[str]=Form(None)
    Caddress_Saddress:str=Form(...)
    Moment_Oinfo:str=Form(...)
    Pofficer_who_Iaccused:str=Form(...)
    Relativ_Friends:str=Form(...)
    Accused_Fdetails:str=Form(...)
    Wife_Details:str=Form(...)
    Apartner_MOBnumber:str=Form(...)
    Pcrime_Pstation:int=Form(...)
    Crime_Number:str=Form(...)
    Crime_Date:datetime
    Pcrime_Sentence:str
    Pcrime_Date:date
    user_id:Optional[int]=Form(None)
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
      
                     
            



      
   
   


    






      









