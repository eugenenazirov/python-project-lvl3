import pytest
import os
import tempfile
import re
from page_loader import download


@pytest.fixture
def download_url():
    return 'http://test.com/example'


@pytest.fixture
def expected_name():
    return 'test-com-example.html'


@pytest.fixture
def dwnld_url_with_html_end():
    return 'http://test.com/example.html'


@pytest.fixture
def exp_name_without_html_end():
    return 'test-com-example.html'


def test_download_path(requests_mock, download_url, expected_name):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(download_url, text='<p>example</p>')
    assertion_result = os.path.join(tmp_path, expected_name)
    assert download(download_url, tmp_path) == assertion_result


def test_path_with_html_end(
    requests_mock,
    dwnld_url_with_html_end,
    exp_name_without_html_end
):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(dwnld_url_with_html_end, text='<p>example</p>')
    assertion_result = os.path.join(tmp_path, exp_name_without_html_end)
    assert download(dwnld_url_with_html_end, tmp_path) == assertion_result


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
