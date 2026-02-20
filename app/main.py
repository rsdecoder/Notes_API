from datetime import timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from .database import engine
from .models import Base, User
from .dependencies import get_db, get_current_user
from . import schemas, crud
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notes API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
    authenticated_user = crud.authenticate_user(db, str(user.email), user.password)

    if not authenticated_user:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials"
        )

    access_token = create_access_token(
        data= {"sub": authenticated_user.email},
        expires_delta= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token,
            "token_type" : "bearer"}

# Authorize token with a different endpoint
@app.post("/session")
async def session(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    authenticated_user = crud.authenticate_user(db, str(form_data.username), form_data.password)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )

    access_token = create_access_token(
        data={"sub": authenticated_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token,
            "token_type": "bearer"}

# ***************** /REGISTER *******************************
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_email(db, str(user.email))
    if existing_user:
        raise HTTPException(
            status_code= status.HTTP_400_BAD_REQUEST,
            detail= "EMAIL already exists"
        )
    return crud.create_user(db, user)


# *************** PUT ********/NOTES/{NOTE_ID} ****************

@app.put("/notes/{note_id}", response_model = schemas.NoteResponse)
def update_note(
        note_id: int,
        note_data: schemas.NoteUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)

):
    note = crud.get_note_by_id(db, note_id)

    if not note or note.owner_id != current_user.id:
        raise HTTPException(status_code = 404, detail = "Note not found")

    return crud.update_note(
        db,
        note,
        note_data.title,
        note_data.content
    )

# **************** DELETE /NOTES/{note_id} **************************

@app.delete("/notes/{note_id}")
def delete_note(
        note_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    note = crud.get_note_by_id(db, note_id)

    if not note or note.owner_id != current_user.id:
        raise HTTPException(status_code = 404, detail="Note not found")

    crud.delete_note(db, note)
    return {"message": "Note deleted" }


@app.get("/")
def root():
    return {"message": "Notes API running"}

