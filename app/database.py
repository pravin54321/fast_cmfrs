from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm  import sessionmaker
from sqlalchemy.orm import Session
from .dependencies import *
from .schemas.schemas import *
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/cmfrs_01"
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_size=20, max_overflow=30)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind= engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)

# def getdb():
#     db=SessionLocal()
#     try:
#         yield db
#     except:
#         db.close()  

def getdb():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        # Log the exception or handle it accordingly
        print(f"An error occurred: {e}")
        # Rollback the transaction to maintain consistency
        db.rollback()
    finally:
        # Close the session to release the connection back to the pool
        db.close()