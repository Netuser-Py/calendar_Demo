from datetime import datetime, timedelta
import pytz

def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0

def it_is_now():
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(now)

def set_a_date():
    startDate = datetime(2019, 12, 1) + timedelta(seconds = -1)
    print(is_dst(startDate, timezone="America/Winnipeg"))
    lastSart = datetime(2019, 12, 15) + timedelta(seconds = -1)
    print(lastSart)
    print(is_dst(lastSart, timezone="America/Winnipeg"))

    # endT = "2019-10-01T00:00:00-06:00" # ends before (DST?)
    tempDT = pytz.timezone("America/Winnipeg").localize(startDate)
    fmt = '%Y-%m-%dT%H:%M:%S%z'   
    startDate = tempDT.strftime(fmt)
    print(startDate)

    tempDT = pytz.timezone("America/Winnipeg").localize(lastSart)
    fmt = '%Y-%m-%dT%H:%M:%S%z'    
    lastSart = tempDT.strftime(fmt)
    print(lastSart)

    print("Report for events from: " + str(startDate) + " to " + lastSart + "\n") 
    return

def main():
    set_a_date()
    return

if __name__ == '__main__':
    # test()
    main()