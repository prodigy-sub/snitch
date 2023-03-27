from datetime import datetime


class NaverNews:
    def __init__(self, title, content, date, press, url):
        self.title: str = title
        self.content: str = content
        self.date: datetime = date
        self.press: str = press
        self.url: str = url

    def __str__(self) -> str:
        return f"Title: {self.title}, press: {self.press}, date: {self.date}, url: {self.url}"
