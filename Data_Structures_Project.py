from tkinter import *

def calculate(distribution):
        return distribution / 100
         
def on_click():
    value = entry.get()
    if is_number(value):
        value = float(value)
        if value < 0 or value >= 100:
            result_label.config(text="Negative or too Large Input")
        else:
            result = calculate(float(value))
            result_label.config(text=f"Result: {result}")  
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

input_frame = Frame(window)
input_frame.pack(pady=10)

label2 = Label(input_frame, text="Enter Amount:", font=("Arial", 11))
label2.pack(side=LEFT, padx=5)

entry = Entry(input_frame)
entry.pack(side=LEFT, padx=1)

# Label(window, text="Last Name:")
# entry2 = Entry(window)
# entry2.pack(side=RIGHT, pady=15, padx=50)

# Label(window, text="Age:")
# entry3 = Entry(window)
# entry3.pack(side=LEFT, pady=30, padx=50)

button = Button(input_frame, text="Submit", command=on_click)
button.pack(side=LEFT, padx=5)

result_label = Label(window, text="", font=("Arial", 12), fg="red")
result_label.pack()

window.mainloop()
