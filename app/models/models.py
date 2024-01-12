from sqlalchemy import Column,Integer,String,Text,ForeignKey,LargeBinary,Boolean,DateTime,Time,Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database import Base,engine,SessionLocal
import pytz
from sqlalchemy.sql import func
import datetime
target_metadata = Base.metadata

def get_current_time():
    from datetime import datetime
    return datetime.now(pytz.timezone('Asia/Kolkata'))

def ncr_uid():
    db=SessionLocal()
    prev_ncr=db.query(NCRModel).order_by(NCRModel.id.desc()).first()
    if prev_ncr:
        prev_ncr=prev_ncr.NCR_uid
        prev_ncr=int(prev_ncr.split("-")[-1])+1
    else:
        prev_ncr=1
    today_date=datetime.date.today().strftime('%y%m%d')
    ncr_id=f"NCR-{today_date}-{str(prev_ncr).zfill(5)}" 
    return ncr_id  
def fir_uid():
    db=SessionLocal()
    prev_fir=db.query(FIRModel).order_by(FIRModel.id.desc()).first()
    if prev_fir:
        prev_fir=prev_fir.Fir_No
        prev_fir=int(prev_fir.split("-")[-1])+1
    else:
        prev_fir=1
    today_date=datetime.date.today().strftime('%y%m%d')
    fir_no=f"FIR-{today_date}-{str(prev_fir).zfill(5)}"
    return fir_no    

class PersonModel(Base):
    __tablename__="person"
    id = Column(Integer,primary_key=True,index=True)
    Name = Column(String(255))
    Mobile_Number = Column(String(12))
    Email = Column(String(255),unique=True)
    Age = Column(Integer)
    Gender = Column(String(50))
    Address = Column(Text)
    Status = Column(String(255))
    Image = relationship('PersonImgModel',back_populates='Person',cascade="all, delete-orphan")
class PersonImgModel(Base):
    __tablename__="personimg"
    id = Column(Integer,primary_key=True,index=True)
    file_path = Column(String(255))
    face_encoding = Column(Text)
    Person_id = Column(Integer,ForeignKey('person.id'),nullable=False)
    Person = relationship('PersonModel',back_populates='Image')

class UserModel(Base):
    __tablename__='user'
    id = Column(Integer,primary_key=True,index=True)
    UserName = Column(String(50),nullable=False)
    UserEmail = Column(String(200),nullable=False, unique=True)
    UserPassword = Column(String(200))
    disabled =  Column(Boolean,default=True)
   

class GroupImageModel(Base):
    __tablename__='groupimg'
    id = Column(Integer,primary_key=True,index=True)
    ImgPath = Column(String(200),nullable=False) 
    original_img = Column(String(200),nullable=False)  

class StateModel(Base):
    __tablename__='state'
    id = Column(Integer,primary_key=True,autoincrement=True,index=True)
    State = Column(String(200),nullable=False,unique=True,)
    create_date = Column(DateTime,default=get_current_time)
    update_date = Column(DateTime,default=get_current_time,onupdate=func.now())
    region=relationship('RegionModel',back_populates='state',cascade='all,delete')
    distric=relationship('DistricModel',back_populates='state',cascade='all,delete')
    headoffices= relationship('HeadOfficeModel',back_populates='state',cascade='all,delete')
    subdivision=relationship('SubdivisionModel',back_populates='state',cascade='all,delete')
    taluka=relationship('TalukaModel',back_populates='state',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='state',cascade='all,delete')
    post=relationship('PostModel',back_populates='state',cascade='all,delete')

class RegionModel(Base):
    __tablename__='region' 
    id = Column(Integer,primary_key=True,autoincrement=True)
    Region = Column(String(200),unique=True,nullable= False)
    State_id=Column(Integer,ForeignKey('state.id'),nullable=False)
    create_date = Column(DateTime,default=get_current_time)
    update_date = Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='region')
    distric=relationship('DistricModel',back_populates='region',cascade='all,delete')
    headoffices= relationship('HeadOfficeModel',back_populates='region',cascade='all,delete') 
    subdivision=relationship('SubdivisionModel',back_populates='region',cascade='all,delete')
    taluka=relationship('TalukaModel',back_populates='region',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='region',cascade='all,delete')
    post=relationship('PostModel',back_populates='region',cascade='all,delete')  

