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

from datetime import datetime

def get_event_type():
    """
    Request type of event from user (Open Day or Musician)
    """
    print("Welcome to the Open Day Planner. I hope it helps to make the event run seamlessly!\n")
    while True:
        event_type=input("What type of event are you planning? Please write Open Day or Musician: ")
        if validate_event_type(event_type):
            print("You input a valid event type")
            break
    # print(f"The event type you provided is {event_type}")
    # print("\n")
    # if event_type == "Open Day":
    #     print("You selected Open Day, a valid response")
    # elif event_type == "Musician":
    #     print("You selected Musician, a valid response")
    # else:
    #     print("That is not a valid response. Please select Open Day or Musician, ensuring you use initial caps")

def validate_event_type(values):
    """ 
    Check user input Open Day or Musician
    """
    try:
        if values != "Open Day" and values != "Musician":
            raise ValueError (
                "Please input 'Open Day' or 'Musician', ensuring you use initial caps."
            )
    except ValueError as e:
        print(f"'{values}' is not a valid response. {e}\n")
        return False
    return True


def get_event_date():
    """
    Get input from user about date of event
    """
    print("Please provide the date of the event")
    print("Use the format mm/dd/yyyy \n")
    eventDate = input("Event date: \n")
    validate_event_date(eventDate)
    

def validate_event_date(date_values):
    """ 
    check date provided is a valid date
    """
    # https://theprogrammingexpert.com/check-if-string-is-date-in-python/#:~:text=To%20check%20if%20a%20string,string%20and%20a%20date%20format.&text=When%20working%20with%20strings%20in,date%20can%20be%20very%20useful.

    format_ddmmyyyy = "%d/%m/%Y"
    try:
        date = datetime.strptime(date_values, format_ddmmyyyy)
        print("The string is a date with format " + format_ddmmyyyy)
    except ValueError:
        print("The string is not a date with format " + format_ddmmyyyy)
        return False
    return True

    
    print(f"You provided this date {eventDate}")
    checkDate = input("Is this correct (Y/N)")
    if checkDate == "Y":
        print("They typed the right date!)")
    elif checkDate == "N":
        print("Better try again")
    else:
        print("Please try again and type either 'Y' or 'N'")

get_event_type()
# get_event_date()
