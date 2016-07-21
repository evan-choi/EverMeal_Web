# coding: utf-8

from datetime import datetime


class datetimeEx:
    @staticmethod
    def now():
        return datetimeEx.totimestamp(datetime.now())


    @staticmethod
    def totimestamp(dt):
        return str(dt)
        #epoch = datetime(1970, 1, 1)
        #td = dt - epoch
        #return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6
