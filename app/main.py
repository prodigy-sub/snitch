from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def my_first_get():
    return {"message": "Hello World"}