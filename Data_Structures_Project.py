# * FILE : Data_Structures_Project.py
# * PROJECT : SENG1070 - Project
# * PROGRAMMER : Mohammed Al-Fakih Student
# * FIRST VERSION : 2025-08-10
# * DESCRIPTION :
# * Income Manager

import csv 
import logging
import re
from tkinter import *
from tkinter import messagebox
from datetime import datetime

# FUNCTION : calculate
# DESCRIPTION :
# Makes a digit to a percentage
# PARAMETERS : 
# float : distribution, the amount to convert to percentage
# RETURNS :
# float : the percentage
def calculate(distribution):
    return distribution / 100

# FUNCTION : check_value
# DESCRIPTION :
# Checks if value passed is within range of 0 and 100, else it returns false
# PARAMETERS : 
# float : the value to check
# RETURNS :
# float : the actual value if value is within 0 and 100
def check_value(value):
    if is_number(value):
        value = float(value)
        return 0 <= value <= 100
    
    logging.warning("Category value is not within range 0 and 100")   
    return False

# FUNCTION : check_distribution
# DESCRIPTION :
# Checks if the total distribution of percetages for categories is equal to %100
# PARAMETERS : 
# float : 3 floats of each category
# RETURNS :
# bool : true or false if condition is met or not
def check_distribution(personal, needs, investment):
    
    if personal < 0 or needs < 0 or investment < 0:
        result_label.config(text="Invalid input! Please enter a valid percentage between 0 and 100.", fg="red")
        logging.error("A category is less than 0")  
    else:

        distribution = personal + needs + investment

        if distribution != 100:
            result_label.config(text="Distribution total must be %100", fg="red")
            logging.warning("Distribution of percentages is not equal to %100")  
            return False
        else:
            return True

# FUNCTION : percentage
# DESCRIPTION :
# Shows all percentage distributions for each category
# PARAMETERS : 
# float : 3 floats of each category
# float : the entry amount
# RETURNS :
# NONE
def percentage(personal, needs, investment, value):

    # Check if entry is a digit, and check if each category is a digit and within range 0 to 100
    # Then get the percetages for each category and show final calculations and add them to csv file
    if is_number(value):
        if float(value) > 0:
            if check_value(personal) and check_value(needs) and check_value(investment):
                if check_distribution(float(personal), float(needs), float(investment)):

                    value = float(value)
                    personal_amount = calculate(float(personal)) * value
                    needs_amount = calculate(float(needs)) * value
                    investment_amount = calculate(float(investment)) * value

                    result_label.config(
                        text=f"Distribution:\n\n"
                            f"Personal Amount: ${personal_amount:.2f}\n"
                            f"Needs Amount: ${needs_amount:.2f}\n"
                            f"Investment Amount: ${investment_amount:.2f}",
                            fg="green"
                    )

                    add_entry(personal_amount, needs_amount, investment_amount, value, "history.csv")
            else:
                result_label.config(text="Invalid input! Please enter a valid percentage between 0 and 100.", fg="red")
                logging.warning("User entered an invaild value not between 0 and 100")  

        else:
            result_label.config(text="Invalid input! Please enter a valid ammount", fg="red")
            logging.warning("User entered a negative input to: Entry Amount")  

    else:
        result_label.config(text="Invalid input! Please enter a valid ammount", fg="red")


# FUNCTION : is_number
# DESCRIPTION :
# Checks if input is a digit or not
# PARAMETERS : 
# string : the value to check
# RETURNS :
# bool : true or false if condition is met or not
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        logging.error("Failed, user entered a non-digit character")  
        return False

# FUNCTION : create_csv
# DESCRIPTION :
# Creates a csv file
# PARAMETERS : 
# string : name of the file
# RETURNS :
# NONE
def create_csv(filename):
    try:
        with open(filename, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Entry Amount", "Personal", "Needs", "Investments", "Date"])
    except FileExistsError:
        logging.error("Failed to create csv file")  

# FUNCTION : add_entry
# DESCRIPTION :
# Adds entry to csv file
# PARAMETERS : 
# floats : each of category
# string : file name
# RETURNS :
# NONE
def add_entry(personal, needs, investment, amount, filename):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, personal, needs, investment, date_now])

# FUNCTION : show_history
# DESCRIPTION :
# Shows entries' history
# PARAMETERS : 
# NONE
# RETURNS :
# NONE
def show_history():
    try:
        with open("history.csv", "r") as file:
            reader = csv.reader(file)
            rows = list(reader)

        if not rows:
            messagebox.showinfo("History", "No history found.")
            return

        history_text = "\n".join([", ".join(row) for row in rows])
        messagebox.showinfo("Calculation History", history_text)

    except FileNotFoundError:
        messagebox.showerror("Error", "History file not found.")
        logging.error("Failed open csv file, not found")

