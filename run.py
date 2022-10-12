# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
import datetime
from datetime import datetime
from datetime import date 
import re
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting import *




SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)



print("Welcome to the Open Day Planner. I hope it helps to make the event run seamlessly!\n")

def get_event_type():
    """
    Request type of event from user (Open Day or Musician)
    """
    while True:
        global event_type
        event_type=input("What type of event are you planning? Please write Open Day or Musician: ")
        if validate_event_type(event_type):
            break
    return event_type

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
        event_date = input("Event date: \n")
        if validate_event_date(event_date):
            return event_date
            break
    
   

def confirm_date():
    final_date_to_check = get_date_to_check()    
    while True:
        checkDate = input("Is this correct (Y/N)? \n")
        if check_date_validation(checkDate):
            break
    if checkDate == "N":
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

def get_date_to_check():
    global date_of_event
    date_of_event = get_event_date()
    format_ddmmyyyy = "%d/%m/%Y"
    formatted_date = datetime.strptime(date_of_event, format_ddmmyyyy)
    # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    formatted_date_no_time = datetime.date(formatted_date)
    # https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
    date_to_check = formatted_date_no_time.strftime("%A, %d. %B %Y")
    print(f"You provided this date: {date_to_check}")
    return date_to_check
    
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

def get_email():
    while True:
        global entered_email
        entered_email = input("What is your email address?  ")
        print("\n")
        if validate_email(entered_email):
            break
    print("Thank you for providing a valid email address so we can share the spreadsheet with you.\n")
    return entered_email

def validate_email(s):
    pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat,s):
        return True
    else:
        print("That is not a valid email address; please try again.\n")
        return False




    # datestouse
    # date_today = date.today()
    # format_ddmmyyyy = "%d/%m/%Y"
    # formatted_date = datetime.strptime(date_of_event, format_ddmmyyyy)
    # # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    # formatted_date_no_time = datetime.date(formatted_date)
    # # https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
    # date_to_check = formatted_date_no_time.strftime("%A, %d. %B %Y")


# https://theprogrammingexpert.com/python-remove-time-from-datetime/#:~:text=To%20remove%20the%20time%20from,a%20date%20using%20date().&text=You%20can%20also%20use%20strftime,datetime%20object%20without%20the%20time.
def check_date_future():
    if formatted_date_no_time > datetime.today().date():
        print("greater than")
    elif formatted_date_no_time < datetime.today().date():
        print("less than")

def create_spreadsheet():
    global spreadsheet
    spreadsheet = GSPREAD_CLIENT.create(f'{event_type}: {date_of_event}')
    spreadsheet.share(f'{entered_email}', perm_type='user', role='writer')
    # spreadsheet = GSPREAD_CLIENT.create('test-spreadsheet')
    # spreadsheet.share('mandyhole17@gmail.com', perm_type='user', role='writer')

def create_worksheet(sheet_name, sheet_data, final_column):
    test_spreadsheet=GSPREAD_CLIENT.open('Open Day: 14/08/2020')
    new_worksheet=test_spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
    # https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
    new_worksheet.clear()
    set_with_dataframe(worksheet=new_worksheet, dataframe=sheet_data, include_index=False,
    include_column_header=True, resize=True)
    # https://github.com/robin900/gspread-formatting
    set_column_width(new_worksheet, 'A:D', 250)
    fmt = cellFormat(
        backgroundColor=color(.9, .9, .9),
        textFormat=textFormat(bold=True, foregroundColor=color(0, 0, 0)),
        horizontalAlignment='CENTER'
        )
    format_cell_range(new_worksheet, f'A1:{final_column}1', fmt)

    return new_worksheet
    
    # spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20) change above to this once done testing to create new spreadsheet)
    # sheet_name.update([sheet_values.columns.values.tolist()] + sheet_values.values.tolist())

# https://www.digitalocean.com/community/tutorials/update-rows-and-columns-python-pandas
# https://docs.gspread.org/en/latest/user-guide.html




stock_data = pd.DataFrame({
    'Type of Stock': ['Highlighter', 'Luggage Tag', 'Pens', 'Pencils', 'Notebooks', 'Water bottles'],
    'Number Remaining': ['', '', '', '', '', ''],
    'Location of Stock': ['', '', '', '', '', ''],
    'Date checked': ['', '', '', '', '', '']})

create_worksheet('Stock Take', stock_data, 'D')

attendees_data = pd.DataFrame({
    "Name of Child": [''],
    "Child's Year Group": [''],
    "Child's Interests": [''],
    "Dietary Requirements": [''],
})

tasks_data = pd.DataFrame({
    "Task": [
            'Added to Website',
            'Option on Booking Form', 
            'Created Zap', 
            'Added Facebook Event',
            'Checked Stock',
            'Ordered New Badges',
            'Update Social Headers/Add popup Box',
            'Add social post / boost',
            'Complete artwork',
            'Add social media post(2)',
            'Add social media post(3)',
            'Remove option from form',
            'Remove Social Header'
            ],
    "Date completed": ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    "Person performing task": ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    "Notes": ['', '', '', '', '', '', '', '', '', '', '', '', '']
})


# create_spreadsheet()
# create_worksheet('Tasks', tasks_dataframe)
# create_worksheet('Attendees', attendees_dataframe)
# create_worksheet('Stock Take', stock_dataframe)


# https://www.tutorialspoint.com/python-program-to-validate-email-address


# def main():
#     get_event_type()
#     confirm_date()
#     get_email()
    # create_spreadsheet()
    # tasks_worksheet = create_worksheet('Stock')
    # set_with_dataframe(tasks_worksheet, stock_data)