import pytest
import os
import tempfile
from page_loader import download

@pytest.fixture
def download_url():
    return 'http://test.com/example'


@pytest.fixture
def img_url():
    return "https://test.com/img/image.png"


@pytest.fixture
def image_html():
    path_to_html = os.path.join('tests', 'fixtures', 'img_page.html')
    with open(path_to_html, 'r') as f:
        html = f.read()
    return html


def test_image_download_path(requests_mock, download_url, img_url, image_html):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    test_img_path = os.path.join('tests', 'fixtures', 'img', 'image.png')
    requests_mock.get(download_url, text=image_html)
    with open(test_img_path, 'r') as t_img:
        test_img = t_img
    requests_mock.get(img_url, body=test_img)
    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    downloaded_img_path = os.path.join(page_dir, 'test-com-img-image.png')
    is_img_downloaded = os.path.exists(downloaded_img_path)
    assert is_img_downloaded


def test_html_changing(requests_mock, download_url, img_url, image_html):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name

    test_img_path = os.path.join('tests', 'fixtures', 'img', 'image.png')
    requests_mock.get(download_url, text=image_html)
    with open(test_img_path, 'r') as t_img:
        test_img = t_img
    requests_mock.get(img_url, body=test_img)

    downloaded_page = download(download_url, tmp_path)
    page_dir = os.path.splitext(downloaded_page)[0] + '_files'
    page_dir_name = os.path.split(page_dir)[1]

    downloaded_img_path = os.path.join(page_dir, 'test-com-img-image.png')
    local_name = os.path.split(downloaded_img_path)[1]
    local_tag_path = os.path.join(page_dir_name, local_name)

    with open(downloaded_page, 'r') as d_html:
        html = d_html.read()

    assert local_tag_path in html
