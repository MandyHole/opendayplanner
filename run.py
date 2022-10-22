# Write your code to expect a terminal of 80 characters wide and 24 rows high
from datetime import datetime, date, timedelta
import re
import asyncio
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/calendar"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


stock_data = pd.DataFrame({
    'Type of Stock': ['Highlighter', 'Luggage Tag', 'Pens',
                      'Pencils', 'Notebooks', 'Water Bottles'],
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
            'Update Social Headers/Add Popup Box',
            'Add Social Post / Boost',
            'Complete New Artwork',
            'Add Social Media Post(2)',
            'Add Social Media Post(3)',
            'Remove Option From Form',
            'Remove Social Header'
            ],
    "Date Completed": ['', '', '', '', '', '', '', '', '', '', '', '', ''],
    "Person Performing Task": ['', '', '', '', '', '',
                               '', '', '', '', '', '', ''],
    "Notes": ['', '', '', '', '', '', '', '', '', '', '', '', '']
})

musician_tasks_data = pd.DataFrame({
    "Task": [
            'Added to Website',
            'Option on Booking Form',
            'Created Zap',
            'Checked Stock',
            'Remove Option From Form',
            ],
    "Date Completed": ['', '', '', '', ''],
    "Person Performing Task": ['', '', '', '', ''],
    "Notes": ['', '', '', '', '']
})

print("Welcome to the Open Day Planner.")
print("I hope it helps to make the event run seamlessly!\n")


def get_event_type():
    """
    Requests the type of event from user (Open Day or Musician).
    Loops until the user inputs a correct value.
    """
    while True:
        global EVENT_TYPE
        EVENT_TYPE = input("Type of event: ")
        if validate_event_type(EVENT_TYPE):
            break
    return EVENT_TYPE


def validate_event_type(values):
    """
    Checks user input 'Open Day' or 'Musician'
    Produces a value error if not and triggers loop to ask again.
    """
    try:
        if values != "Open Day" and values != "Musician":
            raise ValueError(
                "Input 'Open Day' or 'Musician' using initial caps."
            )
    except ValueError as e:
        print(f"'{values}' is not a valid response. {e}\n")
        return False
    return True


def get_event_date():
    """
    Get input from user about date of event.
    Sends input through validation.
    Loops until a correctly formatted date in future is input.
    """
    print("\n")
    print("Please provide the date of the event.")
    print("Use the format dd/mm/yyyy) \n")
    while True:
        event_date = input("Event date: ")
        if validate_event_date(event_date):
            break
    print("\n")
    return event_date


def validate_event_date(date_values):
    """
    Checks the date provided is formatted correctly.
    Checks the date provided is in the future.
    Produces a value error if either condition isn't met.
    """
    # https://theprogrammingexpert.com/check-if-string-is-date-in-python/#:~:text=To%20check%20if%20a%20string,string%20and%20a%20date%20format.&text=When%20working%20with%20strings%20in,date%20can%20be%20very%20useful.
    # https://theprogrammingexpert.com/python-remove-time-from-datetime/#:~:text=To%20remove%20the%20time%20from,a%20date%20using%20date().&text=You%20can%20also%20use%20strftime,datetime%20object%20without%20the%20time.

    format_ddmmyyyy = "%d/%m/%Y"
    # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    date_today = datetime.now()
    try:
        if date == datetime.strptime(date_values,
                                     format_ddmmyyyy) or \
            datetime.strptime(date_values,
                              format_ddmmyyyy) <= date_today:
            raise ValueError(
                "Use the format dd/mm/yyyy and check it is in the future.")
    except ValueError as e:
        print(f"'{date_values}' is not a valid response. {e}\n")
        return False
    return True


def get_date_to_check():
    """
    Reformats date into a format with Day and Month spelled out
    Prints date to user to check to ensure it is correct.
    """
    global DATE_OF_EVENT
    DATE_OF_EVENT = get_event_date()
    format_ddmmyyyy = "%d/%m/%Y"
    formatted_date = datetime.strptime(DATE_OF_EVENT, format_ddmmyyyy)
    # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    formatted_date_no_time = datetime.date(formatted_date)
    # https://docs.python.org/3/library/datetime.html#datetime.datetime.weekday
    date_to_check = formatted_date_no_time.strftime("%A, %d. %B %Y")
    print(f"You provided this date: {date_to_check}")
    return date_to_check


