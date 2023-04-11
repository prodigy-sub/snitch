from datetime import datetime


class NaverNewsArticle:
    def __init__(self, title: str, datetime: datetime, journalist: str, press: str, content: str, url: str):
        self.title: str = title
        self.datetime: datetime = datetime
        self.journalist: str = journalist
        self.press: str = press
        self.content: str = content
        self.url: str = url

    def __str__(self) -> str:
        return f"""
title: {self.title} 
datetime: {self.datetime}
journalist: {self.journalist}
press: {self.press}
content: {self.content}
url: {self.url}
    """
