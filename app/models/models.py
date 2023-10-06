from sqlalchemy import Column,Integer,String,Text,ForeignKey,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
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

Base.metadata.create_all(bind=engine)