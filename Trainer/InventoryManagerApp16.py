import tkinter as tk
from tkinter import ttk, messagebox
import json
from pprint import pprint

# Filepath for the JSON data
JSON_FILE_PATH = "Training_Datasets/Day3/inventory_levels.json"

class InventoryManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Manager")
        self.geometry("800x600")

        # Load data
        self.inventory_data = self.load_inventory()

        # Create UI elements
        self.create_widgets()

    def load_inventory(self):
        """
        Load the inventory data from the JSON file.
        """
        try:
            with open(JSON_FILE_PATH, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return []
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")
            return []

    def save_inventory(self):
        """
        Save the inventory data back to the JSON file.
        """
        with open(JSON_FILE_PATH, 'w') as file:
            json.dump(self.inventory_data, file, indent=4)
        messagebox.showinfo("Success", "Inventory saved successfully.")

    def create_widgets(self):
        """
        Create the main UI widgets.
        """
        # Treeview for displaying inventory
        self.tree = ttk.Treeview(self, columns=("Category", "Product_Type", "Stock_Level", "Reorder_Threshold"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview()

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Item", command=self.add_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Item", command=self.update_item).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Item", command=self.delete_item).pack(side="left", padx=5)

    def update_treeview(self):
        """
        Update the treeview with the current inventory data.
        """
        self.tree.delete(*self.tree.get_children())
        for item in self.inventory_data:
            self.tree.insert("", "end", values=(item["Category"], item["Product_Type"], item["Stock_Level"], item["Reorder_Threshold"]))

    def add_item(self):
        """
        Add a new item to the inventory.
        """
        self.edit_item_window(is_update=False)

    def update_item(self):
        """
        Update the selected item in the inventory.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return

        item_values = self.tree.item(selected_item, "values")
        self.edit_item_window(is_update=True, item_values=item_values)

    def delete_item(self):
        """
        Delete the selected item from the inventory.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return

        item_values = self.tree.item(selected_item, "values")
        self.inventory_data = [item for item in self.inventory_data if item["Product_Type"] != item_values[1]]
        self.update_treeview()
        self.save_inventory()

    def edit_item_window(self, is_update, item_values=None):
        """
        Open a window for adding or updating an item.
        """
        window = tk.Toplevel(self)
        window.title("Edit Item" if is_update else "Add Item")

        fields = ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"]
        entries = {}

        for field in fields:
            ttk.Label(window, text=field).pack(pady=5)
            entry = ttk.Entry(window)
            entry.pack(pady=5)
            entries[field] = entry

        if is_update and item_values:
            for field, value in zip(fields, item_values):
                entries[field].insert(0, value)

        def save():
            new_item = {field: entries[field].get() for field in fields}

            # Validate inputs
            try:
                new_item["Stock_Level"] = int(new_item["Stock_Level"])
                new_item["Reorder_Threshold"] = int(new_item["Reorder_Threshold"])
            except ValueError:
                messagebox.showerror("Error", "Stock_Level and Reorder_Threshold must be integers.")
                return

            if is_update:
                for item in self.inventory_data:
                    if item["Product_Type"] == item_values[1]:
                        item.update(new_item)
                        break
            else:
                self.inventory_data.append(new_item)

            self.update_treeview()
            self.save_inventory()
            window.destroy()

        ttk.Button(window, text="Save", command=save).pack(pady=10)

if __name__ == "__main__":
    app = InventoryManagerApp()
    app.mainloop()
