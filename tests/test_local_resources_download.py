import pytest
import os
import tempfile
import re
from page_loader import download


@pytest.fixture
def download_url():
    return 'https://test.com/example'


@pytest.fixture
def link_url():
    return "https://test.com/assets/style.css"


@pytest.fixture
def link_html():
    path_to_html = os.path.join('tests', 'fixtures', 'link_page.html')
    with open(path_to_html, 'r') as f:
        html = f.read()
    return html


@pytest.fixture
def script_url():
    return "https://test.com/packs/js/app.js"


@pytest.fixture
def script_html():
    path_to_html = os.path.join('tests', 'fixtures', 'script_page.html')
    with open(path_to_html, 'r') as f:
        html = f.read()
    return html


def test_link_download_path(requests_mock, download_url, link_html, link_url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    requests_mock.get(download_url, text=link_html)

    test_css_path = os.path.join('tests', 'fixtures', 'styles', 'style.css')
    with open(test_css_path, 'r') as t_css:
        test_css = t_css
    requests_mock.get(link_url, body=test_css)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'

    downloaded_css_path = os.path.join(page_dir, 'test-com-assets-style.css')
    is_css_downloaded = os.path.exists(downloaded_css_path)
    assert is_css_downloaded


def test_css_changing(requests_mock, download_url, link_url, link_html):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    test_css_path = os.path.join('tests', 'fixtures', 'styles', 'style.css')
    requests_mock.get(download_url, text=link_html)
    with open(test_css_path, 'r') as t_css:
        test_css = t_css
    requests_mock.get(link_url, body=test_css)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    page_dir_name = os.path.split(page_dir)[1]

    downloaded_css_path = os.path.join(page_dir, 'test-com-assets-style.css')
    local_name = os.path.split(downloaded_css_path)[1]
    local_tag_path = os.path.join(page_dir_name, local_name)

    with open(downloaded_page, 'r') as d_html:
        html = d_html.read()

    assert local_tag_path in html


def test_script_download_path(requests_mock, download_url, script_html, script_url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    requests_mock.get(download_url, text=script_html)

    test_js_path = os.path.join('tests', 'fixtures', 'scripts', 'app.js')
    with open(test_js_path, 'r') as t_js:
        test_js = t_js
    requests_mock.get(script_url, body=test_js)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'

    downloaded_js_path = os.path.join(page_dir, 'test-com-packs-js-app.js')
    is_js_downloaded = os.path.exists(downloaded_js_path)
    assert is_js_downloaded


def test_js_changing(requests_mock, download_url, script_html, script_url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    test_js_path = os.path.join('tests', 'fixtures', 'scripts', 'app.js')
    requests_mock.get(download_url, text=script_html)
    with open(test_js_path, 'r') as t_js:
        test_js = t_js
    requests_mock.get(script_url, body=test_js)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    page_dir_name = os.path.split(page_dir)[1]

    downloaded_js_path = os.path.join(page_dir, 'test-com-packs-js-app.js')
    local_name = os.path.split(downloaded_js_path)[1]
    local_tag_path = os.path.join(page_dir_name, local_name)

    with open(downloaded_page, 'r') as d_html:
        html = d_html.read()

    assert local_tag_path in html
