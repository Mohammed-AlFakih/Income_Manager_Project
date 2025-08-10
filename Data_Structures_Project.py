import csv
from tkinter import *
from tkinter import messagebox
from datetime import datetime

def calculate(distribution):
    return distribution / 100

def check_value(value):
    if is_number(value):
        value = float(value)
        return 0 <= value <= 100
    return False

def check_distribution(personal, needs, investment):

    distribution = personal + needs + investment

    if distribution != 100:
        result_label.config(text="Distribution total must be %100")
        return False
    else:
        return True

def percentage(personal, needs, investment, value):
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
                            f"Investment Amount: ${investment_amount:.2f}"
                    )

                    add_entry(personal_amount, needs_amount, investment_amount, value, "history.csv")
            else:
                result_label.config(text="Invalid input! Please enter a valid percentage between 0 and 100.")
        else:
         result_label.config(text="Invalid input! Please enter a valid ammount")
    else:
        result_label.config(text="Invalid input! Please enter a valid ammount")

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    
def create_csv(filename):
    try:
        with open(filename, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Entry Amount", "Personal", "Needs", "Investments", "Date"])
    except FileExistsError:
        pass  

def add_entry(personal, needs, investment, amount, filename):
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, personal, needs, investment, date_now])

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

window = Tk()
window.title("Income Manager")
window.geometry("500x400")

Label(window, text="Income Manager", font=("Arial", 14)).pack(pady=10)

#-------------------------------------------------------------------------------------------------
amount_frame = Frame(window)
amount_frame.pack(pady=5)
Label(amount_frame, text="Enter Amount $:", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
amount = Entry(amount_frame)
amount.grid(row=0, column=1, padx=5, pady=5)

#-------------------------------------------------------------------------------------------------
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

history_button = Button(window, text="Show History", command=show_history)
history_button.pack(pady=10)

# Result label
result_label = Label(window, text="", font=("Arial", 12), fg="red", justify=LEFT)
result_label.pack(pady=20)

create_csv("history.csv")

window.mainloop()
