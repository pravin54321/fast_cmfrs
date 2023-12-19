from sqlalchemy import Column,Integer,String,Text,ForeignKey,LargeBinary,Boolean,DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from ..database import Base,engine
target_metadata = Base.metadata


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
    State = Column(String(200),nullable=False,unique=True)
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    headoffices= relationship('HeadOfficeModel',back_populates='state')
    subdivision=relationship('SubdivisionModel',back_populates='state')
    taluka=relationship('TalukaModel',back_populates='state')
    policestation=relationship('PoliceStationModel',back_populates='state')
    post=relationship('PostModel',back_populates='state')

class RegionModel(Base):
    __tablename__='region' 
    id = Column(Integer,primary_key=True,autoincrement=True)
    Region = Column(String(200),unique=True,nullable= False)
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    headoffices= relationship('HeadOfficeModel',back_populates='region') 
    subdivision=relationship('SubdivisionModel',back_populates='region')
    taluka=relationship('TalukaModel',back_populates='region')
    policestation=relationship('PoliceStationModel',back_populates='region')
    post=relationship('PostModel',back_populates='region')  

class DistricModel(Base):
    __tablename__='distric'
    id = Column(Integer,primary_key=True,autoincrement=True)
    Distric = Column(String(200),unique=True,nullable=True)
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    headoffices = relationship('HeadOfficeModel',back_populates='distric')   
    subdivision=relationship('SubdivisionModel',back_populates='distric')
    taluka=relationship('TalukaModel',back_populates='distric')
    policestation=relationship('PoliceStationModel',back_populates='distric')
    post=relationship('PostModel',back_populates='distric')
class HeadOfficeModel(Base):
    __tablename__='headoffice'
    id = Column(Integer,primary_key=True,autoincrement=True,index=True) 
    HeadOffice=Column(String(200),unique=True,nullable=True)
    State_id = Column(Integer,ForeignKey('state.id'))
    Region_id = Column(Integer,ForeignKey('region.id'))
    Distric_id = Column(Integer,ForeignKey('distric.id'))
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    state = relationship('StateModel',back_populates='headoffices')
    region = relationship('RegionModel',back_populates='headoffices')
    distric = relationship('DistricModel',back_populates='headoffices')
    subdivision=relationship('SubdivisionModel',back_populates='headoffice')
    taluka=relationship('TalukaModel',back_populates='headoffice')
    policestation=relationship('PoliceStationModel',back_populates='headoffice')
    post=relationship('PostModel',back_populates='headoffice')
class SubdivisionModel(Base):
    __tablename__='subdivision'
    id=Column(Integer,primary_key=True,autoincrement=True)
    Subdivision=Column(String(200),unique=True)
    State_id=Column(Integer,ForeignKey('state.id'))    
    Region_id=Column(Integer,ForeignKey('region.id'))
    Distric_id=Column(Integer,ForeignKey('distric.id'))
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    state=relationship('StateModel',back_populates='subdivision')
    region=relationship('RegionModel',back_populates='subdivision')
    distric=relationship('DistricModel',back_populates='subdivision')
    headoffice=relationship('HeadOfficeModel',back_populates='subdivision')
    taluka=relationship('TalukaModel',back_populates='subdivision')
    policestation=relationship('PoliceStationModel',back_populates='subdivision')
    post=relationship('PostModel',back_populates='subdivision')
class TalukaModel(Base):
    __tablename__='taluka'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    Taluka=Column(String(200))
    State_id=Column(Integer,ForeignKey('state.id'))
    Region_id=Column(Integer,ForeignKey('region.id'))
    Distric_id=Column(Integer,ForeignKey('distric.id'))
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'))
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id')) 
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    state=relationship('StateModel',back_populates='taluka')
    region=relationship('RegionModel',back_populates='taluka')  
    distric=relationship('DistricModel',back_populates='taluka') 
    headoffice=relationship('HeadOfficeModel',back_populates='taluka')
    subdivision=relationship('SubdivisionModel',back_populates='taluka')
    policestation=relationship('PoliceStationModel',back_populates='taluka')
    post=relationship('PostModel',back_populates='taluka')
class PoliceStationModel(Base):
    __tablename__='policestation'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)
    PoliceStation=Column(String(200))
    State_id=Column(Integer,ForeignKey('state.id'))
    Region_id=Column(Integer,ForeignKey('region.id'))
    Distric_id=Column(Integer,ForeignKey('distric.id'))
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'))
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id'))
    Taluka_id=Column(Integer,ForeignKey('taluka.id'))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    state=relationship('StateModel',back_populates='policestation')
    region=relationship('RegionModel',back_populates='policestation')
    distric=relationship('DistricModel',back_populates='policestation')
    headoffice=relationship('HeadOfficeModel',back_populates='policestation')
    subdivision=relationship('SubdivisionModel',back_populates='policestation')
    taluka=relationship('TalukaModel',back_populates='policestation')
    post=relationship('PostModel',back_populates='policestation')
   
class PostModel(Base):
    __tablename__='post'
    id=Column(Integer,primary_key=True,autoincrement=True)
    Post=Column(String(200))
    State_id=Column(Integer,ForeignKey('state.id'))
    Region_id=Column(Integer,ForeignKey('region.id'))
    Distric_id=Column(Integer,ForeignKey('distric.id'))
    HeadOffice_id=Column(Integer,ForeignKey('headoffice.id'))
    Subdivision_id=Column(Integer,ForeignKey('subdivision.id'))
    Taluka_id=Column(Integer,ForeignKey('taluka.id'))
    PoliceStation_id=Column(Integer,ForeignKey('policestation.id'))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
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
    Religion=Column(String(200))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow) 
    cast=relationship('CastModel',back_populates='religion') 
    subcast=relationship('SubcastModel',back_populates='religion')

class CastModel(Base):
    __tablename__='cast'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True) 
    Cast=Column(String(200))
    Religion_id=Column(Integer,ForeignKey('religion.id'))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    religion=relationship('ReligionModel',back_populates='cast')
    subcast=relationship('SubcastModel',back_populates='cast') 
class SubcastModel(Base):
    __tablename__='subcast'
    id=Column(Integer,primary_key=True,autoincrement=True)  
    Subcast=Column(String(200))
    Religion_id=Column(Integer,ForeignKey('religion.id'))
    Cast_id=Column(Integer,ForeignKey('cast.id')) 
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    religion=relationship('ReligionModel',back_populates='subcast')
    cast=relationship('CastModel',back_populates='subcast')
#--------langues_model--------
class LanguesModel(Base):
    __tablename__='langues'         
    id=Column(Integer,autoincrement=True,primary_key=True)
    Langues=Column(String(200))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)  
#________Occupation_model_________
class OccupationModel(Base):
    __tablename__='Occupation'
    id=Column(Integer,autoincrement=True,index=True,primary_key=True)
    Occupation=Column(String(200))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow) 
#_________outhperson_model________
class OuthPersonModel(Base):   
    __tablename__='outhperson'
    id=Column(Integer,primary_key=True,autoincrement=True,index=True)                 
    OuthPerson=Column(String(200))
    create_date=Column(DateTime,default=datetime.utcnow)
    update_date=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)

    



Base.metadata.create_all(bind=engine)