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
def complaint_uid():
    import datetime
    db=SessionLocal()
    prev_complaint=db.query(ComplaintModel).order_by(ComplaintModel.id.desc()).first()
    if prev_complaint:
        prev_complaint=prev_complaint.Complaint_uid
        prev_complaint=int(prev_complaint.split("-")[-1]) + 1
    else:
        prev_complaint=1    
    today_date=datetime.date.today().strftime('%Y%m%d')
    complaint_id = f"COM-{today_date}-{str(prev_complaint).zfill(5)}"
    return complaint_id

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
#--------------charge_sheet_number------------------------
def chargesheet_uid():
    db=SessionLocal()
    prev_chargesheet=db.query(ChargeSheetModel).order_by(ChargeSheetModel.id.desc()).first()
    if prev_chargesheet:
        prev_chargesheet=prev_chargesheet.ChargeSheet_No
        prev_chargesheet=int(prev_chargesheet.split("-")[-1])+1
    else:
        prev_chargesheet=1
    today_date=datetime.date.today().strftime('%y%m%d') 
    chargesheet_no=f"CS-{today_date}-{str(prev_chargesheet).zfill(5)}"
    return chargesheet_no       

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
    Pstation_id=Column(Integer,ForeignKey('policestation.id'))
    UserName = Column(String(50),nullable=False)
    UserEmail = Column(String(200),nullable=False, unique=True)
    Mobile_Number=Column(String(100))
    User_Designation=Column(Integer,ForeignKey('designation.id'))
    Posting_Distric=Column(Integer,ForeignKey('distric.id'))
    UserPassword = Column(String(200))
    Role=Column(Integer,comment='0 for policestation,1 for sp and 2 for admin') 
    disabled =  Column(Boolean,default=True)
    police_station=relationship('PoliceStationModel',backref='Pstation_id')
    designation=relationship('DesignationModel',backref='User_Designation')
    district=relationship('DistricModel',backref='Posting_Distric')
   

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
    region=relationship('RegionModel',back_populates='state')
    distric=relationship('DistricModel',back_populates='state',cascade='all,delete')
    headoffices= relationship('HeadOfficeModel',back_populates='state',cascade='all,delete')
    subdivision=relationship('SubdivisionModel',back_populates='state',cascade='all,delete')
    taluka=relationship('TalukaModel',back_populates='state',cascade='all,delete')
    policestation=relationship('PoliceStationModel',back_populates='state',cascade='all,delete')
    post=relationship('PostModel',back_populates='state',cascade='all,delete')

class RegionModel(Base):
    __tablename__='region' 
    id = Column(Integer,primary_key=True,autoincrement=True)
    Region = Column(String(200),nullable= False)
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
    # fir=relationship('FIRModel',back_populates='police_station',foreign_keys='FIRModel.P_Station')
    # fir_outside=relationship('FIRModel',back_populates='out_side_ps',foreign_keys='FIRModel.outside_ps')
    charge_sheet=relationship('ChargeSheetModel',back_populates='police_station')
   
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
    charge_sheet_act=relationship('ChargeSheet_ActModel',back_populates='kalam')
#---------designation_model------------------
class DesignationModel(Base):
    __tablename__='designation'
    id=Column(Integer,primary_key=True,index=True)
    Designation=Column(String(200),unique=True,nullable=False) 
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    policestation_login=relationship('PoliceStationLogineModel',back_populates='designation')
    complaint=relationship('ComplaintModel',back_populates='designation')   
class Infomode_Model(Base):
    __tablename__='infomode'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    Info_Mode=Column(String(256))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())  
