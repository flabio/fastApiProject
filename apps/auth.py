from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

JWT_SECRET = "berer"
ALGORITHM = "HS256"
from datetime import datetime, timedelta

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def create_access_token(user):
    try:
        
        claims = {
            "user_id": user.id,
            "rol_name": user.rol_name,
            "church_id": user.church_id,
            "church_name": user.church_name,
            "detachment_name":user.detachment_name,
            "sub_detachment_id":user.sub_detachment_id,
            "user_active": user.user_active,
            "exp": datetime.utcnow() + timedelta(minutes=120),
        }
        
        return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=ALGORITHM)
        
    except Exception as ex:
        print(str(ex))
        raise ex


    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_token(token):
    try:
        payload = jwt.decode(token, key=JWT_SECRET)
        return payload
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not authenticated")

def check_active(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    active = payload.get("user_active")
    if active:
        return payload
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please activate your Account first",
            headers={"WWW-Authenticate": "Bearer"},
        )

def check_admin(payload: dict = Depends(check_active)):
    role = payload.get("rol_name")
    if role == "admin" :
        return payload
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only admins can access this route",
            headers={"WWW-Authenticate": "Bearer"},
        )
def check_comandant(payload:dict=Depends(check_active)):
    role = payload.get("rol_name")
    if role == "comandante" or role == "admin":
        return payload
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only comandants can access this route",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
