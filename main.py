"""
This program allows the user to upload their class schedule in text format and have it automatically uploaded 
to their Google Calendar:
-In weekly intervals
-For the duration of a semester
-Each class has a different colour

This program only works for authorized users (as per google cloud console dashboard):
patrick.bonini13@gmail.com
"""
import datetime as dt
import os.path
import re

#text to google calendar
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']

def main ():
    """
    If you're a first time user, signs in to your google account
    """
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

    #Converts the text file into a list containing the different elements needed
    textFromFile = open('schedule.txt', 'r')
    text = textFromFile.read()
    text = text.split('; ')
    schedule = [i.split(', ') for i in text]
    #Loops over the list
    for i in range(len(schedule)):
        #Assigns a different color code to each class
        colors = [0,1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7]
        currentColor = colors[i]
        #Creates the calendar events
        try:
            service = build("calendar", "v3", credentials=creds)

            event = {
                'summary': schedule[i][0],       
                'Description': 'Event details',
                'colorId': currentColor,
                'start': {
                    'dateTime': schedule[i][1],
                    'timeZone': 'America/Chicago'
                },
                'end': {
                    'dateTime': schedule[i][2],
                    'timeZone': 'America/Chicago'
                },
                'location': schedule[i][3],
                'recurrence': [
                    'RRULE:FREQ=WEEKLY;COUNT=13'
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