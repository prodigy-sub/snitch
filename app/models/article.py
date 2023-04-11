from odmantic import Model
from datetime import datetime


class NaverNewsArticleModel(Model):
    title: str
    published_datetime: datetime
    journalist: str
    press: str
    content: str
    url: str

    class Config:
        collection = "navernews_articles"