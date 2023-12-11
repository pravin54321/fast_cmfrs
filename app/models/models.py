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

class RegionModel(Base):
    __tablename__='region' 
    id = Column(Integer,primary_key=True,autoincrement=True)
    Region = Column(String(200),unique=True,nullable= False)
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    headoffices= relationship('HeadOfficeModel',back_populates='region') 
    subdivision=relationship('SubdivisionModel',back_populates='region')  

class DistricModel(Base):
    __tablename__='distric'
    id = Column(Integer,primary_key=True,autoincrement=True)
    Distric = Column(String(200),unique=True,nullable=True)
    create_date = Column(DateTime,default=datetime.utcnow)
    update_date = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    headoffices = relationship('HeadOfficeModel',back_populates='distric')   
    subdivision=relationship('SubdivisionModel',back_populates='distric')
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

Base.metadata.create_all(bind=engine)