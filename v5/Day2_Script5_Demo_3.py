import tkinter as tk
import csv

def load_data():
    with open("Training_Datasets/Day1/production_line_data.csv", mode="r") as file:
        reader = csv.DictReader(file)
        listbox.delete(0, tk.END)
        for row in reader:
            listbox.insert(tk.END, f"{row['Machine_ID']} | {row['Equipment_Type']} | {row['Units_Produced']} units")

# GUI Setup
root = tk.Tk()
root.title("Production Data Viewer")

# Load Button
tk.Button(root, text="Load Data", command=load_data).pack()

# Listbox for Data
listbox = tk.Listbox(root, width=60)
listbox.pack()

root.mainloop()
