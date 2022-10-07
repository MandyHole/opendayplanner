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
from datetime import datetime
from datetime import date 


print("Welcome to the Open Day Planner. I hope it helps to make the event run seamlessly!\n")

def get_event_type():
    """
    Request type of event from user (Open Day or Musician)
    """
    while True:
        event_type=input("What type of event are you planning? Please write Open Day or Musician: ")
        if validate_event_type(event_type):
            break

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
    print("\n")
    print("Please provide the date of the event (use the format dd/mm/yyyy) \n")
    while True:
        eventDate = input("Event date: \n")
        if validate_event_date(eventDate):
            return eventDate
            break
    print(f"You provided this date {eventDate}")
   

def confirm_date():
    while True:
        checkDate = input("Is this correct (Y/N)? \n")
        if check_date_validation(checkDate):
            break
    if checkDate == "N":
        get_event_date()
        confirm_date()





def validate_event_date(date_values):
    """ 
    check date provided is a valid date
    """
    # https://theprogrammingexpert.com/check-if-string-is-date-in-python/#:~:text=To%20check%20if%20a%20string,string%20and%20a%20date%20format.&text=When%20working%20with%20strings%20in,date%20can%20be%20very%20useful.

    format_ddmmyyyy = "%d/%m/%Y"
    try:
        date = datetime.strptime(date_values, format_ddmmyyyy)
    except ValueError:
        print("Please ensure you use the format dd/mm/yyyy.")
        return False
    return True
    
def check_date_validation(check_value):
    try:
        if check_value != "Y" and check_value != "N":
            raise ValueError (
                "Please input 'Y' for yes or 'N' for no, ensuring you use a capital letter."
            )
    except ValueError as e:
        print(f"'{check_value}' is not a valid response. {e}\n")
        return False
    return True

date_today = date.today()
print(date_today)

get_event_type()
date_of_event = get_event_date()
format_ddmmyyyy = "%d/%m/%Y"
formatted_date = datetime.strptime(date_of_event, format_ddmmyyyy)
# https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
formatted_date_no_time = datetime.date(formatted_date)

confirm_date()
print(f"formatted date: {formatted_date}")
# https://theprogrammingexpert.com/python-remove-time-from-datetime/#:~:text=To%20remove%20the%20time%20from,a%20date%20using%20date().&text=You%20can%20also%20use%20strftime,datetime%20object%20without%20the%20time.
print(f"formatted date without time: {formatted_date_no_time}")
# print(type(formatted_date))
# print(type(formatted_date_no_time))
# print(type(date_today))
if formatted_date_no_time > datetime.today().date():
    print("greater than")
elif formatted_date_no_time < datetime.today().date():
    print("less than")