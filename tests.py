import os
from datetime import date, datetime
from hashlib import sha1

import pytest
from faker import Faker

import settings
from db import execute, init as init_db
from app import make_app
from service import upload, save_user_upload


@pytest.fixture
def app(request, autouse=True):
    request.addfinalizer(lambda: os.remove('test.db'))
    init_db('test.db')

    return make_app()


@pytest.fixture
def file_to_upload(request):
    f = open('./tests/files/sicp.pdf', 'rb')
    request.addfinalizer(lambda: f.close())

    yield f


@pytest.fixture
def user():
    execute(
        '''INSERT INTO users (username, email, password, dt_registered) VALUES (
            :username,
            :email,
            :password,
            :dt_registered
        )''',
        username='test_user',
        email='test@example.com',
        password=sha1(str(123).encode('utf8')).hexdigest(),
        dt_registered=datetime.now(),
    )

    return execute('SELECT * FROM users LIMIT 1')[0]


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


@pytest.mark.gen_test
def test_save_user_file(app, user):
    save_user_upload(user, '/tmp/test_path')

    result = execute('SELECT COUNT(*) AS count FROM user_uploads')
    assert result[0]['count'] == 1
