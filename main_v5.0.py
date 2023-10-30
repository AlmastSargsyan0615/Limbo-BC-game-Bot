import pyautogui
import pyperclip
import time
import pytesseract
import re
import pandas as pd
from datetime import datetime
import keyboard
import os
import shutil
from bs4 import BeautifulSoup

#position for clicking in crash
crash_amount_x, crash_amount_y = 175, 777
crash_payout_x, crash_payout_y = 503, 777
crash_btn_x, crash_btn_y = 468, 672

crash_amount = 200
crash_payout = 2.5

#position for clicking in trenball
trenball_amount_x, trenball_amount_y = 170, 680

trenball_btn_red_x, trenball_btn_red_y = 235, 800
trenball_btn_blue_x, trenball_btn_blue_y = 470, 800
trenball_btn_yellow_x, trenball_btn_yellow_y = 670, 800

trenball_amount = 150

#position for clicking to switch
to_trenball_x, to_trenball_y = 790, 205
to_crash_x, to_crash_y = 690, 205


# position for clicking in inspector
right_click_point = (1059, 507)  # Change these coordinates to your special points
left_click_point = (1120, 630)  # Change these coordinates to your special points

# Define the input_issus to start with
input_issus = '6315727'

# Initialize neighboring_value to None
neighboring_value = None

# Number of iterations
num_iterations = 15000

# Specify the desired Excel filename
excel_filename = 'LatestDB.xlsx'

# Create empty lists to store data
data_entries = []
data_entries_from_excel = []
latest_entries = []

# Variable to track if the Home key is pressed and extracted number is detected
stop_script = False
is_greater = False

def get_last_issus_and_neighboring_div(html_content, input_issus):
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all div elements with class "issus"
    issus_divs = soup.find_all('div', class_='issus')
   

    # Check if the list of issus_divs is not empty
    if issus_divs:
        # Get the text from the last issus div (assuming the last one is the last in the list)
        last_issus = issus_divs[-1].get_text()
        
        # Check if the last issus value is greater than the input parameter
        last_issus_value = int(last_issus)
        input_issus_value = int(input_issus)
        is_greater = last_issus_value > input_issus_value

        # Get the next div element (neighboring div) and its text
        neighboring_div = issus_divs[-1].find_next('div')
        neighboring_value = neighboring_div.get_text()
        neighboring_value = float(neighboring_value.replace("x", ""))
        return last_issus, neighboring_value, is_greater

    # Return None if no match or if the list of issus_divs is empty
    return None, None, False

# Function to right-click at the specified point
def right_click_at(point):
    pyautogui.rightClick(point)

# Function to left-click at the specified point
def left_click_at(point):
    pyautogui.leftClick(point)
           

def perform_click_and_type(position_x, position_y, click_count, input_value, sleep_time):
    # Click at the specified position
    pyautogui.click(position_x, position_y, clicks=click_count)

    # Type the input value
    pyautogui.typewrite(str(input_value))

    # Wait for the specified duration
    time.sleep(sleep_time)

def stop_program(e):
    global stop_script
    if e.name == "home":
        stop_script = True

# Register the Home key event listener
keyboard.on_press(stop_program)

# Check if "LatestDB.xlsx" exists, if yes, make a copy to "PreviousDB.xlsx"
if os.path.exists(excel_filename):
    shutil.copyfile(excel_filename, 'PreviousDB.xlsx')

# Read data from "PreviousDB.xlsx" and extract the Numbers field as an array
if os.path.exists('PreviousDB.xlsx'):
    old_data_df = pd.read_excel('PreviousDB.xlsx')
    old_data = old_data_df['Numbers'].tolist()
else:
    old_data = []


# Create a copy of oldData as total_data
total_data = old_data.copy()
####################################################
 ###### usage od old_data and total_data ###########
# i = 0
# for i in range(len(old_data)):
#     number1 = old_data[i]
#     print(f"Element at index {i}: {number}")
# i = 0
# for i in range(len(total_data)):
#     number2 = total_data[i]
#     print(f"Element at index {i}: {number}")
####################################################

