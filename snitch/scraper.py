from datetime import datetime
from bs4 import BeautifulSoup
import requests
from typing import List, Final, Dict
from snitch.scraped_data import NaverNewsArticle


HEADERS: Final[str] = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
}

# TODO: study singleton pattern and apply it to these classes
class BaseScraper:
    def __init__(self, home_url):
        self.home_url = home_url

    # TODO: use coroutine
    def url2soup(self, url: str, parser: str = "lxml", timeout: int = 60 * 2) -> BeautifulSoup:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        html = response.text
        return BeautifulSoup(html, parser)


class NaverNewsScraper(BaseScraper):
    def __init__(self, home_url="https://search.naver.com/search.naver"):
        super().__init__(home_url)


    def scrap(self, keyword: str, start_date: datetime = None, end_date: datetime = None) -> List[NaverNewsArticle]:
        search_url = self.home_url + f"?where=news&query={keyword}&sort={1}" # sort 0: 관련도순, 1: 최신순, 2: 오래된순
        search_html = self.url2soup(search_url)
        article_urls = self._get_article_urls(search_html)
        return [self._get_article_infos(article_url) for article_url in article_urls]
    
    
    def _get_article_urls(self, search_html: BeautifulSoup) -> List[str]:
        """
        Return a list of article urls
        """
        articles = search_html.select("div.info_group > a.info:not(.press)")
        return [article["href"] for article in articles]
    
    # TODO : use coroutine
    def _get_article_infos(self, article_url: str) -> NaverNewsArticle:
        article_html = self.url2soup(article_url)
        
        title = self._get_title(article_html)
        article_content = self._get_article_content(article_html)
        press = self._get_press(article_html)
        journalist = self._get_journalist(article_html)
        article_datetime = self._get_datetime(article_html)
        
        return NaverNewsArticle(title, article_datetime, journalist, press, article_content, article_url)
    
    def _get_title(self, article_html: BeautifulSoup) -> str:
        title = article_html.select_one("#title_area > span").string
        # TODO: use custom exception (or anything more specific)
        if title.strip() == "":
            raise Exception("No title")
        
        return title
    
    def _get_press(self, article_html: BeautifulSoup) -> str:
        press = article_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")["title"]
        # TODO: use custom exception (or anything more specific)
        if press.strip() == "":
            raise Exception("No press")
        
        return press
    
    def _get_journalist(self, article_html: BeautifulSoup) -> str:
        journalist = article_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_journalist > a > em").string
        if journalist.strip() == "":
            raise Exception("No journalist")
        
        return journalist
    
    def _get_datetime(self, article_html: BeautifulSoup) -> datetime:
        date_string = article_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span").string
        date_string = date_string.replace("오후", "PM").replace("오전", "AM")
        return datetime.strptime(date_string, '%Y.%m.%d. %p %I:%M')
    
    def _get_article_content(self, article_html: BeautifulSoup) -> str:
        content = ""
        article_content_html = article_html.select_one("#dic_area")
        for element in article_content_html:
            if element.__class__.__name__ == "NavigableString":
                if element.string.strip() != "":
                    content += element.string.strip() + "\n"
        
        if content.strip() == "":
            raise Exception("No content")
                    
        return content