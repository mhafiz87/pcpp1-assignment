import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import json
import xml.etree.ElementTree as ET
import csv
from datetime import datetime

class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Enhanced Production Monitoring System")
        self.geometry("1280x800")
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Database connection
        self.db_connection = sqlite3.connect('Training_Datasets/Day4/maintenance_logs.db')
        self.cursor = self.db_connection.cursor()

        # Initialize data
        self.inventory_data = []
        self.supplier_data = []
        self.production_data = []
        self.maintenance_data = []

        # Create main UI
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)

        self.create_inventory_tab()
        self.create_supplier_tab()
        self.create_maintenance_tab()
        self.create_production_tab()
        self.create_summary_tab()

    # ------------------ Inventory Tab ------------------ #
    def create_inventory_tab(self):
        inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(inventory_tab, text="Inventory Management")

        ttk.Button(inventory_tab, text="Load Inventory Data", command=self.load_inventory).pack(pady=5)
        ttk.Button(inventory_tab, text="Add Inventory Item", command=self.add_inventory_item).pack(pady=5)
        ttk.Button(inventory_tab, text="Remove Selected Item", command=self.remove_inventory_item).pack(pady=5)
        ttk.Button(inventory_tab, text="Amend Selected Item", command=self.amend_inventory_item).pack(pady=5)

        self.inventory_tree = ttk.Treeview(inventory_tab, columns=("Category", "Product_Type", "Stock_Level", "Reorder_Threshold"), show="headings")
        for col in self.inventory_tree["columns"]:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, width=200, anchor="center")
        self.inventory_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_inventory(self):
        try:
            with open('Training_Datasets/Day3/inventory_levels.json', 'r') as file:
                self.inventory_data = json.load(file)
            self.update_treeview(self.inventory_tree, self.inventory_data, ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"])
            messagebox.showinfo("Success", "Inventory data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load inventory data: {e}")

    def add_inventory_item(self):
        new_item = {
            "Category": simpledialog.askstring("Input", "Enter Category:"),
            "Product_Type": simpledialog.askstring("Input", "Enter Product Type:"),
            "Stock_Level": simpledialog.askinteger("Input", "Enter Stock Level:"),
            "Reorder_Threshold": simpledialog.askinteger("Input", "Enter Reorder Threshold:")
        }
        if all(new_item.values()):
            self.inventory_data.append(new_item)
            self.update_treeview(self.inventory_tree, self.inventory_data, ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"])
            messagebox.showinfo("Success", "Inventory item added successfully!")

    def remove_inventory_item(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        item_values = self.inventory_tree.item(selected_item, "values")
        self.inventory_tree.delete(selected_item)
        self.inventory_data = [item for item in self.inventory_data if item["Product_Type"] != item_values[1]]
        messagebox.showinfo("Success", "Inventory item removed successfully!")

    def amend_inventory_item(self):
        selected_item = self.inventory_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        item_values = self.inventory_tree.item(selected_item, "values")
        amended_item = {
            "Category": simpledialog.askstring("Input", "Enter Category:", initialvalue=item_values[0]),
            "Product_Type": simpledialog.askstring("Input", "Enter Product Type:", initialvalue=item_values[1]),
            "Stock_Level": simpledialog.askinteger("Input", "Enter Stock Level:", initialvalue=int(item_values[2])),
            "Reorder_Threshold": simpledialog.askinteger("Input", "Enter Reorder Threshold:", initialvalue=int(item_values[3]))
        }
        if all(amended_item.values()):
            for i, item in enumerate(self.inventory_data):
                if item["Product_Type"] == item_values[1]:
                    self.inventory_data[i] = amended_item
                    break
            self.update_treeview(self.inventory_tree, self.inventory_data, ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"])
            messagebox.showinfo("Success", "Inventory item amended successfully!")

    # ------------------ Supplier Tab ------------------ #
    def create_supplier_tab(self):
        supplier_tab = ttk.Frame(self.notebook)
        self.notebook.add(supplier_tab, text="Supplier Management")

        ttk.Button(supplier_tab, text="Load Supplier Data", command=self.load_supplier).pack(pady=5)
        ttk.Button(supplier_tab, text="Add Supplier", command=self.add_supplier).pack(pady=5)
        ttk.Button(supplier_tab, text="Remove Selected Supplier", command=self.remove_supplier).pack(pady=5)

        self.supplier_tree = ttk.Treeview(supplier_tab, columns=("Supplier_ID", "Material_Type", "Delivery_Date"), show="headings")
        for col in self.supplier_tree["columns"]:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, width=200, anchor="center")
        self.supplier_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_supplier(self):
        try:
            tree = ET.parse('Training_Datasets/Day2/supplier_schedule.xml')
            root = tree.getroot()
            self.supplier_data = [{"Supplier_ID": schedule.find("Supplier_ID").text,
                                   "Material_Type": schedule.find("Material_Type").text,
                                   "Delivery_Date": schedule.find("Delivery_Date").text}
                                  for schedule in root.findall("Schedule")]
            self.update_treeview(self.supplier_tree, self.supplier_data, ["Supplier_ID", "Material_Type", "Delivery_Date"])
            messagebox.showinfo("Success", "Supplier data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load supplier data: {e}")

    def add_supplier(self):
        new_supplier = {
            "Supplier_ID": simpledialog.askstring("Input", "Enter Supplier ID:"),
            "Material_Type": simpledialog.askstring("Input", "Enter Material Type:"),
            "Delivery_Date": simpledialog.askstring("Input", "Enter Delivery Date (YYYY-MM-DD):")
        }
        if all(new_supplier.values()):
            self.supplier_data.append(new_supplier)
            self.update_treeview(self.supplier_tree, self.supplier_data, ["Supplier_ID", "Material_Type", "Delivery_Date"])
            messagebox.showinfo("Success", "Supplier added successfully!")

    def remove_supplier(self):
        selected_item = self.supplier_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No supplier selected.")
            return
        item_values = self.supplier_tree.item(selected_item, "values")
        self.supplier_tree.delete(selected_item)
        self.supplier_data = [supplier for supplier in self.supplier_data if supplier["Supplier_ID"] != item_values[0]]
        messagebox.showinfo("Success", "Supplier removed successfully!")

    # ------------------ Maintenance Tab ------------------ #
    def create_maintenance_tab(self):
        maintenance_tab = ttk.Frame(self.notebook)
        self.notebook.add(maintenance_tab, text="Maintenance Logs")

        ttk.Button(maintenance_tab, text="Load Maintenance Logs", command=self.load_maintenance).pack(pady=5)
        ttk.Button(maintenance_tab, text="Add Maintenance Log", command=self.add_maintenance_log).pack(pady=5)
        ttk.Button(maintenance_tab, text="Remove Selected Log", command=self.remove_maintenance_log).pack(pady=5)
        ttk.Button(maintenance_tab, text="Check Overdue Maintenance", command=self.check_maintenance_alerts).pack(pady=5)

        self.maintenance_tree = ttk.Treeview(maintenance_tab, columns=("Machine_ID", "Maintenance_Date", "Details"), show="headings")
        for col in self.maintenance_tree["columns"]:
            self.maintenance_tree.heading(col, text=col)
            self.maintenance_tree.column(col, width=200, anchor="center")
        self.maintenance_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_maintenance(self):
        try:
            self.cursor.execute("SELECT * FROM MaintenanceLogs")
            rows = self.cursor.fetchall()
            self.maintenance_data = [{"Machine_ID": row[0], "Maintenance_Date": row[1], "Details": row[2]} for row in rows]
            self.update_treeview(self.maintenance_tree, self.maintenance_data, ["Machine_ID", "Maintenance_Date", "Details"])
            messagebox.showinfo("Success", "Maintenance logs loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load maintenance logs: {e}")

    def add_maintenance_log(self):
        new_log = {
            "Machine_ID": simpledialog.askstring("Input", "Enter Machine ID:"),
            "Maintenance_Date": simpledialog.askstring("Input", "Enter Maintenance Date (YYYY-MM-DD):"),
            "Details": simpledialog.askstring("Input", "Enter Maintenance Details:")
        }
        if all(new_log.values()):
            self.cursor.execute("INSERT INTO MaintenanceLogs (Machine_ID, Maintenance_Date, Details) VALUES (?, ?, ?)",
                                (new_log["Machine_ID"], new_log["Maintenance_Date"], new_log["Details"]))
            self.db_connection.commit()
            self.load_maintenance()
            messagebox.showinfo("Success", "Maintenance log added successfully!")

    def remove_maintenance_log(self):
        selected_item = self.maintenance_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No log selected.")
            return
        log_values = self.maintenance_tree.item(selected_item, "values")
        self.cursor.execute("DELETE FROM MaintenanceLogs WHERE Machine_ID = ? AND Maintenance_Date = ?",
                            (log_values[0], log_values[1]))
        self.db_connection.commit()
        self.load_maintenance()
        messagebox.showinfo("Success", "Maintenance log removed successfully!")

    def check_maintenance_alerts(self):
        overdue_logs = []
        for log in self.maintenance_data:
            maintenance_date = datetime.strptime(log["Maintenance_Date"], "%Y-%m-%d")
            if maintenance_date < datetime.now():
                overdue_logs.append(log["Machine_ID"])
        if overdue_logs:
            messagebox.showinfo("Overdue Maintenance", f"Overdue Maintenance for Machines:\n{', '.join(overdue_logs)}")
        else:
            messagebox.showinfo("Maintenance Check", "No overdue maintenance logs.")

    # ------------------ Production Tab ------------------ #
    def create_production_tab(self):
        production_tab = ttk.Frame(self.notebook)
        self.notebook.add(production_tab, text="Production Data")

        ttk.Button(production_tab, text="Load Production Data", command=self.load_production).pack(pady=5)

        self.production_tree = ttk.Treeview(production_tab, columns=("Machine_ID", "Equipment_Type", "Run_Start", "Run_End", "Units_Produced", "Product_Category", "Product_Type"), show="headings")
        for col in self.production_tree["columns"]:
            self.production_tree.heading(col, text=col)
            self.production_tree.column(col, width=150, anchor="center")
        self.production_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_production(self):
        try:
            with open('Training_Datasets/Day1/production_line_data.csv', 'r') as file:
                reader = csv.DictReader(file)
                self.production_data = [row for row in reader]
            self.update_treeview(self.production_tree, self.production_data, ["Machine_ID", "Equipment_Type", "Run_Start", "Run_End", "Units_Produced", "Product_Category", "Product_Type"])
            messagebox.showinfo("Success", "Production data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load production data: {e}")

    # ------------------ Summary Tab ------------------ #
    def create_summary_tab(self):
        summary_tab = ttk.Frame(self.notebook)
        self.notebook.add(summary_tab, text="Summary & Reports")

        ttk.Button(summary_tab, text="Generate Summary Report", command=self.generate_summary).pack(pady=5)

        self.summary_text = tk.Text(summary_tab, wrap="word", height=30)
        self.summary_text.pack(fill="both", expand=True, padx=10, pady=10)

    def generate_summary(self):
        summary = "Production Monitoring Summary:\n"
        summary += f"Total Inventory Items: {len(self.inventory_tree.get_children())}\n"
        summary += f"Total Suppliers: {len(self.supplier_tree.get_children())}\n"
        summary += f"Total Maintenance Logs: {len(self.maintenance_tree.get_children())}\n"
        summary += f"Total Production Runs: {len(self.production_tree.get_children())}\n"
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    # ------------------ Utility Methods ------------------ #
    @staticmethod
    def update_treeview(treeview, data, columns):
        """
        Update a Treeview widget with new data.
        """
        treeview.delete(*treeview.get_children())  # Clear existing data
        for entry in data:
            treeview.insert("", "end", values=[entry[col] for col in columns])

    def on_closing(self):
        """
        Handle application close event.
        """
        self.db_connection.close()
        self.destroy()

# ------------------ Main Execution ------------------ #
if __name__ == "__main__":
    app = ProductionMonitoringApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

