from sqlalchemy import Column,Integer,String,Text,ForeignKey,LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base,engine


class PersonModel(Base):
    __tablename__="person"
    id = Column(Integer,primary_key=True,index=True)
    Name = Column(String(255))
    Mobile_Number = Column(Integer)
    Email = Column(String(255))
    Age = Column(Integer)
    Gender = Column(String(50))
    Address = Column(Text)
    Status = Column(String(255))
    Image = relationship('PersonImgModel',back_populates='Person')
class PersonImgModel(Base):
    __tablename__="personimg"
    id = Column(Integer,primary_key=True,index=True)
    file_path = Column(String(255))
    # face_encoding = Column(LargeBinary)
    Person_id = Column(Integer,ForeignKey('person.id'))
    Person = relationship('PersonModel',back_populates='Image')

Base.metadata.create_all(bind=engine)