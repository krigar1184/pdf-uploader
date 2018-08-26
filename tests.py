import pytest
from app import make_app
from service import upload


@pytest.fixture
def app():
    return make_app('test.db')


@pytest.fixture
def file_to_upload(request):
    f = open('./tests/files/sicp.pdf', 'rb')
    request.addfinalizer(lambda: f.close())

    yield f


@pytest.mark.gen_test
def test_upload_file(file_to_upload):
    upload(file_to_upload.read())
