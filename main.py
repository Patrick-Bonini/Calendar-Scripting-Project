import datetime as dt
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main ():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    #Lists upcoming events
    """ try:
        service = build("calendar", "v3", credentials=creds)

        now = dt.datetime.now().isoformat() + 'Z'

        event_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy="startTime").execute()
        events = event_result.get('items', [])

        if not events:
            print("No upcoming events")
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
    except HttpError as error:
        print("Error occurred:", error) """
    
    try:
        service = build("calendar", "v3", credentials=creds)

        event = {
            'summary': 'Event name',
            'location': 'Event location',
            'Description': 'Event details',
            'colorId': 6,
            'start': {
                'dateTime': '2023-07-25T09:00:00-04:00',
                'timeZone': 'Europe/Vienna'
            },
            'end': {
                'dateTime': '2023-07-25T17:00:00-04:00',
                'timeZone': 'Europe/Vienna'
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=3'
            ],
            'attendees': [
                {'email': 'patrick.bonini13@gmail.com'}
            ]
        }

        event = service.events().insert(calendarId='primary', body=event).execute()

        print(f"Event created {event.get('htmlLink')}")

    except HttpError as error:
        print("Error occurred:", error)

if __name__ == '__main__':
    main()