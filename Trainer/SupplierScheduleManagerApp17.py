import tkinter as tk
from tkinter import ttk, messagebox
import xml.etree.ElementTree as ET
from datetime import datetime

# Filepath for the XML data
XML_FILE_PATH = "Training_Datasets/Day2/supplier_schedule.xml"

class SupplierManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supplier Manager")
        self.geometry("900x600")

        # Load data
        self.supplier_data = self.load_suppliers()

        # Create UI elements
        self.create_widgets()

    def load_suppliers(self):
        """
        Load the supplier data from the XML file.
        """
        try:
            tree = ET.parse(XML_FILE_PATH)
            root = tree.getroot()
            data = []
            for schedule in root.findall("Schedule"):
                data.append({
                    "Supplier_ID": schedule.find("Supplier_ID").text,
                    "Material_Type": schedule.find("Material_Type").text,
                    "Delivery_Date": schedule.find("Delivery_Date").text
                })
            return data
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
            return []
        except ET.ParseError:
            messagebox.showerror("Error", "Invalid XML format.")
            return []

    def save_suppliers(self):
        """
        Save the supplier data back to the XML file.
        """
        root = ET.Element("SupplierSchedules")
        for supplier in self.supplier_data:
            schedule_element = ET.SubElement(root, "Schedule")
            ET.SubElement(schedule_element, "Supplier_ID").text = supplier["Supplier_ID"]
            ET.SubElement(schedule_element, "Material_Type").text = supplier["Material_Type"]
            ET.SubElement(schedule_element, "Delivery_Date").text = supplier["Delivery_Date"]

        tree = ET.ElementTree(root)
        tree.write(XML_FILE_PATH, encoding="utf-8", xml_declaration=True)
        messagebox.showinfo("Success", "Suppliers saved successfully.")

    def create_widgets(self):
        """
        Create the main UI widgets.
        """
        # Treeview for displaying suppliers
        self.tree = ttk.Treeview(self, columns=("Supplier_ID", "Material_Type", "Delivery_Date"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview()

        # Buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Add Supplier", command=self.add_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Supplier", command=self.update_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Supplier", command=self.delete_supplier).pack(side="left", padx=5)

    def update_treeview(self):
        """
        Update the treeview with the current supplier data.
        """
        self.tree.delete(*self.tree.get_children())
        for supplier in self.supplier_data:
            self.tree.insert("", "end", values=(supplier["Supplier_ID"], supplier["Material_Type"], supplier["Delivery_Date"]))

    def add_supplier(self):
        """
        Add a new supplier to the data.
        """
        self.edit_supplier_window(is_update=False)

    def update_supplier(self):
        """
        Update the selected supplier in the data.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected.")
            return

        item_values = self.tree.item(selected_item, "values")
        self.edit_supplier_window(is_update=True, item_values=item_values)

    def delete_supplier(self):
        """
        Delete the selected supplier from the data.
        """
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected.")
            return

        item_values = self.tree.item(selected_item, "values")
        self.supplier_data = [supplier for supplier in self.supplier_data if supplier["Supplier_ID"] != item_values[0]]
        self.update_treeview()
        self.save_suppliers()

    def edit_supplier_window(self, is_update, item_values=None):
        """
        Open a window for adding or updating a supplier.
        """
        window = tk.Toplevel(self)
        window.title("Edit Supplier" if is_update else "Add Supplier")

        fields = ["Supplier_ID", "Material_Type", "Delivery_Date"]
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
            new_supplier = {field: entries[field].get() for field in fields}

            # Validate inputs
            if not new_supplier["Supplier_ID"] or not new_supplier["Material_Type"] or not new_supplier["Delivery_Date"]:
                messagebox.showerror("Error", "All fields are required.")
                return

            try:
                datetime.strptime(new_supplier["Delivery_Date"], "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
                return

            if is_update:
                for supplier in self.supplier_data:
                    if supplier["Supplier_ID"] == item_values[0]:
                        supplier.update(new_supplier)
                        break
            else:
                self.supplier_data.append(new_supplier)

            self.update_treeview()
            self.save_suppliers()
            window.destroy()

        ttk.Button(window, text="Save", command=save).pack(pady=10)

if __name__ == "__main__":
    app = SupplierManagerApp()
    app.mainloop()