class CrimeMethod_Model(Base):
    __tablename__="crime_method"
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Crime_Type=Column(String(256))
    Description=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())         

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
    Complaint_uid=Column(String(200),default=complaint_uid)
    Complainant_Name=Column(String(200),nullable=False)
    Mob_Number=Column(String(50),nullable=False)
    Complainant_Age=Column(Integer)
    Email=Column(String(200))  
    Address=Column(Text)
    Pin_Code=Column(Integer)
    Adhar_Number=Column(String(12))
    Complaint_Date=Column(DateTime)
    Occurance_date_time=Column(DateTime)
    Place_Occurance=Column(Text)
    Dfrom_Pstation=Column(String(256),comment="distance from police station")
    Relation_Victim=Column(String(256),comment='relation with complainant and victime')
    Station_id=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    Auth_Person=Column(String(200),nullable=False)
    Designation_id=Column(Integer,ForeignKey('designation.id'),nullable=False)
    Mode_Complaint_id=Column(Integer,ForeignKey('infomode.id'),comment="foreigne key of complaint mode")
    Crime_type_id=Column(Integer,ForeignKey("crime_method.id"))
    Dutty_Officer=Column(String(256))
    Preliminary_enq_Officer=Column(String(256))
    Investing_Officer=Column(String(256))
    Complainant_Imgpath=Column(String(256))
    Complaint_Desc=Column(Text)
    user_id=Column(Integer,comment='current user id save')
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    evidence=relationship('ComEvidenceModel',backref='evidence',cascade='all,delete-orphan')
    victime=relationship('ComVictime_Model',backref='victime',cascade='all,delete-orphan')
    witness=relationship('ComWitness_Model',backref='witness',cascade='all,delete-orphan')
    accuse=relationship('ComAccused_Model',backref='accuse',cascade='all,delete-orphan')
    policestation=relationship('PoliceStationModel',back_populates='complaint')
    designation=relationship('DesignationModel',back_populates='complaint')
    mode_complaint=relationship('Infomode_Model',backref='mode_complaint')
    crime_type=relationship('CrimeMethod_Model',backref='crime_type')

class ComVictime_Model(Base):#complaint victime model
    __tablename__='complaint_victime'
    id =Column(Integer,primary_key=True,unique=True,autoincrement=True,index=True)
    complaint_id=Column(Integer,ForeignKey('complaint.id'))
    Victime_Name=Column(String(256))
    Victime_Age=Column(Integer)
    Victime_Address=Column(Text)
    Relation=Column(String(256),comment='relation with complainant and victime')
    Remark=Column(Text)
    Victime_Imgpath=Column(String(256))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
class ComWitness_Model(Base):#complaint witness
    __tablename__='complaint_witness'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True,unique=True)
    complaint_id=Column(Integer,ForeignKey('complaint.id'))
    Witness_Name=Column(String(256))
    Witnes_age=Column(Integer)
    Witness_Address=Column(Text)
    Relation=Column(String(256),comment='relation with victime')
    Witness_Imgpath=Column(String(256))
    Remark=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now)
class ComAccused_Model(Base):#complaint accused
    __tablename__='complaint_accused'
    id=Column(Integer,primary_key=True,unique=True,autoincrement=True)
    complaint_id=Column(Integer,ForeignKey('complaint.id'))
    Accused_Name=Column(String(256))
    Aliase=Column(String(256),comment='aliase name')
    Father_Name=Column(String(256))
    Mobile_Number=Column(String(12))
    DOB=Column(Date)
    Accused_Age=Column(Integer)  
    relation=Column(String(256),comment='relation with victime')
    Remark=Column(Text)
    Accused_Imgpath=Column(String(256))#accused image path
    addresses=relationship("Com_Accused_Address_Model",backref="addresses",cascade='all,delete-orphan')
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
class Com_Accused_Address_Model(Base):
    __tablename__="com_accused_address"
    id=Column(Integer,primary_key=True,unique=True,index=True,nullable=True)
    accused_id=Column(Integer,ForeignKey("complaint_accused.id"))
    Address_Type=Column(String(255))
    Address=Column(Text)  
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())  
class ComEvidenceModel(Base):
    __tablename__='comevidence'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Complaint_id=Column(Integer,ForeignKey('complaint.id'))
    File_Path=Column(String(200))
    File_Type=Column(String(200))    
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
   

#------------Ncr_Table---------------------------------------------
class NCRModel(Base):
    __tablename__='ncr_model'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)  
    police_station_id=Column(Integer,ForeignKey('policestation.id'),nullable=False)
    Complaint_id=Column(Integer,ForeignKey('complaint.id'),nullable=True)
    info_recive=Column(DateTime,comment='info recive date and time')  
    GD_No=Column(String(200))
    GD_Date_Time=Column(DateTime)
    Occurrence_Date_Time=Column(DateTime)
    Place_Occurrence=Column(Text)
    Occurance_from=Column(Time,comment='occurance time range')
    Occurance_to=Column(Time,comment='occurance time range from to')
    Name_Complainant=Column(String(200))
    Complainant_Mob_Number=Column(String(12))
    Complainant_Age=Column(Integer)
    NCR_uid=Column(String(200),default=ncr_uid)
    Complainant_imgpath=Column(String(200))
    Complainant_Description=Column(Text)
    complaint_or_Ncr=Column(Integer,comment='from complaint-0 & dir_ncr-1')
    user_id=Column(Integer,comment='user id logine')
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    complainant_address=relationship('Complainat_AddressModel',backref='complainant_address')   
    accused=relationship('AccusedModel',backref='accused',cascade='all,delete-orphan') 
    police_station=relationship('PoliceStationModel',back_populates='ncr')
