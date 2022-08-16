import pytest
import os
import tempfile
import re
from base64 import b64encode
from page_loader import download


@pytest.fixture
def download_url():
    return 'http://test.com/example'


@pytest.fixture
def get_img_url():
    return "https://test.com/img/image.png"


@pytest.fixture
def expected_name():
    return 'test-com-example.html'


@pytest.fixture
def test_image_html():
    path_to_html = os.path.join('tests', 'fixtures', 'img_page.html')
    with open(path_to_html, 'r') as f:
        html = f.read()
    return html


def test_download_path(requests_mock, download_url, expected_name):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(download_url, text='<p>example</p>')
    assertion_result = os.path.join(tmp_path, expected_name)
    assert download(download_url, tmp_path) == assertion_result


def test_request_with_mock(requests_mock, download_url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(download_url, text='<p>example</p>')
    assertion_result = '<p>example</p>'
    downloaded_file_path = download(download_url, tmp_path)
    with open(downloaded_file_path, 'r') as d_file:
        downloaded_file = d_file.read()
    minified_downloaded_file = re.sub(r"\s+|\n|\r|\s+$", '', downloaded_file)
    assert minified_downloaded_file == assertion_result


def test_image_download_path(requests_mock, download_url, get_img_url, test_image_html):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    test_img_path = os.path.join('tests', 'fixtures', 'img', 'image.png')
    requests_mock.get(download_url, text=test_image_html)
    with open(test_img_path, 'r') as t_img:
        test_img = t_img
    requests_mock.get(get_img_url, body=test_img)
    assertion_result = os.path.exists(test_img_path)
    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    downloaded_img_path = os.path.join(page_dir, 'assets', 'image.png')
    is_img_downloaded = os.path.exists(downloaded_img_path)
    assert is_img_downloaded == assertion_result


def test_html_changing(requests_mock, download_url, get_img_url, test_image_html):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    test_img_path = os.path.join('tests', 'fixtures', 'img', 'image.png')
    requests_mock.get(download_url, text=test_image_html)
    with open(test_img_path, 'r') as t_img:
        test_img = t_img
    requests_mock.get(get_img_url, body=test_img)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    page_dir_name = os.path.split(page_dir)[1]

    downloaded_img_path = os.path.join(page_dir, 'assets', 'image.png')
    local_name = os.path.split(downloaded_img_path)[1]
    local_tag_path = os.path.join(page_dir_name, 'assets', local_name)

    with open(downloaded_page, 'r') as d_html:
        html = d_html.read()

    assert local_tag_path in html
