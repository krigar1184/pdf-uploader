#!/usr/bin/env python

from tornado import ioloop
from app import make_app
from db import init as init_db


if __name__ == '__main__':
    init_db(db_path='main.db')
    app = make_app()
    app.listen(8888)

    print("Running on 127.0.0.1:8888...")
    ioloop.IOLoop.current().start()
