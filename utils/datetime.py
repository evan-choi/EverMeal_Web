# coding: utf-8

from datetime import datetime
import time
#import pytz

class datetimeEx:
    @staticmethod
    def now():
        #tz = pytz.timezone('Asia/Seoul')  # <- put your local timezone here
        #d = datetime.now(tz)  # the current time in your local timezone
        #return datetimeEx.totimestamp(datetime(2016, 7, 16))
        return time.time()


    @staticmethod
    def totimestamp(dt):
        epoch = datetime(1970, 1, 1)
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