class Complainat_AddressModel(Base):#ncr_model
    __tablename__='ncr_com_address'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    NCR_id=Column(Integer,ForeignKey('ncr_model.id'))  
    Address_Type=Column(String(200))
    Address=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    # ncr=relationship('NCRModel',back_populates='compl_address')
class AccusedModel(Base):# for ncr  accused model
    __tablename__='ncr_accused'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    NCR_id=Column(Integer,ForeignKey('ncr_model.id'))
    Name=Column(String(200))
    Aliase_Name=Column(String(200))
    Father_Name=Column(String(200))
    DOB=Column(Date)
    Age=Column(Integer)
    Mobile_Number=Column(String(12))
    Accused_Description=Column(Text)
    image_path=Column(String(256))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    accus_address=relationship('Accused_AddressModel',backref="accuse_address",cascade='all,delete-orphan')
    act=relationship('NCR_ACTModel',back_populates='accused',cascade='all,delete-orphan')
class Accused_AddressModel(Base):# for NCR Accused address model
    __tablename__='ncr_accused_address'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)    
    Accused_id=Column(Integer,ForeignKey('ncr_accused.id')) 
    Address_Type=Column(String(200))
    Address=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_time=Column(DateTime,default=get_current_time,onupdate=func.now())
    # accused=relationship('AccusedModel',back_populates='accus_address')  
class NCR_ACTModel(Base):# for NCR act_section
    __tablename__='ncr_act'
    id=Column(Integer,primary_key=True,unique=True,index=True)  
    Act_id=Column(Integer,ForeignKey('kalam.id') , nullable=False)
    accused_id=Column(Integer,ForeignKey('ncr_accused.id'),nullable=False)
    Section=Column(Text)  
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    accused=relationship('AccusedModel',back_populates='act') 
    # ncr=relationship(NCRModel,back_populates='act')
    kalam=relationship('CrimeKalamModel',back_populates='ncr_act')
class FIRModel(Base):
    __tablename__='fir'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    complaint_id=Column(Integer,ForeignKey('complaint.id'),nullable=True)
    ps_state_id=Column(Integer,ForeignKey('state.id'),comment='police station state')
    ps_district_id=Column(Integer,ForeignKey('distric.id'),comment='police station district')
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
    Type_Information_id=Column(Integer,ForeignKey('infomode.id'))
    Dir_distance_From_Ps=Column(Text)
    Occurrence_Address=Column(Text)
    Beat_no=Column(String(200))
    State_id=Column(Integer,ForeignKey('state.id'),nullable=True,comment='outside police station state')
    Distric_id=Column(Integer,ForeignKey('distric.id'),nullable=True,comment='out side police station district')
    outside_ps=Column(Integer,ForeignKey('policestation.id'),nullable=True)
    status=Column(Integer,comment='0 for complaint & 1 for dir_fir')
    user_id=Column(Integer,comment="logine user id")
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    mode_information=relationship(Infomode_Model,backref='mode_information')
    # outside_state=relationship(StateModel,backref='outside_state')
    # outside_distric=relationship(DistricModel,backref='otside_distric')
    police_station=relationship('PoliceStationModel',backref='fir',foreign_keys=[P_Station])
    out_side_ps=relationship('PoliceStationModel',backref='fir_outside',foreign_keys=[outside_ps])
    fir_accused=relationship('FirAccused_model',backref='fir_accused',cascade='all,delete-orphan' )

class FirAccused_model(Base):
    __tablename__='fir_accused'
    id=Column(Integer,primary_key=True,autoincrement=True,unique=True)
    fir_id=Column(Integer,ForeignKey('fir.id'),nullable=False)
    Name=Column(String(200))
    Alias_Name=Column(String(200))
    Father_Name=Column(String(200))
    DOB=Column(Date)
    Age=Column(Integer)
    Mobile_Number=Column(String(12))
    Accused_Description=Column(Text)
    Image_Path=Column(String(200))
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    accused_act=relationship('FirActModel',backref='accused_act',cascade='all,delete-orphan')
    addresses=relationship('Fir_Accused_Address_Model',backref='addresses',cascade='all,delete-orphan')
class Fir_Accused_Address_Model(Base):
    __tablename__="fir_accused_address"
    id=Column(Integer,primary_key=True,autoincrement=True,unique=True,index=True) 
    Accused_id=Column(Integer,ForeignKey('fir_accused.id'),nullable=False) 
    Address_Type=Column(String(255))
    Address=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())

