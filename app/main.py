from fastapi import FastAPI
app = FastAPI(title="Notes API")


@app.get("/")

def root():
    return {"message": "Notes API running"}
