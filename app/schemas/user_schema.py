from pydantic import BaseModel,validator #validation

class UserCreate(BaseModel):
    email:str
    password:str
    role:str="freelancer"
@validator("email")
def validate_email(cls, value):

        if "@" not in value:

            raise ValueError("Enter valid email")

        return value

@validator("password")
def validate_password(cls, value):

        if len(value) < 6:

            raise ValueError(
                "Password must contain at least 6 characters"
            )

        return value

class UserLogin(BaseModel):
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    email:str

class Config:
    from_attributes = True