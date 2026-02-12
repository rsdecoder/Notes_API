from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password, verify_password
from .models import Note

" ************************* CREATE NOTE *************************"
def create_note(db, title: str, content: str, user_id: int):
    note = Note(
        title = title,
        content = content,
        owner_id = user_id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

" ************************* GET NOTE BY ID *************************"
def get_note_by_id(db, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()



" ************************* UPDATE NOTE *************************"
def update_note(db, note: Note, title: str, content: str):
    note.title = title
    note.content = content
    db.commit()
    db.refresh(note)
    return note


" ************************* DELETE NOTE *************************"
def delete_note(db, note: Note):
    db.delete(note)
    db.commit()

" ************************* GET ALL USER NOTES BY USER ID ************************* "
def get_user_notes(db, user_id: int):
    return db.query(Note).filter(Note.owner_id == user_id).all()


"************************* GET USERS BY EMAIL *************************"
def get_user_by_email(db: Session, email:str):
    return db.query(models.User).filter(models.User.email == email).first()


" ************************* CREATE USER ************************* "
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user  = models.User(
        email = user.email,
        hashed_password = hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

""" ************************* AUTHENTICATE USER *************************"""
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        return None
    return user



