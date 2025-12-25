from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import engine
from .models import Base
from .dependencies import get_db
from . import schemas, crud

app = FastAPI(title="Notes API")

Base.metadata.create_all(bind=engine)


@app.post("/login", response_model = schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials"
        )

    access_token = create_access_token(
        data= {"sub": authenticated_user.email},
        expires_delta= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token}







@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "EMAIL already exists"
        )
    return crud.create_user(db, user)





@app.get("/")
def root():
    return {"message": "Notes API running"}

