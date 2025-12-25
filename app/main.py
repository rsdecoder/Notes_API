from fastapi import FastAPI
from .database import engine
from .models import Base

app = FastAPI(title="Notes API")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Notes API running"}

