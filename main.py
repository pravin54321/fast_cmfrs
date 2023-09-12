from fastapi import FastAPI,Depends,HTTPException
from schemas import *
from models import *
from sqlalchemy.orm import Session
from database import getdb
from pydantic import ValidationError
from fastapi.responses import JSONResponse
import os
import uuid
from datetime import datetime



app = FastAPI()

@app.get('/')
def root():
    msg="Hellow"
    return msg


# @app.post('/person/', response_model=PersonBase)
# def create_person(person: PersonBase,  db: Session = Depends(getdb)):
   
  
#     try:
#         db_person = PersonModel(**person.model_dump())
#         db.add(db_person)
#         db.commit()
#         db.refresh(db_person)
#         return person
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500,detail=str(e))
@app.post("/person/")
async def create_upload_files(files: list[UploadFile]):
    for file in files:
        upload_dir = "Upload"
        os.makedirs(upload_dir, exist_ok=True)
        unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{str(uuid.uuid4())}_{file.filename}"
        file_path = os.path.join(upload_dir,unique_filename)
        with open(file_path,"wb") as f:
            f.write(file.file.read())

    return {"filenames": [file.filename for file in files]}
    
#get all person data    
@app.get('/person/',response_model=list[PersonBase])
async def get_all_personData(db: Session = Depends(getdb)):
    """ get all person data"""
    person = db.query(PersonModel).all()
    return person
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