class DistricModel(Base):
    __tablename__='distric'
    id = Column(Integer,primary_key=True,autoincrement=True)
    Distric = Column(String(200),unique=True,nullable=False)
    State_id = Column(Integer,ForeignKey('state.id'),nullable=False)
    Region_id = Column(Integer,ForeignKey('region.id'),nullable=False)
    create_date = Column(DateTime,default=get_current_time)
    update_date = Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='distric')
    region=relationship('RegionModel',back_populates='distric')
    headoffices = relationship('HeadOfficeModel',back_populates='distric',cascade='all,delete')   
    subdivision=relationship('SubdivisionModel',back_populates='distric',cascade='all,delete')
    taluka=relationship('TalukaModel',back_populates='distric',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='distric',cascade='all,delete')
    post=relationship('PostModel',back_populates='distric',cascade='all,delete')
class HeadOfficeModel(Base):
    __tablename__='headoffice'
    id = Column(Integer,primary_key=True,autoincrement=True,index=True) 
    HeadOffice=Column(String(200),unique=True,nullable=False)
    State_id = Column(Integer,ForeignKey('state.id'),nullable=False)
    Region_id = Column(Integer,ForeignKey('region.id'),nullable=False)
    Distric_id = Column(Integer,ForeignKey('distric.id'),nullable=False)
    create_date = Column(DateTime,default=get_current_time)
    update_date = Column(DateTime,default=get_current_time,onupdate=func.now())
    state = relationship('StateModel',back_populates='headoffices')
    region = relationship('RegionModel',back_populates='headoffices')
    distric = relationship('DistricModel',back_populates='headoffices')
    subdivision=relationship('SubdivisionModel',back_populates='headoffice',cascade='all,delete')
    taluka=relationship('TalukaModel',back_populates='headoffice',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='headoffice',cascade='all,delete')
    post=relationship('PostModel',back_populates='headoffice',cascade='all,delete')
class SubdivisionModel(Base):
    __tablename__='subdivision'
    id=Column(Integer,primary_key=True,autoincrement=True)
    Subdivision=Column(String(200),unique=True,nullable=False)
    State_id=Column(Integer,ForeignKey('state.id'),nullable=False)    
    Region_id=Column(Integer,ForeignKey('region.id'),nullable=False)
    Distric_id=Column(Integer,ForeignKey('distric.id'),nullable=False)
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'),nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='subdivision')
    region=relationship('RegionModel',back_populates='subdivision')
    distric=relationship('DistricModel',back_populates='subdivision')
    headoffice=relationship('HeadOfficeModel',back_populates='subdivision')
    taluka=relationship('TalukaModel',back_populates='subdivision',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='subdivision',cascade='all,delete')
    post=relationship('PostModel',back_populates='subdivision',cascade='all,delete')
class TalukaModel(Base):
    __tablename__='taluka'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Taluka=Column(String(200),unique=True,nullable=False)
    State_id=Column(Integer,ForeignKey('state.id'),nullable=False)
    Region_id=Column(Integer,ForeignKey('region.id'),nullable=False)
    Distric_id=Column(Integer,ForeignKey('distric.id'),nullable=False)
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'),nullable=False)
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id'),nullable=False) 
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='taluka')
    region=relationship('RegionModel',back_populates='taluka')  
    distric=relationship('DistricModel',back_populates='taluka') 
    headoffice=relationship('HeadOfficeModel',back_populates='taluka')
    subdivision=relationship('SubdivisionModel',back_populates='taluka')
    policestation=relationship('PoliceStationModel',back_populates='taluka',cascade='all,delete')
    post=relationship('PostModel',back_populates='taluka',cascade='all,delete')
class PoliceStationModel(Base):
    __tablename__='policestation'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    PoliceStation=Column(String(200),unique=True,nullable=False)
    State_id=Column(Integer,ForeignKey('state.id'),nullable=False)
    Region_id=Column(Integer,ForeignKey('region.id'),nullable=False)
    Distric_id=Column(Integer,ForeignKey('distric.id'),nullable=False)
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'),nullable=False)
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id'),nullable=False)
    Taluka_id=Column(Integer,ForeignKey('taluka.id'),nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='policestation')
    region=relationship('RegionModel',back_populates='policestation')
    distric=relationship('DistricModel',back_populates='policestation')
    headoffice=relationship('HeadOfficeModel',back_populates='policestation')
    subdivision=relationship('SubdivisionModel',back_populates='policestation')
    taluka=relationship('TalukaModel',back_populates='policestation')
    policestation_login=relationship('PoliceStationLogineModel',back_populates='policestation',cascade='delete,all')
    post=relationship('PostModel',back_populates='policestation',cascade='all,delete')
    complaint=relationship('ComplaintModel',back_populates='policestation',cascade="all,delete")
    ncr=relationship('NCRModel',back_populates='police_station',cascade='delete,all')
    fir=relationship('FIRModel',back_populates='police_station',foreign_keys='FIRModel.P_Station')
    fir_outside=relationship('FIRModel',back_populates='out_side_ps',foreign_keys='FIRModel.outside_ps')
   
