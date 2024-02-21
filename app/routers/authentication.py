from sqlalchemy import func
from ..dependencies import *
from ..models.models import *
from ..database import SessionLocal,getdb
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
import mysql.connector
from ..schemas import *
from datetime import datetime,timedelta

dlt_img='C:/Cluematrix/FaceRecogniationNewProject/'
def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(UserEmail:str):
    db = SessionLocal()
    print("user_email--------->",UserEmail)
    user_data = db.query(UserModel).filter(UserModel.UserEmail==UserEmail).first()
    print("user_present",user_data)
    if user_data is not None:
        user_dict = {
            "id":user_data.id,
            "UserName": user_data.UserName,
            "UserEmail": user_data.UserEmail,
            "Mobile_Number":user_data.Mobile_Number,
            "UserPassword": user_data.UserPassword,
            "disabled":user_data.disabled,
            "Designation_id":user_data.User_Designation,
            "User_Designation":user_data.designation.Designation if user_data.User_Designation is not None else None,
            "district_id":user_data.Posting_Distric,
            "Posting_Distric":user_data.district.Distric if user_data.Posting_Distric is not None else None,
            "pstation_id":user_data.Pstation_id,
            "police_station":user_data.police_station.PoliceStation if user_data.Pstation_id  is not None else None,
            "Role":user_data.Role
          }
        return hash_password(**user_dict)
    else:
        return None
def authuntication(UserEmail:str,password:str):
    user = get_user(UserEmail)
    print(UserEmail)
    print(user)
    if not user:
        return False
    verify_pwd=verify_password(password,user.UserPassword)
    if not verify_pwd:
        return False
    return user
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:Annotated[str,Depends(oauth_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    db = SessionLocal()
    try:
        payloadm = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_email:str = payloadm.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = TokenData(username=user_email)
    except JWTError:
        raise credentials_exception
    user = get_user(UserEmail=user_email)
    if user is None:
        raise credentials_exception
    return user    
async def get_current_active_user(current_user:Annotated[UserBase,Depends(get_current_user)]):
    if current_user.disabled:
         print("========",current_user)
         return current_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Inactive user"
                        )
   
#_____________image_store_for_complaint---------------------
from .algo  import StoreImage 
async def imagestore(file,subdir):
    unique_filename=f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file_path=os.path.join(f'{StoreImage}{subdir}',unique_filename)
    async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(1024):
                try:
                    await f.write(chunk)
                except Exception as e:
                    print(f"Error while writing the file: {e}")
    return unique_filename                
#________________delete_image_in folder___________
async def dlt_image(file_path):
    file_path=f"{dlt_img}/{file_path}"
    try:
        os.remove(file_path)
        print('file_deleted_successfully')
    except FileNotFoundError:
        print('file_does not exist ')
    except Exception as e:
        print(f'error deleting file:{e}')    
       
