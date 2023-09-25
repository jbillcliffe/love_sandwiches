# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
        print("Example: 10,20,30,40,50,60.\n")

        data_str = input("Enter your data here :")
        sales_data = data_str.split(",")

        if validate_data(sales_data):
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
    print("Updating sales worksheet ..... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales update made successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus for each item type
    ---
    The surplus = sales - stock
    - Positive value = waste
    - Negative = Extra made when stock ran out
    """
    print("Calculating Surplus Data .....\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # stock_row = stock[len(stock)-1]
    # 27,27,36,26,32,31
    stock_row = [int(num) for num in stock[-1]]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    print("Surplus Data Calculated.\n")
    return surplus_data


def update_surplus_worksheet(surplus_row):
    """
    Update surplus worksheet with new row after list data provided
    """
    print("Updating surplus worksheet ..... \n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(surplus_row)
    print("Surplus update made successfully.\n")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    final_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(final_surplus_data)


print("Welcome to Love Sandwiches Data Automation\n")
main()
