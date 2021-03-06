# just for demo purposes 
# please play with this at your own risk

from datetime import datetime, timedelta
import pytz
import time
from tzlocal import get_localzone
import maya


def to_local(dt):
    """From any timezone to local datetime - also cope with DST"""
    dt1 = maya.parse(dt).datetime()
    localtime = time.localtime()
    if localtime.tm_isdst:
        utctime = time.gmtime()
        hours_delta = timedelta(hours=(localtime.tm_hour - utctime.tm_hour))
        dt1 = dt1 - hours_delta

    return dt1.replace(tzinfo=get_localzone())


def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0

def it_is_now():
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)
    return now

def set_a_date():
    startDate = datetime(2019, 10, 1) + timedelta(seconds = -1)
    print(is_dst(startDate, timezone="US/Mountain"))
    lastSart = datetime(2019, 10, 31) + timedelta(seconds = -1)
    print(lastSart)
    print(is_dst(lastSart, timezone="US/Mountain"))

    # endT = "2019-10-01T00:00:00-06:00" # ends before (DST?)
    tempDT = pytz.timezone("US/Mountain").localize(startDate)
    fmt = '%Y-%m-%dT%H:%M:%S%z'   
    startDate = tempDT.strftime(fmt)
    print(startDate)

    tempDT = pytz.timezone("US/Mountain").localize(lastSart)
    fmt = '%Y-%m-%dT%H:%M:%S%z'    
    lastSart = tempDT.strftime(fmt)
    print(lastSart)

    print("Report for events from: " + str(startDate) + " to " + lastSart + "\n") 
    return

# list all timezone valuse used in pytz.timezone
def list_timezones():  
    for tz in pytz.all_timezones:
        print(tz)
    return

def main():
    list_timezones()
    set_a_date()
    print(to_local(it_is_now()))

    return

if __name__ == '__main__':
    # test()
    main()