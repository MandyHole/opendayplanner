# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials
# import datetime
from datetime import datetime
from datetime import date 
from datetime import timedelta
import re
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
from gspread_formatting import *




SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar"
    # ,
    # "https://www.googleapis.com/tasks/v1/lists/taskListID/tasks?parameters",
    # "https://www.googleapis.com/tasks/v1/users/userID/lists?parameters"
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
    global formatted_date
    formatted_date = datetime.strptime(date_of_event, format_ddmmyyyy)
    # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    global formatted_date_no_time
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

def create_worksheet(sheet_name, sheet_data, final_column):
    # test_spreadsheet=GSPREAD_CLIENT.open('Open Day: 14/08/2020')
        #  change above to this once done testing to create new spreadsheet)
    new_worksheet=spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
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
    

# https://www.digitalocean.com/community/tutorials/update-rows-and-columns-python-pandas
# https://docs.gspread.org/en/latest/user-guide.html




stock_data = pd.DataFrame({
    'Type of Stock': ['Highlighter', 'Luggage Tag', 'Pens', 'Pencils', 'Notebooks', 'Water bottles'],
    'Number Remaining': ['', '', '', '', '', ''],
    'Location of Stock': ['', '', '', '', '', ''],
    'Date checked': ['', '', '', '', '', '']})


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

musician_tasks_data = pd.DataFrame({
    "Task": [
            'Added to Website',
            'Option on Booking Form', 
            'Created Zap', 
            'Checked Stock',
            'Remove option from form',
            ],
    "Date completed": ['', '', '', '', ''],
    "Person performing task": ['', '', '', '', ''],
    "Notes": ['', '', '', '', '']
})

def calculate_reminder(x):
    format_ddmmyyyy = "%d/%m/%Y"
    formatted_final_event_date = datetime.strptime(date_of_event, format_ddmmyyyy)
    reminder = formatted_final_event_date - timedelta(days=x)
    date_today = datetime.now()
    if reminder <= date_today:
        reminder = date_today
        print("This date is in the past.")
    elif reminder.strftime("%A") == "Saturday":
        reminder = formatted_final_event_date - timedelta(days=(x+1))
        if reminder <= date_today:
            reminder = date_today
        print("This is a Saturday")
    elif reminder.strftime("%A") == "Sunday":
        reminder = formatted_final_event_date - timedelta(days=(x+2))
        if reminder <= date_today:
            reminder = date_today
        print("This is a Sunday")
    return print(reminder)

calculate_reminder(63)
    
# https://developers.google.com/calendar/api/v3/reference/events/insert
def add_event_to_calendar(description, day):
    event = {
    'summary': f'{event_type}: {date_of_event} Tasks to Complete', 
    'description': f'It is about {day} days until the event. Open the {event_type}: {date_of_event} spreadsheet. {description} Complete the Task Planner Spreadsheet.',
    'start': {
        'dateTime': calculate_reminder(day),
        'timeZone': 'Europe/London',
    'transparency': 'transparent',
    },
    'end': {
        'dateTime': calculate_reminder(day) + timedelta(hours=1),
        'timeZone': 'Europe/London',
    },
    'attendees': [
        {'email': entered_email},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 0},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()

# https://www.tutorialspoint.com/python-program-to-validate-email-address


def main():
    # get_event_type()
    confirm_date()
    # get_email()
    # create_spreadsheet()
    if event_type == "Musician":
        create_worksheet('Task Planner', musician_tasks_data, 'D')
        create_worksheet('Attendees', attendees_data, 'D')
        create_worksheet('Stock Take', stock_data, 'D')
        add_event_to_calendar('Contact Music Department and see if any boosting is required', 30)
        add_event_to_calendar('Remove option from form', 7)
        add_event_to_calendar('Post on social to saying looking forward to event', 1)
        add_event_to_calendar('Please take a photo of the event today and post on social media', 0)
        print("You will now have been shared a spreadsheet to plan the Musician Event.\n"
        print("You also will have reminders in your Calendar on what you need to do going forward.\n")
        print("Please ensure you do the following as soon as possible:\n")
        print("Add it as an event to the website. \n")
        print("Add it as an option to the booking form.\n")
        print("Create a zap to link the Musician Sign Up form to the Attendees worksheet.\n")
        print("Ensure you initial and date these tasks are complete using the Task Planner Worksheet.\n")
        print("We hope this helps with your planning. Please refresh the page to plan another event.\n")

    elif event_type == "Open Day":
        create_worksheet('Task Planner', tasks_data, 'D')
        create_worksheet('Attendees', attendees_data, 'D')
        create_worksheet('Stock Take', stock_data, 'D')
        add_event_to_calendar('Please remember to check the stock (enter into Stock worksheet), order staff badges and update the social headers.', 60)
        add_event_to_calendar('Please remember to add post to social media, boost if required and prepare artwork for next Open Day', 30)
        add_event_to_calendar('Please remember to post reminder on social media', 7)
        add_event_to_calendar('Please remember to post photo of gift bags on social media and update social headers to next event', 1)
        add_event_to_calendar('Please remember to remove option from form', 0)
        print("You will now have been shared a spreadsheet to plan the Open Day.\n"
        print("You also will have reminders in your Calendar on what you need to do going forward.\n")
        print("Please ensure you do the following as soon as possible:\n")
        print("Add it as an event to the website and Facebook. \n")
        print("Add it as an option to the booking form.\n")
        print("Create a zap to link the Open Day Signup form to the Attendees worksheet.\n")
        print("Ensure you initial and date these tasks are complete using the Task Planner Worksheet.\n")
        print("We hope this helps with your planning. Please refresh the page to plan another event.\n")


main()