from tkinter import *

def calculate(distribution):
        return distribution / 100

def check_value(value):
    
    if is_number(value):
        value = float(value)
        if value < 0 or value > 100:
            return False
        else:
            return True
    else:
        return False

def percentage(personal, needs, investment, value):

    if check_value(personal) and check_value(needs) and check_value(investment) and is_number(value):
        personal_amount = calculate(float(personal)) * value
        needs_amount = calculate(float(needs)) * value
        investment_amount = calculate(float(investment)) * value

        result_label.config(
            text=f"Distribution:\n\n"
                 f"Personal Amount: ${personal_amount:.2f}\n"
                 f"Needs Amount: ${needs_amount:.2f}\n"
                 f"Investment Amount: ${investment_amount:.2f}"
        )

    else:
        result_label.config(text="Invalid input! Please numbers between 0 and 100.")


def on_click():
    value = amount.get()
    if is_number(value):
        value = float(value)
        if check_value(value):
            result = calculate(float(value))
            result_label.config(text=f"Result: {result}")
        else:
            result_label.config(text="Negative or too Large Input")
    else:
        result_label.config(text="Invalid input! Please enter a number.")

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

window = Tk()
window.title("My First Tkinter App")
window.geometry("1080x900")

label = Label(window, text="Income Manager", font=("Arial", 14))
label.pack()

#-------------------------------------------------------------------------

input_frame = Frame(window)
input_frame.pack(pady=10)

label2 = Label(input_frame, text="Enter Amount $:", font=("Arial", 11))
label2.pack(side=LEFT, padx=5)

amount = Entry(input_frame)
amount.pack(side=LEFT, padx=1)

#-------------------------------------------------------------------------

input_frame2 = Frame(window)
input_frame2.pack(padx=(1, 1), pady=20)

personal = Label(input_frame2, text="Personal %:")
personal.pack(side=LEFT, padx=0)

entry2 = Entry(input_frame2, width=3)
entry2.pack(side=RIGHT, padx=1)

#-------------------------------------------------------------------------

investment = Label(input_frame2, text="Investment %:")
investment.pack(side=RIGHT, padx=1)

entry3 = Entry(input_frame2, width=3)
entry3.pack(side=RIGHT, padx=1)

#-------------------------------------------------------------------------

needs = Label(input_frame2, text="Needs %:")
needs.pack(side=RIGHT, padx=1)

entry4 = Entry(input_frame2, width=3)
entry4.pack(side=RIGHT, padx=1)

#-------------------------------------------------------------------------

result_label = Label(window, text="", font=("Arial", 12), fg="red")
result_label.pack()

button = Button(input_frame, text="Submit", command=lambda:percentage(entry2.get(), entry3.get(), entry4.get(), amount.get()))
button.pack(side=LEFT, padx=5)


window.mainloop()
