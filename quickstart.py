from __future__ import print_function
import pytz
from pytz import timezone
from datetime import datetime, timedelta
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv, json, sys
import pickle
import os.path

import UTC_stuff

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def list_events():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    # default is: calendarId='primary'
    # get id from calendar properties: calendarId='nhl_28_%57innipeg+%4aets#sports@group.v.calendar.google.com'
    #

    start_date = now
    fmt = '%Y-%m-%d %H:%M' 
    events_result = service.events().list(calendarId='nhl_28_%57innipeg+%4aets#sports@group.v.calendar.google.com', 
                                        timeMin=start_date,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    #events now contains the buffer
    print(events)

    # list each event in events
    for event in events:        
        print(event)
        for item in event:
            print(item, ': ', event[item])

        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    
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
def main():
    list_cals()
    list_events()
    return

if __name__ == '__main__':
    main()
    
    