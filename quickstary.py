from __future__ import print_function
import datetime
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
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    
    events_result = service.events().list(calendarId='primary', #timeMin=now,
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
            #print(str(i) + " " + start, event['summary'])
            print(str(i) )
            print(event)'''
        print(events)

def main():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))
 
    i = 0
    f=csv.writer(open('test.csv','w'))
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', singleEvents=False, maxResults=2500, pageToken=page_token).execute()
  
        for event in events['items']:
            i += 1
            #print(str(i) + " " + start, event['summary'])
            print(str(i) )
            #print(event)
            data = flatten_json(event)
            #data = event
            #print(data)   
            #print(data.keys())     
            f.writerow(data.keys())
            f.writerow(data.values())

        page_token = events.get('nextPageToken')
        if not page_token:
            break 

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
    main()
    
''' 
#return of service.events().list
{
  "kind": "calendar#events",
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