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
    Get sales figures input from user.
    Run a while loop to collect a valid atring of data from the user
    via terminal, wich must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six number, separated by commas.")
        print("Example: 10,20,30,40,50,60")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raise ValueError if strings cannot be converted into int,
    or if there aren´t exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

def update_worksheet(data, worksheet):
    """
    Update worksheets, add new row with the result of the data privided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet update successfully.\n")

def calculate_superplus_data(sales_row):
    """
    Compare sales with stock and calculate the superplus for each items type

    The superplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indecates waste
    - Negative surplus indicates extra made when stock was sold out
    """
    print("Calculating superplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    superplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        superplus = int(stock) - sales
        superplus_data.append(superplus)
    
    return superplus_data

def get_last_5_entries_sales():
    """
    Collect collumns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of list
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return(columns)

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")    
    new_superplus_data = calculate_superplus_data(sales_data)
    update_worksheet(new_superplus_data, "surplus")


print("Welcome to Love Sandwiches Data Automation")
main()
sales_columns = get_last_5_entries_sales()