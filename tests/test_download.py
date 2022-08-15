import pytest
import os
import tempfile
from page_loader import download


@pytest.fixture
def download_link():
    path_to_link = os.path.join('tests', 'fixtures', 'download_link.txt')
    with open(path_to_link, 'r') as link:
        result = link.read()
    return result


@pytest.fixture
def expected_name():
    path_to_result = os.path.join('tests', 'fixtures', 'expected_name.txt')
    with open(path_to_result, 'r') as name:
        result = name.read()
    return result


def test_download_path(download_link, expected_name):
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_path = tmp_dir.name
    assertion_result = os.path.join(tmp_path, expected_name)
    assert download(download_link, tmp_path) == assertion_result
