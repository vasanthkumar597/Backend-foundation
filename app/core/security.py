from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException,status
from app.models.user import User
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

SECRET_KEY="mysecretkey"

ALGORITHM="HS256"

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

password_context= CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

oauth2_scheme=OAuth2PasswordBearer(
    tokenUrl="login"

)

def hash_password(password:str):
    return password_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return password_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({
        "exp":expire
    })

    to_encode.update({
    "type": "access"
    })
    encoded_jwt = jwt.encode(
    to_encode,
    SECRET_KEY,
    algorithm=ALGORITHM
    )

    return encoded_jwt

def create_refresh_token(data:dict):
    to_encode=data.copy()

    expire=datetime.utcnow()+timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    to_encode.update({
        "exp":expire
    })

    to_encode.update({
        "type":"refresh"
    })

    refresh_token=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return refresh_token
def verify_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             detail="Invalid token")

def get_current_user(token:str=Depends(oauth2_scheme),
                     db:Session=Depends(get_db)):
    payload=verify_token(token)
    email=payload.get("sub")
    user=db.query(User).filter(User.email==email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="user not found")
    return user