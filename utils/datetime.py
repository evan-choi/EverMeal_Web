# coding: utf-8

import datetime
import time


class datetimeEx:
    @staticmethod
    def intFromString(str):
        date = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")
        return time.mktime(date.timetuple())

    @staticmethod
    def now():
        #date = datetime.datetime.today()
        return 0#time.mktime(date.timetuple())
