from ..dependencies import *
from ..database import SessionLocal
db = SessionLocal()





def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)
def get_user(UserName:str):
    user_data = db.query(UserModel).filter(UserModel.UserName==UserName).first()
    if user_data is not None:
        user_dict = {
            "UserName": user_data.UserName,
            "UserEmail": user_data.UserEmail,
            "UserPassword": user_data.UserPassword,
        }
        return hash_password(**user_dict)
    else:
        return None
def authuntication(UserName:str,password:str):
    user = get_user(UserName)
    if not user:
        return False
    if not verify_password(password,user.UserPassword):
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

