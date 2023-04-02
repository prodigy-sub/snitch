from bs4 import BeautifulSoup
from snitch.scraper import BaseScraper, NaverNewsScraper


def test_url2soup():
    url = "https://chimhaha.net/"
    base_scraper = BaseScraper(url)
    soup = base_scraper.url2soup(url)
    assert isinstance(soup, BeautifulSoup)

def test_scrap():
    naver_news_scraper = NaverNewsScraper()
    articles = naver_news_scraper.scrap("국민은행")
    assert isinstance(articles, list)
    assert len(articles) > 0
    assert articles[0].startswith("https://n.news.naver.com/")
    
    
# TODO: should be fixed
def test_get_articles():
    assert True
