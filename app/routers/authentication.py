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
db = SessionLocal()
def get_user(UserEmail:str):
    user_data = db.query(UserModel).filter(UserModel.UserEmail==UserEmail).first()
    if user_data is not None:
        user_dict = {
            "id":user_data.id,
            "UserName": user_data.UserName,
            "UserEmail": user_data.UserEmail,
            "UserPassword": user_data.UserPassword,
            "disabled":user_data.disabled,
          
        }
        return hash_password(**user_dict)
    else:
        return None
def authuntication(UserEmail:str,password:str):
    user = get_user(UserEmail)
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
        username:str = payloadm.get("sub")
        user_item=db.query(UserModel).filter(UserModel.UserName==username).first()
        if user_item is None:
            raise credentials_exception
        token_data = TokenData(username=user_item.UserEmail)
    except JWTError:
        raise credentials_exception
    user = get_user(UserEmail=user_item.UserEmail)
    if user is None:
        raise credentials_exception
    return user    
async def get_current_active_user(current_user:Annotated[UserBase,Depends(get_current_user)]):
    if current_user.disabled:
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
def dlt_image(file_path):
    file_path=f"{dlt_img}/{file_path}"
    try:
        os.remove(file_path)
        print('file_deleted_successfully')
    except FileNotFoundError:
        print('file_does not exist ')
    except Exception as e:
        print(f'error deleting file:{e}')    
       
