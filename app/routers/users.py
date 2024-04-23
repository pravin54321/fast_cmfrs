from fastapi import APIRouter
router = APIRouter()
from ..dependencies import *
from ..models.models import *
from  ..schemas.schemas import *
from .algo import imgprocess,SearchImage
from .authentication import *
home_dir='C:/Cluematrix/FaceRecogniationNewProject/'


#--------------------------Authuntication---------------------------------
#-----------------signup-----------------------------
@router.post("/sp_log",response_model=UserBaseGet,tags=['Authentication'])
async def user_creation(current_user:Annotated[UserBase,Depends(get_current_active_user)],user:UserBase,db:Session=Depends(getdb)):
    email_exist = db.query(UserModel).filter(UserModel.UserEmail==user.UserEmail).first()
    if email_exist:
         raise HTTPException(detail='Email id already exist',status_code=status.HTTP_400_BAD_REQUEST)
    password = get_password_hash(user.UserPassword)
    setattr(user,'UserPassword',password)
    user=UserModel(**user.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
@router.post("/signup",response_model=Admin_BaseGet,tags=['Authentication'])
async def admin_created(admin:Admin_Base,db:Session=Depends(getdb)):
     email_exist=db.query(UserModel).filter(UserModel.UserEmail==admin.UserEmail).first()
     if email_exist:
          raise HTTPException(detail='Email already exist',status_code=status.HTTP_400_BAD_REQUEST)
     password=get_password_hash(admin.UserPassword)
     setattr(admin,'UserPassword',password)
     admin=UserModel(**admin.model_dump()) 
     db.add(admin)
     db.commit()
     db.refresh(admin)
     return admin   
    
#------------------logine--------------------------
@router.post('/login',tags=['Authentication'])
def logine_for_acess_token(form_data : Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(getdb)):  
    user = authuntication(form_data.username,form_data.password)
    if not user:
        raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Incorrct Username and Password",
               headers={"WWW-Authenticate": "Bearer"},
          )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
    data={"sub": user.UserEmail}, expires_delta=access_token_expires
    )
    if user.Role == 0:
         return{"user":user.UserName,
                "useremail":user.UserEmail,
                "mobile_number":user.Mobile_Number,
                "designation":{"id":user.Designation_id,"designation":user.User_Designation},
                "police_station":{"id":user.pstation_id,"police_station":user.police_station,
                "access_token": access_token,"token_type": "bearer"}
                }
    elif user.Role == 1:
         return{"user":user.UserName,
                "useremail":user.UserEmail,
                "mobile_number":user.Mobile_Number,
                "designation":{"id":user.Designation_id,"designation":user.User_Designation},
                "posting_distric":{"id":user.Posting_Distric,"police_station":user.Posting_Distric},
                 "access_token": access_token,"token_type": "bearer"
                }
    elif user.Role == 2:
          return{"user":user.UserName,
                "useremail":user.UserEmail,
                "mobile_number":user.Mobile_Number,
                "designation":{"id":user.Designation_id,"designation":user.User_Designation},
                "police_station":{"id":user.pstation_id,"police_station":user.police_station},
                "access_token": access_token,"token_type": "bearer"
                }   
         
#-----------------user_activate_deactivate----------------------------
@router.post('/dactivate_user/{user_id}',tags=['Authentication'])
async def dactivate(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                    user_id:int,db:Session=Depends(getdb)):
     user_exist=db.query(UserModel).filter(UserModel.id==user_id).update({'disabled':0})
     db.commit()
     if user_exist is 1:
          return Response(content=f"user deactivate successfully",status_code=status.HTTP_200_OK)
     raise HTTPException(detail=f"id-{user_id} does not exist",status_code=status.HTTP_400_BAD_REQUEST)
@router.put('/activate_user/{user_id}',tags=['Authentication'])
async def activate(current_user:Annotated[UserBase,Depends(get_current_active_user)],
                   user_id:int,db:Session=Depends(getdb)):
     user_exist=db.query(UserModel).filter(UserModel.id==user_id).update({'disabled':1})
     db.commit()
     if user_exist is 1:
          return Response(content=f'user acivate successfully',status_code=status.HTTP_200_OK)
     raise HTTPException(detail=f'id-{user_id} does not exist',status_code=status.HTTP_400_BAD_REQUEST)
          

#------------------------person_information-----------------------------
@router.post('/person/',tags=['Person'])
async def create_person( 
                current_user: Annotated[UserBase, Depends(get_current_active_user)],
                Name: str = Form(...),
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
                            await a.facedetection("face_image",db,save=False)
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
        await obj.facedetection("search_faceimage",db,save=False)
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
async def get_all_personData(current_user: Annotated[UserBase, Depends(get_current_active_user)],db: Session = Depends(getdb)):
    """ get all person data"""
    try:
        person = db.query(PersonModel).all()
        return person
    except Exception as e:
         raise HTTPException(status_code=400,detail=str(e))
#get singale person
@router.get('/person/{person_id}',response_model=PersonImage,tags=['Person'])
async def get_person(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                     person_id:int,db: Session = Depends(getdb)):
    """get singale person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404,detail="person is not found")
    return person
#update_person
@router.put('/person/{person_id}',response_model=PersonBase,tags=['Person'])
async def update_person(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                       person_id:int,person_data:PersonBase,db: Session = Depends(getdb)):
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
async def person_delete(current_user: Annotated[UserBase, Depends(get_current_active_user)],
                        person_id:int,db: Session = Depends(getdb)):
    """delete person"""
    person = db.query(PersonModel).filter(PersonModel.id == person_id).first()  
    if person is None:
        raise HTTPException(status_code=404,detail='person not found') 
    db.delete(person)
    db.commit()
    return {"msg":"Person has been deleted"}

#-----------------------------group_photo-----------------------------------------------------------------------
@router.post('/groupimg/',response_model=list[GroupImg],tags=['group_image'])
async def search_groupimg(img:UploadFile = File(..., media_type="image/jpeg, image/png"),db:Session=Depends(getdb)):
    try: 
        db.query(GroupImageModel).delete()
        obj=imgprocess()
        await obj.store_img(img,'group_image')
        await obj.facedetection('group_face',db,save=True)
        grp_img = db.query(GroupImageModel).all()
        return grp_img
    except Exception as e:
         raise MyCustomeException(detail=str(e))
#------------------------------search_group_image-------------------------------------------------------
@router.post('/searchgroupimg',tags=['group_image'])
async def gimg_search(img:str,db:Session=Depends(getdb)):
     img_path=home_dir+img
     try:
          obj = imgprocess()
        #   await obj.store_img(img,"search_img")    
        #   await obj.facedetection("search_faceimage",db,save=False)
          await obj.facelandmark_gimg("gface_landmark",img_path)
          embedding=await obj.embedding(None,None)
          obj_01 = SearchImage(embedding,db)
          result = await obj_01.SingaleImageSearch_02()
          data = await obj_01.FinalResult(result)
          all_image=db.query(GroupImageModel).all()
          return {'Result':data,
                  'Image':all_image
                  }
     except Exception as e:
          raise MyCustomeException(detail=str(e))