# FUNCTION : search
# DESCRIPTION :
# Shows for specific date and shows all enteries on that date
# PARAMETERS : 
# date : the date
# string : the error message
# string : the result for searching enteries if found
# RETURNS :
# NONE
def search(date, error_message, results_text):

    # Clears pervious messages
    results_text.delete("1.0", END)  
    error_message.config(text="") 
    try:
        matched_rows = []

        with open("history.csv", "r") as file:
            reader = csv.DictReader(file)
            pattern = r"\d{4}[/-]\d{2}[/-]\d{2}"

            # If the date that the user entered matches the regex date format, then proceed
            if bool(re.match(pattern, date)):
                for row in reader:
                    full_date = row["Date"] 
                    date_only = full_date.split()[0]  
                    changed_format = ""

                    # Converts / with - so it matches the format needed if the user used / instead
                    for character in date:
                        if character == "/":
                            character = "-"
                        changed_format += character
                    if changed_format == date_only:
                        matched_rows.append(row)

            else:
              
                error_message.config(text="Invalid date format. please enter format of yyyy-mm-dd or yyyy/mm/dd", fg="red")

                logging.error("Invalid date format")

        # Show all matched dates
        if matched_rows:
        
            history_text = ""
            for i, row in enumerate(matched_rows, 1):
                history_text += (
                    f"Entry {i}:\n"
                    f"  Entry Amount: ${row['Entry Amount']}\n"
                    f"  Personal: ${row['Personal']}\n"
                    f"  Needs: ${row['Needs']}\n"
                    f"  Investments: ${row['Investments']}\n"
                    f"  Date: {row['Date']}\n\n"
                )
            results_text.insert(END, history_text)

        else:
            results_text.insert(END, "No entries found for that date.")

    except FileNotFoundError:
        messagebox.showerror("Error", "History file not found.")
        logging.error("Failed open csv file, not found")

# FUNCTION : search_for_history
# DESCRIPTION :
# Shows all entries' history
# PARAMETERS : 
# NONE
# RETURNS :
# NONE
def search_for_history():

    history_win = Toplevel(window)
    history_win.title("View History by Date")
    history_win.geometry("700x600")

    Label(history_win, text="Enter date (YYYY-MM-DD):").pack(pady=5)

    input_frame = Frame(history_win)
    input_frame.pack(pady=5)

    date_entry = Entry(input_frame)
    date_entry.pack(pady=5)

    error_message = Label(history_win, text="", font=("Arial", 12), fg="red", justify=LEFT)
    error_message.pack(pady=20)

    results_text = Text(history_win, height=15, width=60)
    results_text.pack(pady=10)

    show_history_button = Button(input_frame, text="Search", command=lambda: search(date_entry.get(), error_message, results_text))
    show_history_button.pack(pady=15) 

# FUNCTION : Create_logger
# DESCRIPTION :
# Creates a logger file
# PARAMETERS : 
# NONE
# RETURNS :
# NONE
def create_logger():

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('log.log', mode='a')  
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logging.info("Application started")

# FUNCTION : bubble_sort_csv
# DESCRIPTION :
# Sorts csv file by date
# PARAMETERS : 
# string : the file
# string : the column in which the csv will be sorted (Date)
# RETURNS :
# NONE
def bubble_sort_csv(file_path, sort_column="Entry Amount"):
    with open(file_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = reader.fieldnames

    n = len(rows)

    for i in range(n):
        for j in range(0, n - i - 1):
            try:
                val1 = float(rows[j][sort_column].replace("$", ""))
            except (ValueError, KeyError):
                val1 = 0.0

            try:
                val2 = float(rows[j + 1][sort_column].replace("$", ""))
            except (ValueError, KeyError):
                val2 = 0.0

            if val1 < val2:
                rows[j], rows[j + 1] = rows[j + 1], rows[j]

    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    messagebox.showinfo("CSV Sorted", "History.csv sorted by Entry Amount (highest → lowest).")

create_logger()
create_csv("history.csv")

window = Tk()
window.title("Income Manager")
window.geometry("700x600")

Label(window, text="Income Manager", font=("Arial", 14)).pack(pady=10)

#-------------------------------------------------------------------------------------------------

# Create the bar for entry amount
amount_frame = Frame(window)
amount_frame.pack(pady=5)
Label(amount_frame, text="Enter Amount $:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
amount = Entry(amount_frame)
amount.grid(row=0, column=1, padx=5, pady=5)

#-------------------------------------------------------------------------------------------------

# Create percetage enteries for each category

percent_frame = Frame(window)
percent_frame.pack(pady=10)

Label(percent_frame, text="Personal %:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_personal = Entry(percent_frame, width=5)
entry_personal.grid(row=0, column=1, padx=5)

Label(percent_frame, text="Needs %:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_needs = Entry(percent_frame, width=5)
entry_needs.grid(row=1, column=1, padx=5)

Label(percent_frame, text="Investment %:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
entry_investment = Entry(percent_frame, width=5)
entry_investment.grid(row=2, column=1, padx=5)

#-------------------------------------------------------------------------------------------------

# Create buttons for submission and history view
Button(
    amount_frame,
    text="Submit",
    command=lambda: percentage(
        entry_personal.get(),
        entry_needs.get(),
        entry_investment.get(),
        amount.get()
    )
).grid(row=0, column=2, padx=10)

sort_button = Button(window, text="Sort CSV", command=lambda: bubble_sort_csv("history.csv", sort_column="Entry Amount"))
sort_button.pack(pady=30)

history_button = Button(window, text="Show History", command=show_history)
history_button.pack(pady=10)

show_history_button = Button(window, text="Search Income Info by History", command=search_for_history)
show_history_button.pack(pady=15)

result_label = Label(window, text="", font=("Arial", 12), fg="red", justify=LEFT)
result_label.pack(pady=20)

window.mainloop()
