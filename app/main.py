from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.logging_config import logger
from app.routes.auth import router as auth_router

app = FastAPI()
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def home():
    return {"message":"Backend Running"}

@app.get("/health")
def health():
    logger.info("Health API called")
    return {"status":"healthy"}

@app.get("/version")
def version():
    return {"version":"1.0.0"}

