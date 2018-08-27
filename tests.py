import os
from datetime import date

import pytest
from faker import Faker

import settings
from db import execute, init as init_db
from app import make_app
from service import upload


@pytest.fixture
def app():
    init_db('test.db')
    return make_app()


@pytest.fixture
def file_to_upload(request):
    f = open('./tests/files/sicp.pdf', 'rb')
    request.addfinalizer(lambda: f.close())

    yield f


@pytest.fixture
def storage(tmpdir):
    yield tmpdir


@pytest.mark.gen_test
def test_upload_and_save_file(monkeypatch, app, storage, file_to_upload):
    fake_filename = Faker().uuid4()
    monkeypatch.setattr(settings, 'STORAGE_PATH', str(storage))
    monkeypatch.setattr('service._generate_file_name', lambda: fake_filename)
    upload(file_to_upload.read(), 'sicp.pdf')

    assert os.path.exists(os.path.join(
        storage,
        date.today().isoformat(),
        '{}.pdf'.format(fake_filename)))

    result = execute('SELECT COUNT(*) FROM user_uploads')
    assert result == 1
