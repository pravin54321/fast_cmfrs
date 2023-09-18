from fastapi import FastAPI,Depends,HTTPException,UploadFile,File,Form,Query
from schemas import *
from models import *
from sqlalchemy.orm import Session
from database import getdb
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
from datetime import datetime
import json
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware
origins = ["*"]  # Replace with your allowed origins (e.g., ["http://localhost:3000"])
app = FastAPI()
app.mount("/Static",StaticFiles(directory="Static") , name="images")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # You can specify specific HTTP methods here (e.g., ["GET", "POST"])
    allow_headers=["*"],  # You can specify specific HTTP headers here
)







@app.get('/')
def root():
    msg="Hellow"
    return msg

#------------------------person_information------------------------------------
@app.post('/person/',)
async def create_person( Name: str = Form(...),
                Mobile_Number: int = Form(...),
                Email: EmailStr|None = Form(None),
                Age: int = Form(...),
                Gender: str = Form(...),
                Address: str = Form(...),
                Status: str = Form(...),
                Images: list[UploadFile] = File(...),
                db: Session = Depends(getdb),
            ):
         
            try:
                    try:  
                        person_data = PersonModel(
                            Name=Name,
                            Mobile_Number=Mobile_Number,
                            Email=Email,
                            Age=Age,
                            Gender=Gender,
                            Address=Address,
                            Status=Status)
                        db.add(person_data)
                        db.commit()
                        # return {"message": "Person created successfully"}
                    except Exception as e:
                         db.rollback()
                         raise HTTPException(status_code=400,detail="An error occurred while processing your request.")
                    try:
                         StoreImage = "Static/Images/Person_Image"
                         os.makedirs(StoreImage,exist_ok=True)
                         for img in Images:
                            unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{img.filename}"
                            file_path = os.path.join(StoreImage,unique_filename)
                            with open(file_path,"wb") as f:
                                 f.write(img.file.read())
                            imageModel = PersonImgModel(file_path=unique_filename,Person_id=person_data.id)
                            db.add(imageModel)
                         db.commit()
                         return{"msg":"Person has been save successfully"}   
                    except Exception as e:
                         raise HTTPException(status_code=400,detail="An error occurred while processing your request.")
                     
            except Exception as e:
                 raise HTTPException(status_code=400,detail="An error occurred while processing your request.")        
                              
@app.get('/person/',response_model=list[PersonImage])
async def get_all_personData(db: Session = Depends(getdb)):
    """ get all person data"""
    try:
        person = db.query(PersonModel).all()
        return person
    except Exception as e:
         raise HTTPException(status_code=400,detail=str(e))
#get singale person
@app.get('/person/{person_id}',response_model=PersonBase)
async def get_person( person_id:int,db: Session = Depends(getdb)):
    """get singale person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404,detail="person is not found")
    return person
#update_person
@app.put('/person/{person_id}',response_model=PersonBase)
async def update_person(person_id:int,person_data:PersonBase,db: Session = Depends(getdb)):
    """prson data update"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="person not found")
    for key,value  in person_data.dict().items():
        setattr(person,key,value)
    db.commit()
    db.refresh(person)
    return person
@app.delete('/person/{person_id}' , response_model=dict) 
async def person_delete(person_id:int,db: Session = Depends(getdb)):
    """delete person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()  
    if person is None:
        raise HTTPException(status_code=404,detail='person not found') 
    db.delete(person)
    db.commit()
    return {"msg":"Person has been deleted"}



    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)