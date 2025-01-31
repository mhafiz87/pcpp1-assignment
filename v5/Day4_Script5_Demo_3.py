import tkinter as tk
import sqlite3
import logging

# Configure logging
logging.basicConfig(filename="Training_Datasets/Day4/capstone_logs.log", level=logging.INFO)

# Initialize Database
def initialize_database():
    conn = sqlite3.connect("capstone_project.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Production (
        Machine_ID TEXT,
        Equipment_Type TEXT,
        Run_Start TEXT,
        Run_End TEXT,
        Units_Produced INTEGER
    )
    """)
    conn.commit()
    conn.close()

def insert_production(machine_id, equipment_type, run_start, run_end, units_produced):
    conn = sqlite3.connect("capstone_project.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO Production (Machine_ID, Equipment_Type, Run_Start, Run_End, Units_Produced)
    VALUES (?, ?, ?, ?, ?)
    """, (machine_id, equipment_type, run_start, run_end, units_produced))

    conn.commit()
    conn.close()
    logging.info(f"Inserted production data: {machine_id}, {units_produced} units.")

def add_production_entry():
    machine_id = entry_machine_id.get()
    equipment_type = entry_equipment_type.get()
    run_start = entry_run_start.get()
    run_end = entry_run_end.get()
    units_produced = int(entry_units_produced.get())

    insert_production(machine_id, equipment_type, run_start, run_end, units_produced)
    listbox.insert(tk.END, f"{machine_id} | {equipment_type} | {units_produced} units")

# GUI Setup
root = tk.Tk()
root.title("Capstone Project: Production Management")

# Input Fields
tk.Label(root, text="Machine ID").pack()
entry_machine_id = tk.Entry(root)
entry_machine_id.pack()

tk.Label(root, text="Equipment Type").pack()
entry_equipment_type = tk.Entry(root)
entry_equipment_type.pack()

tk.Label(root, text="Run Start").pack()
entry_run_start = tk.Entry(root)
entry_run_start.pack()

tk.Label(root, text="Run End").pack()
entry_run_end = tk.Entry(root)
entry_run_end.pack()

tk.Label(root, text="Units Produced").pack()
entry_units_produced = tk.Entry(root)
entry_units_produced.pack()

tk.Button(root, text="Add Entry", command=add_production_entry).pack()

# Listbox to Display Entries
listbox = tk.Listbox(root, width=60)
listbox.pack()

# Initialize Database and Start GUI
initialize_database()
root.mainloop()
