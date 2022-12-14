# Write your code to expect a terminal of 80 characters wide and 24 rows high
from datetime import datetime, date, timedelta
import re
import asyncio
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from gspread_formatting import *

# From Love Sandwiches Project
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# From Love Sandwiches Project
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)


stock_data = pd.DataFrame({
    'Type of Stock': ['Highlighter', 'Luggage Tag', 'Pens',
                      'Pencils', 'Notebooks', 'Water Bottles'],
    'Number Remaining': ['', '', '', '', '', ''],
    'Location of Stock': ['', '', '', '', '', ''],
    'Date Checked': ['', '', '', '', '', '']
    })

attendees_data = pd.DataFrame({
    "Surname": [''],
    "Child 1's Year Group": [''],
    "Child 1's Interests": [''],
    "Child 2's Year Group": [''],
    "Child 2's Interests": [''],
    "Child 3's Year Group": [''],
    "Child 3's Interests": [''],
    "Dietary Requirements": [''],
    "How Heard About Us": ['']
})

tasks_data = pd.DataFrame({
    "Task": [
            'Select imagery',
            'Add event to website',
            'Add booking form option',
            'Create Zap: add attendees',
            'Create Zap: reminders',
            'Add Facebook/Nub News Event',
            'Check promo stock',
            'Order billboards',
            'Order bus magnets',
            'Create invitations/posters/flyers',
            'Print invitations,etc',
            'Email Prep Schools',
            'Submit caretaker request',
            'Distribute invitations, etc',
            'Order staff badges',
            'Update social headers: Facebook/Insta',
            'Add website popup',
            'Add social post / boost',
            'Confirm attendance',
            'Add social post(2)',
            'Pack goody bags',
            'Print name badges',
            'Add social post(3)',
            'Remove option from form',
            'Remove social header',
            'Wrap up event'
            ],
    "Due Date": ['', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', '',
                 '', '', '', '', '', '', '', '', ''],
    "Date Completed": ['', '', '', '', '', '',
                       '', '', '', '', '', '', '',
                       '', '', '', '', '', '', '',
                       '', '', '', '', '', ''],
    "Contact Email": ['', '', '', '', '', '',
                      '', '', '', '', '', '', '',
                      '', '', '', '',
                      '', '', '', '', '', '', '', '', ''],
    "Notes": ['', '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '',
              '', '', '', '', '', '', '', '', '']
})

prep_tasks_data = pd.DataFrame({
    "Task": ['Select imagery',
             'Add event to website',
             'Add booking form option',
             'Create Zap: add attendees',
             'Create Zap: reminders',
             'Add Facebook /Nub News Event',
             'Book required rooms & photographer',
             'Notify catering',
             'Check promo stock',
             'Order billboards',
             'Order bus magnets',
             'Create invitations/posters/flyers',
             'Print invitations,etc',
             'Email Prep Schools',
             'Submit caretaker request',
             'Distribute invitations, etc',
             'Order staff badges',
             'Update social headers: Facebook/Insta',
             'Add website popup',
             'Add social post / boost',
             'Confirm attendance',
             'Confirm numbers to catering',
             'Add social post(2)',
             'Pack goody bags',
             'Print name badges',
             'Add social post(3)',
             'Remove option from form',
             'Remove social header',
             'Wrap up event'],
    "Due Date": ['', '', '', '', '',
                 '', '', '', '', '',
                 '', '', '', '', '',
                 '', '', '', '', '',
                 '', '', '', '', '',
                 '', '', '', ''],
    "Date Completed": ['', '', '', '', '',
                       '', '', '', '', '',
                       '', '', '', '', '',
                       '', '', '', '', '',
                       '', '', '', '', '',
                       '', '', '', ''],
    "Person Performing Task": ['', '', '', '', '',
                               '', '', '', '', '',
                               '', '', '', '', '',
                               '', '', '', '', '',
                               '', '', '', '', '',
                               '', '', '', ''],
    "Notes": ['', '', '', '', '',
              '', '', '', '', '',
              '', '', '', '', '',
              '', '', '', '', '',
              '', '', '', '', '',
              '', '', '', '']
})

badges_data = pd.DataFrame({
    "Title": [''],
    "First Name": [''],
    "Surname": [''],
    "Job Title": [''],
})

print("Welcome to the Open Day Planner.")
print("I hope it helps to make the event run seamlessly!\n")


def get_event_type():
    """
    Requests the type of event from user (Open Day or Prep).
    Loops until the user inputs a correct value.
    """
    while True:
        global EVENT_TYPE
        EVENT_TYPE = input("Type of event:\n")
        if validate_event_type(EVENT_TYPE):
            break
    return EVENT_TYPE


