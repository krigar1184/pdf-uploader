import os

from tornado import web
from views import MainHandler, LoginHandler, LogoutHandler, UploadHandler, FileHandler, RegistrationHandler
from db import execute


def make_app():
    execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username VARCHAR NOT NULL,
        email VARCHAR NOT NULL,
        password VARCHAR NOT NULL,
        dt_registered VARCHAR NOT NULL,
        dt_last_seen VARCHAR,
        CONSTRAINT username_uniq UNIQUE (username),
        CONSTRAINT email_uniq UNIQUE (email)
    )''')
    execute('''CREATE TABLE IF NOT EXISTS user_uploads (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        path VARCHAR NOT NULL,
        dt_uploaded VARCHAR NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    return web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/upload', UploadHandler),
        (r'/file', FileHandler),
        (r'/register', RegistrationHandler),
    ],
        cookie_secret='d9d5f45e7ff3f68c97f705a90412fb36',
        login_url='/login',
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=True,
    )
