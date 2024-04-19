import tkinter as tk
from tkinter import ttk, filedialog
import csv

def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = combo_operation.get()

        if operation == "Addition":
            result = num1 + num2
        elif operation == "Subtraction":
            result = num1 - num2
        elif operation == "Multiplication":
            result = num1 * num2
        elif operation == "Division":
            result = num1 / num2
        else:
            result = "Invalid Operation"

        result_label.config(text=f"Result: {result}")

    except ValueError:
        result_label.config(text="Invalid input. Please enter valid numbers.")

def process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    if file_path:
        try:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Skip header
                column_index = 0  # Change this to the desired column index

                total = sum(float(row[column_index]) for row in reader)

            result_label_csv.config(text=f"Sum of column {column_index + 1}: {total}")

        except Exception as e:
            result_label_csv.config(text=f"Error processing CSV: {str(e)}")

# Create the main window
app = tk.Tk()
app.title("Calculator & CSV Processor App")

# Create entry widgets for numbers
entry_num1 = ttk.Entry(app)
entry_num2 = ttk.Entry(app)

# Create a combo box for selecting the operation
operations = ["Addition", "Subtraction", "Multiplication", "Division"]
combo_operation = ttk.Combobox(app, values=operations)
combo_operation.set("Addition")  # Default operation

# Create a button to trigger the calculation
calculate_button = ttk.Button(app, text="Calculate", command=calculate)

# Create a label to display the result
result_label = ttk.Label(app, text="Result: ")

# Create a button to process CSV
process_csv_button = ttk.Button(app, text="Process CSV", command=process_csv)

# Create a label to display CSV processing result
result_label_csv = ttk.Label(app, text="")

# Grid layout
entry_num1.grid(row=0, column=0, padx=10, pady=10)
combo_operation.grid(row=0, column=1, padx=10, pady=10)
entry_num2.grid(row=0, column=2, padx=10, pady=10)
calculate_button.grid(row=1, column=0, columnspan=3, pady=10)
result_label.grid(row=2, column=0, columnspan=3, pady=10)
process_csv_button.grid(row=3, column=0, columnspan=3, pady=10)
result_label_csv.grid(row=4, column=0, columnspan=3, pady=10)

# Run the application
app.mainloop()
