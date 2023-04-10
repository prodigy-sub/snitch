from datetime import datetime

from fastapi import FastAPI

from app.models import mongodb
from app.models.article import NaverNewsArticleModel

app = FastAPI()


@app.get("/")
async def my_first_get():
    article = NaverNewsArticleModel(
        title="기사 제목",
        published_datetime=datetime.now(),
        journalist="기자 이름",
        press="언론사 이름",
        content="기사 내용",
        url="https://기사주소",
    )
    await mongodb.engine.save(article)
    return {"message": "Hello World"}


@app.on_event("startup")
def startup_event():
    mongodb.connect()


@app.on_event("shutdown")
def shutdown_event():
    mongodb.close()
