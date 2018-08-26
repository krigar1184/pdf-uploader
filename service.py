import os
from datetime import date

from db import execute
from hashlib import sha1


def login(username, password):
    user = execute(
        'SELECT 1 FROM users WHERE username = ? AND password = ? ',
        username,
        sha1(password.encode('utf8').hexdigest()),
    )

    return user


def upload(file_body):
    upload_path = os.path.join('./storage', date.today().isoformat())
