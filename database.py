from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker
from sqlalchemy.orm import Session



SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/cmfrs_new"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind= engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

def getdb():
    db=SessionLocal()
    try:
        yield db
    except:
        db.close()    