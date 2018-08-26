import os

from tornado import web
from views import MainHandler, LoginHandler, LogoutHandler, UploadHandler, FileHandler
from db import execute


def make_app(db_path):
    execute('''CREATE TABLE IF NOT EXISTS users (
        username varchar,
        email varchar,
        password varchar,
        dt_registered,
        dt_last_seen
    )''', db_path)


    return web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/upload', UploadHandler),
        (r'/file', FileHandler),
    ],
        cookie_secret='d9d5f45e7ff3f68c97f705a90412fb36',
        login_url='/login',
        template_path=os.path.join(os.path.dirname(__file__), 'templates'),
        debug=True,
    )