def validate_event_type(values):
    """
    Checks user input 'Open Day' or 'Prep'
    Produces a value error if not and triggers loop to ask again.
    """
    try:
        if values != "Open Day" and values != "Prep":
            raise ValueError(
                "Input 'Open Day' or 'Prep' using initial caps."
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
        event_date = input("Event date: \n")
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
    # https://stackoverflow.com/questions/7239315/cant-compare-datetime-datetime-to-datetime-date
    format_ddmmyyyy = "%d/%m/%Y"
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
        if check_y_n(check_date):
            break
    if check_date == "N":
        confirm_date()


def check_y_n(check_value):
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
    print("Your email address enables access to a planning spreadsheet")
    while True:
        global ENTERED_EMAIL
        ENTERED_EMAIL = input("What is your email address?\n")
        print("\n")
        if validate_email(ENTERED_EMAIL):
            break
    print("Thank you for providing a valid email address.")
    print("We can share the Google spreadsheet with you.\n")
    print("Please be patient as the spreadsheet is created...\n")
    return ENTERED_EMAIL


def validate_email(s):
    """
    Checks to ensure the email address provided is in the correct format.
    Prints a statement if incorrect format.
    """
    # https://www.tutorialspoint.com/python-program-to-validate-email-address
    # https://www.includehelp.com/python/ignoring-escape-sequences-in-the-string.aspx#:~:text=To%20ignoring%20escape%20sequences%20in,%22r%22%20before%20the%20string.
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


def staff_badge_data():
    """
    Gets input from users requesting data required for staff badge.
    Runs through validation to ensure a response was provided.
    Appends Information to Badges worksheet using NewStaff Class
    """
    staff_title = get_staff_data("What is their title?")
    staff_first_name = get_staff_data("What is their first name?")
    staff_surname = get_staff_data("What is their surname?")
    staff_role = get_staff_data("What is their job title?")
    new_staff_member = NewStaff(staff_title,
                                staff_first_name, staff_surname, staff_role)
    new_staff_member.add_to_worksheet()


def get_staff_data(info_required):
    """
    Loops staff input until a response is provided.
    Formats response to all caps
    """
    while True:
        var_x = input(f"{info_required} \n")
        if validate_staff(var_x):
            var_final = var_x.upper()
            break
    return var_final


def validate_staff(values):
    """
    Checks user input something into the staff input
    Produces a value error if not and triggers loop to ask again.
    """
    try:
        if values == "":
            raise ValueError(
                "You didn't add any text. Please include a valid response."
            )
    except ValueError as e:
        print(f"{e}\n")
        return False
    return True


def staff_badge_needed():
    """
    Enables user to specify if a staff badge is needed
    Loops until no more badges are required
    """
    while True:
        badge_required = input(
            "Do you need to order a new staff badge (Y/N)? \n")
        if check_y_n(badge_required):
            break
    if badge_required == "Y":
        staff_badge_data()
        print("\n")
        print("The info provided has been added to the Badges Worksheet.\n")
        print("Please provide the info for another staff badge if required.\n")
        staff_badge_needed()


class NewStaff:
    """Adds NewStaff data to Badges worksheet"""
    def __init__(self, title, first_name, surname, role):
        self.title = title
        self.first_name = first_name
        self.surname = surname
        self.role = role

    def add_to_worksheet(self):
        BADGES_WORKSHEET.append_row(
            [self.title, self.first_name, self.surname, self.role])


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
    gspread_reminder = reminder.strftime("%d/%m/%Y")
    return gspread_reminder


def confirmation(message, spreadsheet_to_update, cell_range):
    """
    Enables user to say if they have done a task.
    If the input is not Y or N, loops back to ask again.
    If Y, updates spreadsheet and confirms with print statement.
    If N, reminds them to do asap.
    """
    while True:
        is_completed = input(f"{message} Y/N \n")
        if check_y_n(is_completed):
            break
    if is_completed == "N":
        print("Please ensure you do this as soon as possible.\n")
        print("Once done, manually update the tracking spreadsheet.\n")
        print("\n")
    elif is_completed == "Y":
        spreadsheet_to_update.update(f'{cell_range}',
                                     [[gspread_date, ENTERED_EMAIL]])
        print("The task on the spreadsheet has been updated as complete. \n")
        print("\n")


async def main():
    """
    Runs all functions for the programe to work
    """
    print("Please specify the type of event that you are planning.")
    print("* This could be 'Open Day' or 'Prep'.")
    print("* Please ensure you use initial caps.\n")
    get_event_type()
    confirm_date()
    get_email()
    create_spreadsheet()
    if EVENT_TYPE == "Prep":
        global prep_tasks
        prep_tasks = create_worksheet('Task Planner',
                                      prep_tasks_data,
                                      'E')
        create_worksheet('Attendees', attendees_data, 'I')
        create_worksheet('Stock Take', stock_data, 'D')
        sheet_one = SPREADSHEET.get_worksheet(0)
        SPREADSHEET.del_worksheet(sheet_one)
        today_date = datetime.now()
        global gspread_date
        gspread_date = today_date.strftime("%d/%m/%Y")
        prep_tasks.update('B2:B30', [[gspread_date],
                                     [gspread_date],
                                     [gspread_date],
                                     [gspread_date],
                                     [gspread_date],
                                     [calculate_reminder(120)],
                                     [calculate_reminder(120)],
                                     [calculate_reminder(120)],
                                     [calculate_reminder(90)],
                                     [calculate_reminder(90)],
                                     [calculate_reminder(90)],
                                     [calculate_reminder(80)],
                                     [calculate_reminder(75)],
                                     [calculate_reminder(75)],
                                     [calculate_reminder(60)],
                                     [calculate_reminder(60)],
                                     [calculate_reminder(60)],
                                     [calculate_reminder(60)],
                                     [calculate_reminder(30)],
                                     [calculate_reminder(30)],
                                     [calculate_reminder(10)],
                                     [calculate_reminder(7)],
                                     [calculate_reminder(7)],
                                     [calculate_reminder(4)],
                                     [calculate_reminder(3)],
                                     [calculate_reminder(1)],
                                     [calculate_reminder(1)],
                                     [calculate_reminder(1)],
                                     [calculate_reminder(-5)]])
        # https://docs.python.org/3/library/asyncio.html
        print(
            "You will now have been shared a planning spreadsheet.\n")
        await asyncio.sleep(1)
        confirmation("Have you selected an image?",
                     prep_tasks, 'C2:D2')
        await asyncio.sleep(3)
        confirmation("Have you added this event to the website?",
                     prep_tasks, 'C3:D3')
        await asyncio.sleep(3)
        confirmation("Have you added this event to the booking form?",
                     prep_tasks, 'C4:D4')
        await asyncio.sleep(3)
    elif EVENT_TYPE == "Open Day":
        global task_worksheet
        task_worksheet = create_worksheet('Task Planner', tasks_data, 'E')
        create_worksheet('Attendees', attendees_data, 'I')
        create_worksheet('Stock Take', stock_data, 'D')
        global BADGES_WORKSHEET
        BADGES_WORKSHEET = create_worksheet('Badges', badges_data, 'D')
        staff_badge_needed()
        sheet_one = SPREADSHEET.get_worksheet(0)
        SPREADSHEET.del_worksheet(sheet_one)
        today_date = datetime.now()
        gspread_date = today_date.strftime("%d/%m/%Y")
        task_worksheet.update('B2:B27', [[gspread_date],
                                         [gspread_date],
                                         [gspread_date],
                                         [gspread_date],
                                         [gspread_date],
                                         [calculate_reminder(120)],
                                         [calculate_reminder(90)],
                                         [calculate_reminder(90)],
                                         [calculate_reminder(90)],
                                         [calculate_reminder(80)],
                                         [calculate_reminder(75)],
                                         [calculate_reminder(75)],
                                         [calculate_reminder(60)],
                                         [calculate_reminder(60)],
                                         [calculate_reminder(60)],
                                         [calculate_reminder(60)],
                                         [calculate_reminder(30)],
                                         [calculate_reminder(30)],
                                         [calculate_reminder(10)],
                                         [calculate_reminder(7)],
                                         [calculate_reminder(4)],
                                         [calculate_reminder(3)],
                                         [calculate_reminder(1)],
                                         [calculate_reminder(1)],
                                         [calculate_reminder(1)],
                                         [calculate_reminder(-5)]],)
        print("You will now have been shared a planning spreadsheet.\n")
        await asyncio.sleep(1)
        confirmation("Has an image been selected?",
                     task_worksheet, 'C2:D2')
        await asyncio.sleep(3)
        confirmation("Have you added this event to the website?",
                     task_worksheet, 'C3:D3')
        await asyncio.sleep(3)
        confirmation("Have you added this event to the booking form?",
                     task_worksheet, 'C4:D4')
        await asyncio.sleep(3)
    print("Please ensure you also do the following asap:\n")
    await asyncio.sleep(3)
    print("* Create a zap to link form to the new Attendees worksheet.\n")
    await asyncio.sleep(3)
    print("* Create a zap to receive reminders.\n")
    await asyncio.sleep(3)
    print("* Ensure you initial and date when these are complete.\n")
    await asyncio.sleep(3)
    print("* Please check the spreadsheet for future due dates.\n")
    await asyncio.sleep(3)
    print("We hope this helps with your planning.\n")
    await asyncio.sleep(3)
    print("Please refresh the page to plan another event.\n")
    await asyncio.sleep(3)

asyncio.run(main())
