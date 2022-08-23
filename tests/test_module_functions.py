import pytest
from page_loader import pl
from bs4 import BeautifulSoup


@pytest.fixture
def html():
    return '<p>example</p>'


@pytest.fixture
def url():
    return 'http://test.com/example'


def test_headers():
    assert all((pl.headers, isinstance(pl.headers, dict)))


def test_make_soup(html):
    soup = pl.make_soup(html)
    result = all((soup, isinstance(soup, BeautifulSoup)))
    assert result


def test_get_html_page(requests_mock, url, html):
    requests_mock.get(url, text=html)
    text = pl.get_html_page(url)
    result = all((text, isinstance(text, str)))
    assert result


def test_get_tags(html):
    soup = pl.make_soup(html)
    tags = pl.get_tags(soup, 'p')
    result = all((tags, isinstance(tags, list)))
    assert result
