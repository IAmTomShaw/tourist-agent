import datetime
import os
from src.lib import _to_rfc3339

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
  "https://www.googleapis.com/auth/calendar.readonly",
  "https://www.googleapis.com/auth/calendar.events"
]

creds = None

if os.path.exists("tokens/gcal.json"):
  creds = Credentials.from_authorized_user_file("tokens/gcal.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
      "config/credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open("tokens/gcal.json", "w") as token:
    token.write(creds.to_json())

def get_events(start_date: str = None, end_date: str = None):
  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    if start_date:
      start_date = _to_rfc3339(start_date, datetime.datetime.now())
    else:
      start_date = _to_rfc3339(None, datetime.datetime.now())
    
    if end_date:
      end_date = _to_rfc3339(end_date, datetime.datetime.now() + datetime.timedelta(days=10))
    else:
      end_date = _to_rfc3339(None, datetime.datetime.now() + datetime.timedelta(days=10))
    
    calendar_ids = service.calendarList().list().execute()

    events = []

    for calendar in calendar_ids['items']:
      events_result = service.events().list(
        calendarId=calendar['id'],
        timeMin=start_date,
        timeMax=end_date,
        maxResults=100,
        singleEvents=True,
        orderBy='startTime'
      ).execute()

      event_res = events_result.get('items', [])

      if not event_res:
        continue

      # Prints the start and name of the next 10 events
      for event in event_res:
        events.append({
          "calendar": calendar['summary'],
          "start": event['start'].get('dateTime', event['start'].get('date')),
          "end": event['end'].get('dateTime', event['end'].get('date')),
          "summary": event['summary'],
          "id": event['id'],
          "location": event['location'] if 'location' in event else None
        })

    return events

  except HttpError as error:
    print(f'An error occurred: {error}')
    return None