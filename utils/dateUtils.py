# coding: utf-8

from datetime import datetime
from pytz import timezone

fmt = '%Y-%m-%d %H:%M:%S %Z%z'
tZone = timezone("Asia/Seoul")

class datetimeEx:
    @staticmethod
    def localize(dt):
        return tZone.localize(dt)

    @staticmethod
    def now():
        n = tZone.localize(datetime.now())
        return datetimeEx.totimestamp(n)


    @staticmethod
    def totimestamp(dt):
        epoch = tZone.localize(datetime(1970, 1, 1))
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10**6) / 10**6

    @staticmethod
    def toDatetime(timestamp):
        return datetimeEx.localize(datetime.fromtimestamp(timestamp))
