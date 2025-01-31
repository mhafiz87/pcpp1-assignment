import tkinter as tk

entries = []  # Store all entries

def add_entry():
    machine_id = entry_machine_id.get()
    equipment_type = entry_equipment_type.get()
    run_duration = int(entry_duration.get())
    units_per_day = int(entry_units_per_day.get())

    if not machine_id or not equipment_type or not run_duration or not units_per_day:
        error_label.config(text="All fields are required!")
        return

    total_units = run_duration * units_per_day
    entry = {"machine_id": machine_id, "equipment_type": equipment_type, "total_units": total_units}
    entries.append(entry)

    listbox.insert(tk.END, f"{machine_id} | {equipment_type} | {total_units} units")
    error_label.config(text="")

def filter_entries():
    threshold = int(entry_threshold.get())
    listbox.delete(0, tk.END)
    for entry in entries:
        if entry["total_units"] > threshold:
            listbox.insert(tk.END, f"{entry['machine_id']} | {entry['equipment_type']} | {entry['total_units']} units")

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

# Add Entry Button
tk.Button(root, text="Add Entry", command=add_entry).pack()

# Error Label
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# Listbox for Entries
listbox = tk.Listbox(root, width=50)
listbox.pack()

# Threshold Filter
tk.Label(root, text="Filter by Total Units Produced (Threshold)").pack()
entry_threshold = tk.Entry(root)
entry_threshold.pack()
tk.Button(root, text="Filter", command=filter_entries).pack()

root.mainloop()
