import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import json
import xml.etree.ElementTree as ET
import csv
from datetime import datetime


class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
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

        # Create the main UI
        self.create_menu()
        self.create_frames()
        self.create_tabs()
        self.create_properties_panel()

    def create_menu(self):
        """
        Create the main menu with dropdowns.
        """
        self.menu_bar = tk.Menu(self)

        # File Menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Load Inventory Data", command=self.load_inventory)
        file_menu.add_command(label="Load Supplier Data", command=self.load_supplier)
        file_menu.add_command(label="Load Maintenance Logs", command=self.load_maintenance)
        file_menu.add_command(label="Load Production Data", command=self.load_production)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        # Help Menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=self.menu_bar)

    def create_frames(self):
        """
        Create the left (tabs) and right (properties panel) frames.
        """
        self.left_frame = ttk.Frame(self)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ttk.Frame(self, width=300, padding=10)
        self.right_frame.pack(side="right", fill="y")

    def create_tabs(self):
        """
        Create tabs for managing inventory, suppliers, maintenance logs, and production data.
        """
        self.notebook = ttk.Notebook(self.left_frame)
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

    # ------------------ Supplier Tab ------------------ #
    def create_supplier_tab(self):
        supplier_tab = ttk.Frame(self.notebook)
        self.notebook.add(supplier_tab, text="Supplier Management")

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

    # ------------------ Maintenance Tab ------------------ #
    def create_maintenance_tab(self):
        maintenance_tab = ttk.Frame(self.notebook)
        self.notebook.add(maintenance_tab, text="Maintenance Logs")

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

    # ------------------ Production Tab ------------------ #
    def create_production_tab(self):
        production_tab = ttk.Frame(self.notebook)
        self.notebook.add(production_tab, text="Production Data")

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

    # ------------------ Properties Panel ------------------ #
    def create_properties_panel(self):
        """
        Create a panel on the right side for adding/updating data.
        """
        self.properties_title = ttk.Label(self.right_frame, text="Properties", font=("Arial", 16))
        self.properties_title.pack(pady=10)

        # Dynamic input fields
        self.properties_fields = {}
        self.properties_submit_button = ttk.Button(self.right_frame, text="Submit", command=self.submit_properties)
        self.properties_submit_button.pack(pady=10)

    def populate_properties(self, tab_name):
        """
        Populate the properties panel with input fields based on the active tab.
        """
        for widget in self.right_frame.winfo_children():
            if widget not in {self.properties_title, self.properties_submit_button}:
                widget.destroy()

        self.active_tab = tab_name
        self.properties_fields.clear()

        if tab_name == "inventory":
            fields = ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"]
        elif tab_name == "supplier":
            fields = ["Supplier_ID", "Material_Type", "Delivery_Date"]
        elif tab_name == "maintenance":
            fields = ["Machine_ID", "Maintenance_Date", "Details"]
        else:
            fields = []

        for field in fields:
            ttk.Label(self.right_frame, text=field).pack(anchor="w", pady=5)
            entry = ttk.Entry(self.right_frame)
            entry.pack(fill="x", pady=5)
            self.properties_fields[field] = entry

    def submit_properties(self):
        """
        Handle form submission and update the appropriate dataset.
        """
        if not self.active_tab:
            messagebox.showerror("Error", "No active tab to update.")
            return

        data = {field: entry.get() for field, entry in self.properties_fields.items()}
        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required.")
            return

        if self.active_tab == "inventory":
            self.inventory_data.append(data)
            self.update_treeview(self.inventory_tree, self.inventory_data, ["Category", "Product_Type", "Stock_Level", "Reorder_Threshold"])
        elif self.active_tab == "supplier":
            self.supplier_data.append(data)
            self.update_treeview(self.supplier_tree, self.supplier_data, ["Supplier_ID", "Material_Type", "Delivery_Date"])
        elif self.active_tab == "maintenance":
            self.cursor.execute("INSERT INTO MaintenanceLogs (Machine_ID, Maintenance_Date, Details) VALUES (?, ?, ?)",
                                (data["Machine_ID"], data["Maintenance_Date"], data["Details"]))
            self.db_connection.commit()
            self.load_maintenance()

        messagebox.showinfo("Success", f"Data successfully added to {self.active_tab.capitalize()}!")

    @staticmethod
    def update_treeview(treeview, data, columns):
        """
        Update a Treeview widget with new data.
        """
        treeview.delete(*treeview.get_children())
        for entry in data:
            treeview.insert("", "end", values=[entry[col] for col in columns])

    def show_about(self):
        """
        Display the About dialog.
        """
        messagebox.showinfo("About", "Production Monitoring System\nVersion 1.0\nDeveloped with Tkinter")

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
