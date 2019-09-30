#!/usr/bin/env python

import datetime
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

CREDENTIALS_FILE = 'api_secrets.json'

def get_calendar_service():
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
               CREDENTIALS_FILE, SCOPES)
           creds = flow.run_local_server(port=0)

       # Save the credentials for the next run
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)

   service = build('calendar', 'v3', credentials=creds)
   return service


def choose_calendar():
    service = get_calendar_service()
    # Call the Calendar API
    print('Getting list of calendars\n')
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    if not calendars:
        print('No calendars found.')
        sys.exit()
    print("Choose a Calendar:")
    opt = 1
    for c in calendars:
        print("%d - %s" %(opt, c["summary"]))
        opt += 1
    choice = input("Choice: ")
    return calendars[int(choice)-1]["id"]


def show_cal_events(calendarID):
   service = get_calendar_service()
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   print('Getting List of events:\n')
   events_result = service.events().list(
       calendarId=calendarID, timeMin=now,
       maxResults=100, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])
   if not events:
       print('No upcoming events found.')
   for event in events:
       eventstart = event['start'].get('dateTime', event['start'].get('date'))
       eventend = event['end'].get('dateTime', event['end'].get('date'))
       print("Event: %s" % event["summary"])
       print("Event Description: %s" % event["description"])
       print("Event Start: %s" % eventstart)
       print("Event End: %s" % eventend)
       print("Event Created: %s" % event["created"])
       print("Event Updated: %s" % event["updated"])
       print("Event Creator: %s" % event["creator"]["email"])
       print("\n===\n")


def main():
    c = choose_calendar()
    show_cal_events(c)


if __name__ == '__main__':
    main()