time.sleep(5)
i = 0

try:
    for i in range(num_iterations):
        if stop_script:
            break  # Exit the loop if the Home key is pressed
        # Main loop
        while True:
            if stop_script:
                break  # Exit the loop if the Home key is pressed
            # Right-click, left-click, and paste
            right_click_at(right_click_point)
            time.sleep(0.5)  # Adjust sleep time if needed
            left_click_at(left_click_point)
            time.sleep(0.5)  # Adjust sleep time if needed
            html_content = pyperclip.paste()
            # Call the function to get the last issus value and other information
            last_issus_temp, neighboring_value_temp, is_greater = get_last_issus_and_neighboring_div(html_content, input_issus)

            # Exit the loop if is_greater is True
            if is_greater:
                # Update input_issus for the next iteration
                input_issus = last_issus_temp
                extracted_number = neighboring_value_temp
                break

        # =========================================CRASH
        # Click the amount in crash
        perform_click_and_type(crash_amount_x, crash_amount_y, 2, crash_amount, 0.1)

        # Click the payout  in crash
        perform_click_and_type(crash_payout_x, crash_payout_y, 2, crash_payout, 0.1)

        # Click the betting button  in crash
        perform_click_and_type(crash_btn_x, crash_btn_y, 1, "", 0.3)



        # Click to switch to trenball
        perform_click_and_type(to_trenball_x, to_trenball_y, 1, "", 0.5)


        # =========================================TRENBALL
        # Click the amount in trenball
        perform_click_and_type(trenball_amount_x, trenball_amount_y, 2, trenball_amount, 0.1)

        # Click the red button  in trenball
        perform_click_and_type(trenball_btn_red_x, trenball_btn_red_y, 1, "", 0.3)

        # Click the blue button  in trenball
        perform_click_and_type(trenball_btn_blue_x, trenball_btn_blue_y, 1, "", 0.3)

        # Click the yellow button  in trenball
        # perform_click_and_type(trenball_btn_yellow_x, trenball_btn_yellow_y, 1, "", 0.3)

        time.sleep(1)

        # Click to switch to crash
        perform_click_and_type(to_crash_x, to_crash_y, 1, "", 0.5)


        if crash_payout > extracted_number : 
            bet_result = False
        else: bet_result = True
        
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Append data to the data_entries list
        data_entry = {
            'Date': timestamp,
            'Numbers': extracted_number,
            'Bet amount': crash_amount,
            'Bet rate': crash_payout,
            'Result': bet_result
        }
        data_entries.append(data_entry)
        total_data.append(extracted_number)

        # Print the data in the command line
        data_entry_str = f"{i} - Date: {timestamp} - Numbers: {extracted_number} - Bet amount: {crash_amount} - Bet rate: {crash_payout} - Result: {bet_result}"
        print(data_entry_str)


except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print(f"Completed!")

    if os.path.exists(excel_filename):
            # Read the data from the Excel file
            df = pd.read_excel(excel_filename)

            # Create an empty list to store the data in the same format as data_entries
            data_entries_from_excel = []

            # Loop through the rows and format the data
            for index, row in df.iterrows():
                data_entry = {
                    'Date': row['Date'],
                    'Numbers': row['Numbers'],
                    'Bet amount': row['Bet amount'],
                    'Bet rate': row['Bet rate'],
                    'Result': row['Result']
                }
                data_entries_from_excel.append(data_entry)

            # Now, data_entries_from_excel contains the data in the same format as data_entries
            # print(data_entries_from_excel)
            latest_entries = data_entries_from_excel + data_entries
            data_entries = []
            data_entries = latest_entries

    # Create a DataFrame from the data_entries list
    df = pd.DataFrame(data_entries)

    # Save the DataFrame to the Excel file
    df.to_excel(excel_filename, index=False)

    print(f'Extracted data saved to "{excel_filename}"')



