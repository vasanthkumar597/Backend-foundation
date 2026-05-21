from fastapi import APIRouter
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from sqlalchemy.orm import Session
from fastapi import Depends
from app.models.user import User
from app.schemas.user_schema import UserLogin
from app.core.security import verify_password
from app.core.security import create_access_token
from app.core.security import verify_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import get_current_user
from app.database import get_db
from app.core.security import HTTPException,status
from app.core.security import create_access_token,create_refresh_token

router=APIRouter()

@router.post("/register")
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    allowed_roles = [
    "founder",
    "investor",
    "freelancer"
    ]

    if user.role not in allowed_roles:

        return {
           "message": "Invalid role"
        }


    hashed_password=hash_password(user.password)

    new_user = User(
    email=user.email,
    password_hash=hashed_password,
    role=user.role,
    is_verified=False
)
    db.add(new_user)
    
    db.commit()

    db.refresh(new_user)

    verification_token=create_access_token(
        data={
            "sub":new_user.email
        }
    )

    return{
        "message":"user registered successfully",
         "id": new_user.id,
        "email":user.email,
        "verification_token":verification_token
    }


@router.post("/login")
def login_user(login_data:OAuth2PasswordRequestForm=Depends(),
               db:Session=Depends(get_db)):
    
    db_user=db.query(User).filter(User.email==login_data.username).first()

    if not db_user:
        return{
            "message":"Invalid email!!"
        }
    
    if not verify_password(login_data.password,db_user.password_hash):
        return{
            "message":"Invalid password"

        }
    
    if not db_user.is_verified:

        return {
        "message": "Please verify your email first"
    }
    

    access_token=create_access_token(
       data={
          "sub":db_user.email
        }
    ) 
    refresh_token=create_refresh_token(
        data={
            "sub":db_user.email
        }
    )

    return {
        "access_token":access_token,
        "refresh_token":refresh_token,
        "token_type":"bearer"
    }

@router.post("/refresh")
def refresh_token(refreh_token:str):
    payload=verify_token(refreh_token)
    if payload.get("type")!="refresh":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    email=payload.get("sub")

    new_access_token = create_access_token(
        data={
            "sub":email
        }
    )
    return {
        "access_token":new_access_token,
        "token_type":"bearer"
    }

@router.get("/protected")
def protected_route(current_user:User=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied")
   
    return {
        "message":"Access granted",
        "email":current_user.email
    }

@router.get("/users/me")
def get_me(
    current_user:User=Depends(get_current_user)):

    return {
        "id":current_user.id,
        "email":current_user.email,
        "role":current_user.role
    }

@router.get("/all-users")
def get_all_users(
    current_user:User=Depends(get_current_user),
    db:Session=Depends(get_db)
):
    users=db.query(User).all()

    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Access denied")

    return users

@router.post("/forgot-password")
def forgot_password(email:str,
                    db:Session=Depends(get_db)):
    db_user=db.query(User).filter(
        User.email==email
    ).first()

    if not db_user:

        return {
            "message":"Emial not found"
        }
    reset_token=create_access_token(
        data={
            "sub":db_user.email
        }
    )
    return {
        "reset_token":reset_token
    }

@router.post("/reset-password")
def reset_password(
    token:str,
    new_password:str,
    db:Session=Depends(get_db)
):
    payload=verify_token(token)
    email=payload.get("sub")

    db_user=db.query(User).filter(
        User.email==email
    ).first()
    
    hashed_password=hash_password(new_password)
    db_user.password_hash=hashed_password

    db.commit()

    return {
        "message":"password reset successfull"
    }

@router.post("/verify-email")
def verify_email(
    token:str,
    db:Session=Depends(get_db)):
    
    payload=verify_token(token)
    email=payload.get("sub")
    db_user=db.query(User).filter(
        User.email==email).first()
    
    db_user.is_verified=True

    db.commit()

    return {
        "message":"Email verified successfully"
    }

    
    