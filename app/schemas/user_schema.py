from pydantic import BaseModel,EmailStr,Field  #validation

class UserCreate(BaseModel):
    email:EmailStr
    password:str = Field(min_length=6,max_length=20)
    role:str="freelancer"

class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr

class Config:
    from_attributes = True