class FirActModel(Base):
    __tablename__='fir_act'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    accused_id=Column(Integer,ForeignKey('fir_accused.id'),nullable=False)
    Fir_Act=Column(Integer,ForeignKey('kalam.id'),nullable=False)
    Fir_Section=Column(Text)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    kalam=relationship('CrimeKalamModel',backref='fir_act')    

#--------------------model chargesheet---------------------------
class ChargeSheetModel(Base):
    __tablename__='charge_Sheet'
    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    State_id=Column(Integer,ForeignKey('state.id'))
    District_id=Column(Integer,ForeignKey('distric.id'))
    ps_id=Column(Integer,ForeignKey('policestation.id'),comment='police station id')#
    Year=Column(Integer)
    Fir_No=Column(String(200))
    Fir_Date=Column(Date) 
    ChargeSheet_No=Column(String(200),default=chargesheet_uid) 
    ChargeSheet_Date=Column(Date)
    Type_Final_Report=Column(String(200))
    If_FIR_Unoccured=Column(String(200))      
    If_ChargeSheet=Column(String(200))
    Name_IO=Column(String(200))
    IO_Rank=Column(Integer,ForeignKey('designation.id'))
    Name_Complainant=Column(String(200))
    Father_Name=Column(String(200))
    Detail_Properties=Column(Text,comment='details of sesized item/property/documents')
    user_id=Column(Integer,comment='current logine user')
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    charge_sheet_act=relationship('ChargeSheet_ActModel',back_populates='charge_sheet',cascade='delete,all')
    police_station=relationship(PoliceStationModel,back_populates='charge_sheet')
class ChargeSheet_ActModel(Base):
    __tablename__='chargesheet_act'
    id=Column(Integer,primary_key=True,autoincrement=True)
    ChargeSheet_id=Column(Integer,ForeignKey('charge_Sheet.id'))
    ChargeSheet_Act=Column(Integer,ForeignKey('kalam.id'))
    ChargeSheet_Section=Column(Text) 
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    charge_sheet=relationship(ChargeSheetModel,back_populates='charge_sheet_act')
    kalam=relationship(CrimeKalamModel,back_populates='charge_sheet_act')   
#_____________________Enquiry_form_________________________
class EnquiryFormModel(Base):
    __tablename__='enquiry_form'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Police_Station_id=Column(Integer,ForeignKey('policestation.id'))
    Accused_Name=Column(String(200))
    Nick_Name=Column(String(200))
    Father_or_Wife_Name=Column(String(200))
    Age=Column(String(200))
    Mob_Number=Column(String(200))
    Height=Column(String(50))
    Body_Complexion=Column(String(100))
    Body_Type=Column(String(200))
    Eyes_Colur=Column(String(100))
    Hair_Colur=Column(String(100))
    Langues_id=Column(Integer,ForeignKey('langues.id'))
    Identification_Mark=Column(Text)
    Subcast_id=Column(Integer,ForeignKey('subcast.id'))
    Occupation_id=Column(Integer,ForeignKey('Occupation.id'))
    Address=Column(Text)
    Residence_Address=Column(Text)
    Birth_Place=Column(Text)
    Is_Father_Alive=Column(String(50))
    Father_Name=Column(String(200))
    Father_Address=Column(Text)
    Father_Occupation_id=Column(Integer,ForeignKey('Occupation.id'))
    Is_Father_Property=Column(String(50))
    Fater_Property_detail=Column(Text)
    Is_Mother_Alive=Column(String(50))
    Mother_Details=Column(Text)
    Brother_or_Sister=Column(String(50))
    Brother_Sister_Details=Column(Text)
    Relative_or_Friends=Column(String(50))
    Relative_Friends_Details=Column(Text)
    Is_Own_Property=Column(String(50))
    Own_Property_Details=Column(Text)
    Is_Education=Column(String(20))
    Education_Details=Column(Text)
    Is_Married=Column(String(20))
    Wife_or_Husband_Details=Column(Text)
    How_long_Current_Address=Column(String(20))
    Who_Knows_You=Column(Text)
    Know_Other_Than_Relative=Column(Text)
    Proffession_Before_Coming=Column(Text)
    Arrested_Before=Column(Text) 
    Is_Sentence_before=Column(String(20))
    Sentence_Details=Column(Text)
    is_CommitedCrime_Arrested_anyone=Column(String(20))
    Details_Anyone=Column(Text)
    Stolen_Goodes_Sized_From=Column(Text)
    PO_Details_Accused=Column(Text)
    Stay_Other_Place=Column(Text)
    PO_Emp=Column(Text)
    Is_commited_Crime_Before=Column(String(200))
    Reason_Commited_Crime=Column(Text)
    Started_Crime=Column(String(50))
    Gang_or_Group=Column(String(200))
    Crime_to_Other_Gang=Column(Text)
    Where_Crime_Commited=Column(Text)
    DoYouKnow_OtherCriminal=Column(Text)
    HowMuch_MonyStolen=Column(String(200))
    Where_Go_Before_Crime=Column(Text)
    Where_Stop_Ofter_Crime=Column(Text)
    Whose_sold_Stolen_Assets=Column(Text)
    Robbery_Other_Distric=Column(Text)
    Patner_in_Villege=Column(Text)
    How_Learn_Commiting_Crime=Column(String(200))
    Which_Village_Gang_Activate=Column(Text)
    Gang_Main_Adda=Column(Text)
    Which_Town_Visited_Often=Column(Text)
    Know_Robbery_Next=Column(String(200))
    Gang_any_Addiction=Column(String(200))
    Why_left_PrevGang=Column(Text)
    How_Steal_NewVillage=Column(Text)
    Clicked_Photes_Where=Column(Text)
    When_Police_ShowUp=Column(Text)
    Which_langues_use_Crime=Column(Integer,ForeignKey('langues.id'))
    Steal_Everyday=Column(String(200))
    is_Drink_Alchol=Column(String(50))
    Entertainment_Media=Column(Text)
    Where_Sleep_Night=Column(String(200))
    Where_Take_Shelter=Column(Text)
    Image_Path=Column(String(200))
    user_id=Column(Integer)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now()) 
    police_station=relationship("PoliceStationModel",backref='policestation')
    subcast=relationship("SubcastModel",backref='subcast')
    accuse_langues=relationship(LanguesModel,foreign_keys=[Langues_id],backref='accuse_langues')
    crime_langues=relationship(LanguesModel,foreign_keys=[Which_langues_use_Crime],backref='crime_langues')
    accused_occupation=relationship(OccupationModel,foreign_keys=[Occupation_id],backref='accused_occupation')
    father_occupation=relationship(OccupationModel,foreign_keys=[Father_Occupation_id],backref='father_occupation')
