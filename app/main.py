from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def first_get():
    return {"message": "Hello World"}