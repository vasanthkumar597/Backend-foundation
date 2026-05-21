from sqlalchemy import Column, Integer, String,Boolean
from app.database import Base


class User(Base):#alembic revision --autogenerate -m "create tablename table"
    #to update -- alembic upgrade head
    __tablename__ = "users"

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String, unique=True,nullable=True)
    password_hash= Column(String,nullable=False)
    role=Column(String,default="freelancer")
    is_verified=Column(Boolean,default=False)
    


    

    