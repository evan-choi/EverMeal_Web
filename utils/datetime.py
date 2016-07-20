import datetime
import time


class datetimeEx:
    @staticmethod
    def intFromString(str):
        date = datetime.datetime.strptime(str, "%Y-%m-%d %H:%M:%S.%f")

        return time.mktime(date.timetuple())
