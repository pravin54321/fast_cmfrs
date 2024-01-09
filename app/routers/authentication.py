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
def get_user(UserName:str):
    db = SessionLocal()
    user_data = db.query(UserModel).filter(UserModel.UserName==UserName).first()
    if user_data is not None:
        user_dict = {
            "UserName": user_data.UserName,
            "UserEmail": user_data.UserEmail,
            "UserPassword": user_data.UserPassword,
            "disabled":user_data.disabled,
          
        }
        return hash_password(**user_dict)
    else:
        return None
def authuntication(UserName:str,password:str):
    user = get_user(UserName)
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
    try:
        payloadm = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = payloadm.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(UserName = token_data.username)
    if user is None:
        raise credentials_exception
    return user    
async def get_current_active_user(current_user:Annotated[UserBase,Depends(get_current_user)]):
    if current_user is current_user.disabled:
        raise HTTPException(status=status.HTTP_400_BAD_REQUEST,
                            detail="Inactive user"
                            )
    return current_user


#_________________unique_id_for complaint_______________
def complaint_uid():
    import datetime
    db=SessionLocal()
    prev_complaint=db.query(ComplaintModel).order_by(ComplaintModel.id.desc()).first()
    if prev_complaint:
        prev_complaint=prev_complaint.Complaint_uid
        prev_complaint=int(prev_complaint.split("-")[-1]) + 1
    else:
        prev_complaint=1    
    today_date=datetime.date.today().strftime('%Y%m%d')
    complaint_id = f"COM-{today_date}-{str(prev_complaint).zfill(5)}"
    return complaint_id
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
    if os.path.exists(file_path):
        os.remove(file_path)
        print('file_deleted_successfully')
      
    else:
        print('file_does not delete ')
       