def confirm_date():
    """
    Enables user to confirm that the date provided is the correct date.
    If not, loops back to ask for the date again.
    """
    get_date_to_check()
    while True:
        check_date = input("Is this date correct (Y/N)? \n")
        if check_date_validation(check_date):
            break
    if check_date == "N":
        confirm_date()


def check_date_validation(check_value):
    """
    Checks user input Y or N to confirm date.
    Produces value error if not.
    """
    try:
        if check_value != "Y" and check_value != "N":
            raise ValueError(
                "Please input 'Y' for yes or 'N' for no."
            )
    except ValueError as e:
        print(f"'{check_value}' is not a valid response. {e}\n")
        return False
    return True


def get_email():
    """
    Asks user to input their email address.
    Loops until a valid email address is provided.
    Prints statements to say what email will be used for.
    """
    print("\n")
    print("Your email address enables access to a spreadsheet and reminders")
    while True:
        global ENTERED_EMAIL
        ENTERED_EMAIL = input("What is your email address?  ")
        print("\n")
        if validate_email(ENTERED_EMAIL):
            break
    print("Thank you for providing a valid email address.")
    print("We can share the Google spreadsheet and reminders with you.\n")
    print("Please be patient as the spreadsheet is created...\n")
    return ENTERED_EMAIL


def validate_email(s):
    """
    Checks to ensure the email address provided is in the correct format.
    Prints a statement if incorrect format.
    """
    # https://www.tutorialspoint.com/python-program-to-validate-email-address
    pat = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
    if re.match(pat, s):
        return True
    else:
        print("That is not a valid email address; please try again.\n")
        return False


def create_spreadsheet():
    """
    Creates a spreadsheet that is shared with user's email.
    Spreadsheet is titled with the event type and date.
    """
    global SPREADSHEET
    SPREADSHEET = GSPREAD_CLIENT.create(f'{EVENT_TYPE}: {DATE_OF_EVENT}')
    SPREADSHEET.share(f'{ENTERED_EMAIL}', perm_type='user', role='writer')


def create_worksheet(sheet_name, sheet_data, final_column):
    """
    Adds a new worksheet to the spreadsheet created for the event.
    Inputs dataframes for content.
    Adds formatting to header row.
    """
    # test_spreadsheet=GSPREAD_CLIENT.open('Open Day: 14/08/2020')
    #  change above to this once done testing to create new spreadsheet)
    new_worksheet = SPREADSHEET.add_worksheet(title=sheet_name,
                                              rows=100, cols=20)
    # https://medium.com/@jb.ranchana/write-and-append-dataframes-to-google-sheets-in-python-f62479460cf0
    new_worksheet.clear()
    set_with_dataframe(worksheet=new_worksheet,
                       dataframe=sheet_data, include_index=False,
                       include_column_header=True, resize=True)
    # https://github.com/robin900/gspread-formatting
    set_column_width(new_worksheet, f'A:{final_column}', 250)
    fmt = cellFormat(
        backgroundColor=color(.9, .9, .9),
        textFormat=textFormat(bold=True, foregroundColor=color(0, 0, 0)),
        horizontalAlignment='CENTER'
        )
    format_cell_range(new_worksheet, f'A1:{final_column}1', fmt)
    return new_worksheet
# https://www.digitalocean.com/community/tutorials/update-rows-and-columns-python-pandas
# https://docs.gspread.org/en/latest/user-guide.html


def calculate_reminder(x):
    """
    Adjusts the calendar reminder dates.
    Ensures event doesn't occur in the past.
    Ensures event doesn't occur on a weekend.
    """
    format_ddmmyyyy = "%d/%m/%Y"
    formatted_final_event_date = datetime.strptime(DATE_OF_EVENT,
                                                   format_ddmmyyyy)
    reminder = formatted_final_event_date - timedelta(days=x)
    date_today = datetime.now()
    if reminder <= date_today:
        reminder = date_today
    elif reminder.strftime("%A") == "Saturday":
        reminder = formatted_final_event_date - timedelta(days=(x+1))
        if reminder <= date_today:
            reminder = date_today
    elif reminder.strftime("%A") == "Sunday":
        reminder = formatted_final_event_date - timedelta(days=(x+2))
        if reminder <= date_today:
            reminder = date_today


