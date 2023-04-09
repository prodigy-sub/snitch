from fastapi import FastAPI
from app.models import mongodb

app = FastAPI()


@app.get("/")
def my_first_get():
    return {"message": "Hello World"}


@app.on_event("startup")
def startup_event():
    mongodb.connect()


@app.on_event("shutdown")
def shutdown_event():
    mongodb.close()
