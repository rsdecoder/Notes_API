from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import engine
from .models import Base, User
from .dependencies import get_db, get_current_user
from . import schemas, crud

app = FastAPI(title="Notes API")

Base.metadata.create_all(bind=engine)

# ***************** /NOTES *******************************
@app.post("/notes", response_model = schemas.NoteResponse)
def create_note(
        note: schemas.NoteCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return crud.create_note(
        db,
        title= note.title,
        content = note.content,
        user_id = current_user.id
    )


@app.get("/notes", response_model= list[schemas.NoteResponse])
def get_notes(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return crud.get_user_notes(db, current_user.id)

# ***************** /LOGIN *******************************
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

# ***************** /REGISTER *******************************
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

