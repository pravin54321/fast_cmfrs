from fastapi import APIRouter
router = APIRouter()
from ..dependencies import *
from ..models.models import *
from  ..schemas.schemas import *
from .algo import imgprocess,SearchImage

#------------------------person_information------------------------------------
@router.post('/person/',tags=['Person'])
async def create_person( Name: str = Form(...),
                Mobile_Number: int = Form(...),
                Email: EmailStr|None = Form(None),
                Age: int = Form(...),
                Gender: str = Form(...),
                Address: str = Form(...),
                Status: str = Form(...),
                Images: UploadFile = File(...),
                db: Session = Depends(getdb),
            ):
            person_exists =  db.query(PersonModel).filter(PersonModel.Email==Email).first()
            if person_exists:
                raise HTTPException(status_code=400,detail="Email already exists") 
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
                        db.refresh(person_data)
                        
                        # return {"message": "Person created successfully"}
                    except Exception as e:
                         db.rollback()
                         raise HTTPException(status_code=400,detail="An error occurred while processing your request.")
                    try:
                            a = imgprocess()
                            await a.store_img(Images,"Person_Image")
                            await a.facedetection("face_image")
                            await a.facelandmark("face_landmark")
                            await a.embedding(person_data.id,db)
                            return{"msg":"Person has been save successfully"}  
                    except Exception as e:
                        raise MyCustomeException(detail=str(e))
            except Exception as e:
                 raise HTTPException(status_code=400,detail=str(e)) 
                #  return {"error":str(e)}    
#_______________testing_image_____________
@router.post('/test',response_model=list[imagedata])
async def encoding( db: Session = Depends(getdb)):
    data = []
    l = (1,2,3)
    for id in l:
        person = db.query(PersonImgModel).filter(PersonImgModel.id == id).first()
        image_distance = imagedata(
            Person_id = person.Person.id, 
            id=person.id,
            file_path=person.file_path,
            distance=10,  # Adjust this based on your requirement
            Person={
                "id":person.Person.id,
                "Name":person.Person.Name,
                "Age":person.Person.Age,
                "Address":person.Person.Address,
                "Gender":person.Person.Gender,
                "Mobile_Number":person.Person.Mobile_Number,
                "Status":person.Person.Status,
                "Email":person.Person.Email,
            }
        )
        data.append(image_distance)
    return data
    
  
    
# serach  a singale person
@router.post('/search',tags=['singale_image'])
async def serachimg(img:UploadFile = File(..., media_type="image/jpeg, image/png"),
                    type:str=type, db: Session = Depends(getdb)): 
    try:
        obj = imgprocess()
        await obj.store_img(img,"search_img")
        await obj.facedetection("search_faceimage")
        await obj.facelandmark("search_landmark")
        embedding=await obj.embedding(None,None)
        obj_01 = SearchImage(embedding,db)
        if type=='one':
           result = await obj_01.SingaleImageSearch_01()
           data = await obj_01.FinalResult(result)
           return data
        result = await obj_01.SingaleImageSearch_02()
        data = await obj_01.FinalResult(result)
        return data
    except Exception as e:
        raise MyCustomeException(detail=str(e))
        
    

               
      
 
                              
@router.get('/person/',response_model=list[PersonImage],tags=['Person'])
async def get_all_personData(db: Session = Depends(getdb)):
    """ get all person data"""
    try:
        person = db.query(PersonModel).all()
        return person
    except Exception as e:
         raise HTTPException(status_code=400,detail=str(e))
#get singale person
@router.get('/person/{person_id}',response_model=PersonImage,tags=['Person'])
async def get_person( person_id:int,db: Session = Depends(getdb)):
    """get singale person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404,detail="person is not found")
    return person
#update_person
@router.put('/person/{person_id}',response_model=PersonBase,tags=['Person'])
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
@router.delete('/person/{person_id}' , response_model=dict,tags=['Person']) 
async def person_delete(person_id:int,db: Session = Depends(getdb)):
    """delete person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()  
    if person is None:
        raise HTTPException(status_code=404,detail='person not found') 
    db.delete(person)
    db.commit()
    return {"msg":"Person has been deleted"}

