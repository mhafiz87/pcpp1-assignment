import tkinter as tk

def add_entry():
    machine_id = entry_machine_id.get()
    equipment_type = entry_equipment_type.get()
    run_duration = int(entry_duration.get())
    units_per_day = int(entry_units_per_day.get())
    total_units = run_duration * units_per_day
    listbox.insert(tk.END, f"{machine_id} | {equipment_type} | {total_units} units")

# GUI Setup
root = tk.Tk()
root.title("Production Data Input")

# Input Fields
tk.Label(root, text="Machine ID").pack()
entry_machine_id = tk.Entry(root)
entry_machine_id.pack()

tk.Label(root, text="Equipment Type").pack()
entry_equipment_type = tk.Entry(root)
entry_equipment_type.pack()

tk.Label(root, text="Run Duration (days)").pack()
entry_duration = tk.Entry(root)
entry_duration.pack()

tk.Label(root, text="Units Produced Per Day").pack()
entry_units_per_day = tk.Entry(root)
entry_units_per_day.pack()

# Add Button
tk.Button(root, text="Add Entry", command=add_entry).pack()

# Listbox to Display Entries
listbox = tk.Listbox(root, width=50)
listbox.pack()

root.mainloop()
