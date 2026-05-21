from sqlalchemy import create_engine # connection b/w python & postgresql
from sqlalchemy.orm import sessionmaker,declarative_base # session to interact with database & #  base classes/models
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")

DATABASE_URL = os.getenv("DATABASE_URL") #address,username,password,port,dbname

engine=create_engine(DATABASE_URL)#connects the url to engine

SessionLocal=sessionmaker(bind=engine)#connect to specified engine/database

Base=declarative_base() #foundation dor databses and models

def get_db():
    db=SessionLocal()

    try:
        yield db
    
    finally:
        db.close()