# https://developers.google.com/calendar/api/v3/reference/events/insert
def add_event_to_calendar(description, day):
    """
    Adds a reminder to the user's calendar using email provided.
    Includes customised description with tasks needed.
    Date of reminder is in relation to date of event.
    """
    event = {
        'summary': f'{EVENT_TYPE}: {DATE_OF_EVENT} Tasks to Complete',
        'description': f'It is about {day} days until the event. Open the \
            {EVENT_TYPE}: {DATE_OF_EVENT} spreadsheet. {description} \
                Complete the Task Planner Spreadsheet.',
        'start': {
            'dateTime': calculate_reminder(day),
            'timeZone': 'Europe/London',
        },
        'end': {
            'dateTime': calculate_reminder(day) + timedelta(hours=1),
            'timeZone': 'Europe/London',
        },
        'attendees': [
            {'email': ENTERED_EMAIL},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 0},
                {'method': 'popup', 'minutes': 10},
            ],
        },
        'transparency': 'transparent',

    }
    event = service.events().insert(calendarId='primary', body=event).execute()


async def main():
    """
    Runs all functions for the programe to work
    """
    print("Please specify the type of event that you are planning.")
    print("* This could be 'Open Day' or 'Musician'.")
    print("* Please ensure you use initial caps.\n")
    get_event_type()
    confirm_date()
    get_email()
    # create_spreadsheet()
    if EVENT_TYPE == "Musician":
        # create_worksheet('Task Planner', musician_tasks_data, 'D')
        # create_worksheet('Attendees', attendees_data, 'D')
        # create_worksheet('Stock Take', stock_data, 'D')
        # sheet_one = SPREADSHEET.get_worksheet(0)
        # SPREADSHEET.del_worksheet(sheet_one)
        # add_event_to_calendar('Contact Music Department \
        #   and see if any boosting is required', 30)
        # add_event_to_calendar('Remove option from form', 7)
        # add_event_to_calendar(
        #   'Post on social to saying looking forward to event', 1)
        # add_event_to_calendar(
        #   'Please take a photo of the event today \
        #    and post on social media', 0)
        # https://docs.python.org/3/library/asyncio.html
        print("You will now have been shared a spreadsheet\
              to plan the Musician Event.\n")
        await asyncio.sleep(3)
        print("You also will have reminders in your Calendar\
              on what you need to do going forward.\n")
        await asyncio.sleep(3)
        print("Please ensure you do the following as soon as possible:\n")
        await asyncio.sleep(3)
        print("* Add it as an event to the website. \n")
        await asyncio.sleep(3)
        print("* Add it as an option to the booking form.\n")
        await asyncio.sleep(3)
        print("* Create a zap to link the Musician Sign Up form \
              to the Attendees worksheet.\n")
        await asyncio.sleep(3)
        print("* Ensure you initial and date these tasks are \
              complete using the Task Planner Worksheet.\n")
        await asyncio.sleep(3)
        print("We hope this helps with your planning. Please \
              refresh the page to plan another event.\n")

    elif EVENT_TYPE == "Open Day":
        # create_worksheet('Task Planner', tasks_data, 'D')
        # create_worksheet('Attendees', attendees_data, 'D')
        # create_worksheet('Stock Take', stock_data, 'D')
        # sheet_one = SPREADSHEET.get_worksheet(0)
        # SPREADSHEET.del_worksheet(sheet_one)
        # add_event_to_calendar('Please remember to check the \
        #                        stock (enter into Stock worksheet), \
        #                        order staff badges and update the \
        #                        social headers.', 60)
        # add_event_to_calendar('Please remember to add post to \
        #                        social media, boost if required and \
        #                        prepare artwork for next Open Day', 30)
        # add_event_to_calendar('Please remember to post reminder on \
        #                        social media', 7)
        # add_event_to_calendar('Please remember to post photo of \
        #                        gift bags on social media and \
        #                        update social headers to next event', 1)
        # add_event_to_calendar('Please remember to remove the option \
        #                        from the form', 0)
        print("You will now have been shared a spreadsheet \
               to plan the Open Day.\n")
        await asyncio.sleep(3)
        print("You also will have reminders in your Calendar on \
               what you need to do going forward.\n")
        await asyncio.sleep(3)
        print("Please ensure you do the following \
               as soon as possible:\n")
        await asyncio.sleep(3)
        print("* Add it as an event to the website and Facebook. \n")
        await asyncio.sleep(3)
        print("* Add it as an option to the booking form.\n")
        await asyncio.sleep(3)
        print("* Create a zap to link the Open Day Signup form \
               to the Attendees worksheet.\n")
        await asyncio.sleep(3)
        print("* Ensure you initial and date these tasks are complete \
               using the Task Planner Worksheet.\n")
        await asyncio.sleep(3)
        print("We hope this helps with your planning. \
               Please refresh the page to plan another event.\n")

asyncio.run(main())
