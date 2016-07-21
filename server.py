# coding: utf-8

from datetime import datetime
from app import create_app
import pytz


if __name__ == '__main__':
    app = create_app()

    tz = pytz.timezone('Asia/Seoul')  # <- put your local timezone here
    now = datetime.now(tz)  # the current time in your local timezone

    app.run(host='127.0.0.1', port=8080)
else:
    app = create_app()