class PostModel(Base):
    __tablename__='post'
    id=Column(Integer,primary_key=True,autoincrement=True)
    Post=Column(String(200),unique=True,nullable=False)
    State_id=Column(Integer,ForeignKey('state.id'),nullable=False)
    Region_id=Column(Integer,ForeignKey('region.id'),nullable=False)
    Distric_id=Column(Integer,ForeignKey('distric.id'),nullable=False)
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'),nullable=False)
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id'),nullable=False)
    Taluka_id=Column(Integer,ForeignKey('taluka.id'),nullable=False)
    PoliceStation_id=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    state=relationship('StateModel',back_populates='post')
    region=relationship('RegionModel',back_populates='post')
    distric=relationship('DistricModel',back_populates='post')
    headoffice=relationship('HeadOfficeModel',back_populates='post')
    subdivision=relationship('SubdivisionModel',back_populates='post')
    taluka=relationship('TalukaModel',back_populates='post')
    policestation=relationship('PoliceStationModel',back_populates='post')
   

class ReligionModel(Base):
    __tablename__='religion'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Religion=Column(String(200),unique=True,nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    cast=relationship('CastModel',back_populates='religion',cascade='all,delete') 
    subcast=relationship('SubcastModel',back_populates='religion',cascade='all,delete')

class CastModel(Base):
    __tablename__='cast'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True) 
    Cast=Column(String(200),unique=True,nullable=False)
    Religion_id=Column(Integer,ForeignKey('religion.id'),nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    religion=relationship('ReligionModel',back_populates='cast')
    subcast=relationship('SubcastModel',back_populates='cast',cascade='all,delete') 
class SubcastModel(Base):
    __tablename__='subcast'
    id=Column(Integer,primary_key=True,autoincrement=True)  
    Subcast=Column(String(200),unique=True,nullable=False)
    Religion_id=Column(Integer,ForeignKey('religion.id'),nullable=False)
    Cast_id=Column(Integer,ForeignKey('cast.id'),nullable=False) 
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    religion=relationship('ReligionModel',back_populates='subcast')
    cast=relationship('CastModel',back_populates='subcast')
#--------langues_model--------
class LanguesModel(Base):
    __tablename__='langues'         
    id=Column(Integer,autoincrement=True,primary_key=True)
    Langues=Column(String(200),unique=True,nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())  
#________Occupation_model_________
class OccupationModel(Base):
    __tablename__='Occupation'
    id=Column(Integer,autoincrement=True,index=True,primary_key=True)
    Occupation=Column(String(200),unique=True,nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
#_________outhperson_model________
class OuthPersonModel(Base):   
    __tablename__='outhperson'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)                 
    OuthPerson=Column(String(200),unique=True,nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
#___________crimekalam__________________
class CrimeKalamModel(Base):
    __tablename__='kalam'
    id=Column(Integer,primary_key=True,unique=True,index=True,autoincrement=True)
    Kalam=Column(String(200),nullable=False,unique=True)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    ncr_act=relationship('NCR_ACTModel',back_populates='kalam')

#---------designation_model------------------
class DesignationModel(Base):
    __tablename__='designation'
    id=Column(Integer,primary_key=True,index=True)
    Designation=Column(String(200),unique=True,nullable=False) 
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    policestation_login=relationship('PoliceStationLogineModel',back_populates='designation')
    complaint=relationship('ComplaintModel',back_populates='designation')      

class PoliceStationLogineModel(Base):
    __tablename__='station_login'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    PoliceStation_id=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    User_Name=Column(String(200),nullable=False)
    Designation_id=Column(Integer,ForeignKey('designation.id'),nullable=False)
    Mob_Number=Column(String(200),nullable=False)
    Email=Column(String(200),nullable=False,unique=True)
    Password=Column(String(200),nullable=False)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    policestation=relationship('PoliceStationModel',back_populates='policestation_login')
    designation=relationship('DesignationModel',back_populates='policestation_login')
   
#--------------Complaint_model------------------
class ComplaintModel(Base):
    __tablename__='complaint'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Complaint_uid=Column(String(200),nullable=False)
    Complainant_Name=Column(String(200),nullable=False)
    Mob_Number=Column(String(50),nullable=False)
    Email=Column(String(200))  
    Address=Column(Text)
    Pin_Code=Column(Integer)
    Station_id=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    Auth_Person=Column(String(200),nullable=False)
    Designation_id=Column(Integer,ForeignKey('designation.id'),nullable=False)
    Complaint_Against=Column(String(200))
    Complaint_Desc=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    evidence=relationship('ComEvidenceModel',back_populates='complaint',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='complaint')
    designation=relationship('DesignationModel',back_populates='complaint')

class ComEvidenceModel(Base):
    __tablename__='comevidence'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Complaint_id=Column(Integer,ForeignKey('complaint.id'))
    File_Path=Column(String(200))
    File_Type=Column(String(200))    
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    complaint=relationship('ComplaintModel',back_populates='evidence')
#------------Ncr_Table---------------------------------------------

class NCRModel(Base):
    __tablename__='ncr'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)  
    P_Station=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    info_recive=Column(DateTime)  
    GD_No=Column(Integer)
    GD_Date=Column(DateTime)
    Occurrence_Date=Column(DateTime)
    Place_Occurrence=Column(Text)
    Name_Complainant=Column(String(200))
    NCR_uid=Column(String(200),default=ncr_uid)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    compl_address=relationship('Complainat_AddressModel',back_populates='ncr',cascade='delete,all')
    accused=relationship('AccusedModel',back_populates='ncr',cascade='delete,all')
    act=relationship('NCR_ACTModel',back_populates='ncr',cascade='delete,all')
    police_station=relationship('PoliceStationModel',back_populates='ncr')
class Complainat_AddressModel(Base):
    __tablename__='com_address'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    NCR_id=Column(Integer,ForeignKey('ncr.id'))  
    Address_Type=Column(String(200))
    Address=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    ncr=relationship('NCRModel',back_populates='compl_address')
class AccusedModel(Base):
    __tablename__='accused'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    NCR_id=Column(Integer,ForeignKey('ncr.id'))
    Name=Column(String(200))
    Father_Name=Column(String(200))
    Age=Column(Integer)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    ncr=relationship('NCRModel',back_populates='accused')
    accus_address=relationship('Accused_AddressModel',back_populates='accused',cascade='delete,all')
class Accused_AddressModel(Base):
    __tablename__='accus_address'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)    
    Accused_id=Column(Integer,ForeignKey('accused.id')) 
    NCR_id=Column(Integer,ForeignKey('ncr.id'))
    Address_Type=Column(String(200))
    Address=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_time=Column(DateTime,default=get_current_time,onupdate=func.now())
    accused=relationship('AccusedModel',back_populates='accus_address')  
