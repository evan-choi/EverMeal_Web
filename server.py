# coding: utf-8
import hashlib

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=8080)
else:
    app = create_app()
