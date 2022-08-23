from urllib.error import HTTPError
import pytest
import os
import tempfile
from page_loader import download


@pytest.fixture
def correct_url():
    return 'http://test.com/example'


@pytest.fixture
def incorrect_url():
    return 'http://test.com/example/bla-bla-bla'


@pytest.fixture
def img_url():
    return "https://test.com/img/image.png"


@pytest.mark.parametrize(
    'url', (
        'https://test.com/400',
        'https://test.com/403',
        'https://test.com/404',
        'https://test.com/408',
        'https://test.com/410',
        )
    )
def test_http_client_exceptions(requests_mock, url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get('https://test.com/400', status_code=400)
    requests_mock.get('https://test.com/403', status_code=403)
    requests_mock.get('https://test.com/404', status_code=404)
    requests_mock.get('https://test.com/408', status_code=408)
    requests_mock.get('https://test.com/410', status_code=410)
    with pytest.raises(HTTPError):
        download(url, tmp_path)


@pytest.mark.parametrize(
    'url', (
        'https://test.com/500',
        'https://test.com/502',
        'https://test.com/503',
        'https://test.com/504',
        'https://test.com/505',
        )
    )
def test_http_server_exceptions(requests_mock, url):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    requests_mock.get('https://test.com/500', status_code=500)
    requests_mock.get('https://test.com/502', status_code=502)
    requests_mock.get('https://test.com/503', status_code=503)
    requests_mock.get('https://test.com/504', status_code=504)
    requests_mock.get('https://test.com/505', status_code=505)
    with pytest.raises(HTTPError):
        download(url, tmp_path)


@pytest.mark.parametrize('inexist_path', ('inexist_dir',))
def test_correct_url_invalid_path(requests_mock, correct_url, inexist_path):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    invalid_path = os.path.join(tmp_path, inexist_path)
    requests_mock.get(correct_url, text='<p>example</p>')
    with pytest.raises(FileNotFoundError):
        download(correct_url, invalid_path)


@pytest.mark.parametrize('inexist_path', ('inexist_dir',))
def test_incorrect_url_invalid_path(requests_mock, incorrect_url, inexist_path):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    invalid_path = os.path.join(tmp_path, inexist_path)
    requests_mock.get(incorrect_url, status_code=404)
    with pytest.raises(FileNotFoundError):
        download(incorrect_url, invalid_path)
