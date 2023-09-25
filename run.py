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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect valid data string data from user
    via terminal. If not 6 comma separated integers will throw
    errors until a valid data entry is made
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, seperated by commas")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter your data here :")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, convert strings to integers.
    Raises ValueError if strings cant be integers, or if not 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError("Exactly 6 values are required, you provided "
                             f"{len(values)}")                          
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet with new row after list data provided
    """
    print("Updating sales worksheet")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Update made successfully.\n")


data = get_sales_data()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)

