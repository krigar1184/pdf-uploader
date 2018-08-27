import os
from sqlite3 import OperationalError
from uuid import uuid4
from datetime import date, datetime
from hashlib import sha1

from db import execute
from exceptions import AuthException
import settings


def register(username, email, password, confirm_password):
    assert sha1(password.encode('utf8')).hexdigest() == sha1(confirm_password.encode('utf8')).hexdigest()

    try:
        execute(
            'INSERT INTO users (username, email, password, dt_registered) VALUES (:username, :email, :password, :dt_registered);',
            username=username,
            email=email,
            password=sha1(password.encode('utf8')).hexdigest(),
            dt_registered=datetime.utcnow().isoformat(),
        )
    except OperationalError:
        raise


def login(username, password):
    user = execute(
        'SELECT * FROM users WHERE username = :username AND password = :password ',
        username=username,
        password=sha1(password.encode('utf8')).hexdigest(),
    )

    if not user:
        raise AuthException('User doesn\'t exist.')

    return user


def upload(file_body, file_name):
    upload_path = os.path.join(settings.STORAGE_PATH, date.today().isoformat())
    os.makedirs(upload_path, exist_ok=True)
    new_filename = _generate_file_name() + '.pdf'

    with open(os.path.join(upload_path, new_filename), 'wb') as f:
        f.write(file_body)


def _generate_file_name():
    return str(uuid4())
