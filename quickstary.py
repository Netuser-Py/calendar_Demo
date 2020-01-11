from __future__ import print_function
import pytz
from pytz import timezone
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import csv, json, sys

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main1():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', # timeMin=now,
                                        singleEvents=True, maxResults=2500,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    print('Getting the upcoming ' + str(len(events)) + ' events')

    if not events:
        print('No upcoming events found.')
    else:
        '''i = 0
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            i += 1
            # print(str(i) + " " + start, event['summary'])
            print(str(i) )
            print(event)'''
        print(events)

def list_cals():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(calendar_list_entry['summary'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break



def is_dst(dt=None, timezone="UTC"):
    if dt is None:
        dt = datetime.utcnow()
    timezone = pytz.timezone(timezone)
    timezone_aware_date = timezone.localize(dt, is_dst=None)
    return timezone_aware_date.tzinfo._dst.seconds != 0

def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
 
    i = 0
    # f=csv.writer(open('test.csv','w',encoding="utf-8"))
    f = open('test.txt','w',encoding="utf-8") 
    f2 = open('skip.dat','w',encoding="utf-8") 
    f1 = open('test.json','w')
    page_token = None
    colors = service.colors().get().execute()
    # print(colors) # https://developers.google.com/calendar/v3/reference/colors/get
    
    # startT = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # startT = "2019-10-31T23:59:00-06:00" # Starts after (DST?)
    startDate = datetime(2019, 12, 1) + timedelta(seconds = -1)
    print(is_dst(startDate, timezone="America/Winnipeg"))
    lastSart = datetime(2019, 12, 15) + timedelta(seconds = -1)
    print(lastSart)
    print(is_dst(lastSart, timezone="America/Winnipeg"))

    # endT = "2019-10-01T00:00:00-06:00" # ends before (DST?)
    tempDT = timezone("America/Winnipeg").localize(startDate)
    fmt = '%Y-%m-%dT%H:%M:%S%z'   
    startDate = tempDT.strftime(fmt)
    print(startDate)

    tempDT = timezone("America/Winnipeg").localize(lastSart)
    fmt = '%Y-%m-%dT%H:%M:%S%z'    
    lastSart = tempDT.strftime(fmt)
    print(lastSart)

    f.write("Report for trips from: " + str(startDate) + " to " + lastSart + "\n") 

    while True:
        events = service.events().list(calendarId='goorderly@gmail.com', singleEvents=True, timeMin=startDate,
                                        # timeMax=endT,
                                        maxResults=2500, pageToken=page_token, orderBy='startTime').execute()
        # print(events)
        
        for event in events['items']:
            i += 1
            # print(str(i) + " " + start, event['summary'])
            # print(str(i) + " " + event['colorId'])
            # print(str(i))
            # print(event)
            data = flatten_json(event)            
            # list:
            #   summary 
            #   description
            #   location
            #   colorId
            #   start__dateTime
            #   end__dateTime
            try:
                if data["start__dateTime"] > lastSart:
                    exit_now = True
                    break
            except:
                pass

            if str(data["kind"]) == "calendar#event":
                fld_list = ["id","summary", "description", "location", "colorId", "start__dateTime", 
                            "end__dateTime"]
                f.write("TripSeq =" + str(i) + "\n") 
                for item in fld_list:
                    # print(item + "=" + str(data[item]))    
                    # kind=calendar#event 
                    try:               
                        f.write(item + "=" + str(data[item]) + "\n")  
                        if item == "colorId":
                            id = data[item]
                            #print(data[item])
                            #print(colors.data[item])                      
                            
                            
                            
                            pass
                    except:
                        pass
            else: 
                for item in fld_list:  
                    f2.write(item + "=" + str(data[item]) + "\n")         
          
            # f1.write(json.dumps(data))

            # print(data.keys())     
            # f.writerow(data.keys())
            # f.writerow(data.values())

            # print(data["start__dateTime"])


        page_token = events.get('nextPageToken')
        if exit_now:
            break
        if not page_token:
            break 

# decode summary
# space delimited
# keys:
#   numberX  e.g. 2X
#   no 
#   Trips/Hrs  (disregard? seperate report?)
#   keywords: 
#       Escort
#       W/aide
#       W/
#       MPI
#       MTU
#       PT
#       WCB
#       call first
#       Call 1'st
#       CL
#       CLM
#       RTN
#       RT
#       return
#       collect
#       paid
#       pd
#       ck 
#       wife
#       EIA
#       last minute
#       Cancel last min
#       Cancelled
#       collect
#       pls

def decode_summary():
    return

def flatten_json(json):
    def process_value(keys, value, flattened):
        if isinstance(value, dict):
            for key in value.keys():
                process_value(keys + [key], value[key], flattened)
        elif isinstance(value, list):
            for idx, v in enumerate(value):
                process_value(keys + [str(idx)], v, flattened)
        else:
            flattened['__'.join(keys)] = value

    flattened = {}
    for key in json.keys():
        process_value([key], json[key], flattened)
    return flattened

if __name__ == '__main__':
    list_cals()
    #main()
    
''' 
# return of service.events().list
{
  "kind": "calendar# events",
  "etag": etag,
  "summary": string,
  "description": string,
  "updated": datetime,
  "timeZone": string,
  "accessRole": string,
  "defaultReminders": [
    {
      "method": string,
      "minutes": integer
    }
  ],
  "nextPageToken": string,
  "nextSyncToken": string,
  "items": [
    events Resource
  ]
}
'''