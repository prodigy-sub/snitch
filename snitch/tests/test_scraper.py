from datetime import datetime

import pytest
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


@pytest.fixture(scope="module")
def setup_naver_news_scraper():
    yield NaverNewsScraper()


@pytest.fixture(scope="module")
def test_article_html(setup_naver_news_scraper):
    test_url = "https://n.news.naver.com/mnews/article/003/0011789550?sid=101"
    naver_news_scraper = setup_naver_news_scraper
    article_html = naver_news_scraper.url2soup(test_url)
    yield article_html


def test_get_title(test_article_html, setup_naver_news_scraper):
    naver_news_scraper = setup_naver_news_scraper
    assert naver_news_scraper._get_title(test_article_html) == '삼성전자, 1분기 영업익 6000억…"이례적 감산"(종합)'


def test_get_press(test_article_html, setup_naver_news_scraper):
    naver_news_scraper = setup_naver_news_scraper
    assert naver_news_scraper._get_press(test_article_html) == "뉴시스"


def test_get_journalist(test_article_html, setup_naver_news_scraper):
    naver_news_scraper = setup_naver_news_scraper
    assert naver_news_scraper._get_journalist(test_article_html) == "이인준 기자"


def test_get_datetime(test_article_html, setup_naver_news_scraper):
    naver_news_scraper = setup_naver_news_scraper
    assert naver_news_scraper._get_datetime(test_article_html) == datetime(2023, 4, 7, 10, 6)
