import pytest
import os
import tempfile
from page_loader import download


@pytest.fixture
def download_link():
    return 'http://test.com/example'


@pytest.fixture
def expected_name():
    return 'test-com-example.html'


def test_download_path(requests_mock, download_link, tmp_path, expected_name):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(download_link, text='<p>example</p>')
    assertion_result = os.path.join(tmp_path, expected_name)
    assert download(download_link, tmp_path) == assertion_result


def test_request_with_mock(requests_mock, download_link, tmp_path):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get(download_link, text='<p>example</p>')
    assertion_result = '<p>example</p>'
    downloaded_file_path = download(download_link, tmp_path)
    with open(downloaded_file_path, 'r') as d_file:
        downloaded_file = d_file.read()
    assert downloaded_file == assertion_result
