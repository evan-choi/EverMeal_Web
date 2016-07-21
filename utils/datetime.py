# coding: utf-8

from datetime import datetime
import time


class datetimeEx:
    @staticmethod
    def intFromString(str):
        date = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")
        return time.mktime(date.timetuple())


    @staticmethod
    def now():
        return datetimeEx.totimestamp(datetime.now())


    @staticmethod
    def totimestamp(dt):
        from datetime import datetime

        epoch = datetime(1970, 1, 1)
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
