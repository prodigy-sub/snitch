from datetime import datetime
from bs4 import BeautifulSoup
import requests
from typing import List, Final

HEADERS: Final[str] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

# TODO: study singleton pattern and apply it to these classes
class BaseScraper:
    def __init__(self, home_url):
        self.home_url = home_url

    def url2soup(self, url: str, parser: str = "lxml", timeout: int = 60 * 2) -> BeautifulSoup:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        html = response.text
        return BeautifulSoup(html, parser)


class NaverNewsScraper(BaseScraper):
    def __init__(self, home_url="https://search.naver.com/search.naver"):
        super().__init__(home_url)


    def scrap(self, keyword: str, start_date: datetime = None, end_date: datetime = None):
        search_url = self.home_url + f"?where=news&query={keyword}&sort={1}" # sort 0: 관련도순, 1: 최신순, 2: 오래된순
        search_html = self.url2soup(search_url)
        return self.get_articles(search_html)
    
    
    def get_articles(self, search_html: BeautifulSoup) -> List[str]:
        """
        Return a list of article urls
        """
        articles = search_html.select("div.info_group > a.info:not(.press)")
        return [article["href"] for article in articles]