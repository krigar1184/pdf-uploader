#!/usr/bin/env python

from tornado import ioloop
from app import make_app


if __name__ == '__main__':
    app = make_app('main_db')
    app.listen(8888)

    print("Running on 127.0.0.1:8888...")
    ioloop.IOLoop.current().start()