#--------------------Accused_name----------------------------------------------
class YellowCardModel(Base):
    __tablename__='yellow_card'
    id=Column(Integer,primary_key=True,autoincrement=True,unique=True)
    Accused_Name=Column(String(200)) 
    Accused_Age=Column(Integer)
    PS_id=Column(Integer,ForeignKey("policestation.id"))
    Accused_Bplace=Column(Text)
    Accused_Height=Column(String(200))
    Accused_Bcomplexion=Column(String(200))
    Accused_Btype=Column(String(200))
    Accuse_Ecolur=Column(String(200))
    Accused_Hcolur=Column(String(200))
    Occupation_id=Column(Integer,ForeignKey('Occupation.id'))
    Accused_Imark=Column(Text)
    Scast_id=Column(Integer,ForeignKey('subcast.id'))
    Accused_Education=Column(String(200))
    Pstation_Rnumber=Column(String(200))
    CRD_Number=Column(String(200))
    Accused_Address=Column(Text)
    Accused_ImgPath=Column(String(200))
    Caddress_Saddress=Column(Text)
    Moment_Oinfo=Column(Text)
    Pofficer_who_Iaccused=Column(Text)
    Relativ_Friends=Column(Text)
    Accused_Fdetails=Column(Text)
    Wife_Details=Column(Text)
    Apartner_MOBnumber=Column(Text)
    Pcrime_Pstation=Column(Integer,ForeignKey('policestation.id'),comment='previous crime under which policestation')#prove crime
    Crime_Number=Column(String(200))
    Crime_Date=Column(DateTime)
    Pcrime_Sentence=Column(String(200),comment='previous crime punishment')
    Pcrime_Date=Column(DateTime,comment='privious crime sentence date')
    user_id=Column(Integer)
    create_date=Column(DateTime,default=get_current_time)
    update_date=Column(DateTime,default=get_current_time,onupdate=func.now())
    police_station=relationship(PoliceStationModel,foreign_keys=[PS_id],backref='police_station')
    prv_pstation=relationship(PoliceStationModel,foreign_keys=[Pcrime_Pstation],backref='prv_pstation')
    occupation=relationship(OccupationModel,backref='occupation')
    ycard_subcast=relationship(SubcastModel,backref='ycard_subcast')
















    

    



Base.metadata.create_all(bind=engine)