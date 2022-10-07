# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high



import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

import datetime

def getEventType():
    print("Welcome to the Open Day Planner. I hope it helps to make the event run seamlessly!\n")
    event_type=input("What type of event is it? Please write Open Day or Musician: ")
    print(f"The event type you provided is {event_type}")
    print("\n")
    if event_type == "Open Day":
        print("You selected Open Day, a valid response")
    elif event_type == "Musician":
        print("You selected Musician, a valid response")
    else:
        print("That is not a valid response. Please select Open Day or Musician, ensuring you use initial caps")

getEventType()