class NCR_ACTModel(Base):
    __tablename__='ncr_act'
    id=Column(Integer,primary_key=True,unique=True,index=True)  
    Act_id=Column(Integer,ForeignKey('kalam.id'))
    NCR_id=Column(Integer,ForeignKey('ncr.id'))
    Section=Column(Text)  
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    ncr=relationship(NCRModel,back_populates='act')
    kalam=relationship('CrimeKalamModel',back_populates='ncr_act')
class FIRModel(Base):
    __tablename__='fir'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    P_Station=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    Year=Column(Integer)
    Fir_No=Column(String(200),default=fir_uid)
    Day=Column(String(50))
    Time_Period=Column(Time)
    Date_From=Column(Date)
    Date_To=Column(Date)
    Time_From=Column(Time) 
    Time_To=Column(Time)
    Info_Recived_Date=Column(Date)
    Info_Recived_Time=Column(Time)
    Diary_Entery_No=Column(Integer)
    Diary_Date=Column(Date)
    Diary_Time=Column(Time)
    Type_Information=Column(String(200))
    Dir_distance_From_Ps=Column(Text)
    Occurrence_Address=Column(Text)
    outside_ps=Column(Integer,ForeignKey('policestation.id'))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    fir_act=relationship('FirSectionActModel',back_populates='fir',cascade='delete,all')
    police_station=relationship('PoliceStationModel',back_populates='fir',foreign_keys=[P_Station])
    out_side_ps=relationship('PoliceStationModel',back_populates='fir_outside',foreign_keys=[outside_ps])
class FirSectionActModel(Base):
    __tablename__='fir_act'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Fir_id=Column(Integer,ForeignKey('fir.id'))
    Fir_Act=Column(Integer,ForeignKey('kalam.id'))
    Fir_Section=Column(String(200))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    fir=relationship('FIRModel',back_populates='fir_act')






    

    



Base.metadata.create_all(bind=engine)