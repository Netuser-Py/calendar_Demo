import pytz
from pytz import timezone

from datetime import datetime

def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0




import time
from datetime import datetime, timedelta
from tzlocal import get_localzone

def to_local(dt):
    """From any timezone to local datetime - also cope with DST"""
    localtime = time.localtime()
    if localtime.tm_isdst:
        utctime = time.gmtime()
        hours_delta = timedelta(hours=(localtime.tm_hour - utctime.tm_hour))
        dt = dt - hours_delta

    return dt.replace(tzinfo=get_localzone())


if __name__ == '__main__':
    # Some examples
    print(is_dst()) # it is never DST in UTC
    print(datetime(2019, 11, 1) + timedelta(seconds = -1) )
    print(is_dst(datetime(2019, 11, 1), timezone="America/Winnipeg"))
    testDT = datetime(2019, 11, 1) + timedelta(seconds = -1) 
    testDT = timezone("America/Winnipeg").localize(datetime(2019, 11, 1) + timedelta(seconds = -1) )
    fmt = '%Y-%m-%dT%H:%M:%S%z'
    print(testDT.strftime(fmt))

    lastSart = datetime(2019, 12, 1) + timedelta(seconds = -1)
    print(lastSart)
    print(is_dst(lastSart, timezone="America/Winnipeg"))

    # print(pytz

    # test()
    # main()