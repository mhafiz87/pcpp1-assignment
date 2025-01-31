import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime

# Error
class ValidationError(ValueError):
    """Custom exception for validation errors."""
    def __init__(self, message):
        super().__init__(f"Validation Error: {message}")

# Classes

# Validator
class Validator:
    @staticmethod
    def validate_text(text):
        if isinstance(text, str) and len(text.strip()) > 0:
            return text.strip()
        else:
            raise ValidationError("Text input must be a non-empty string.")

    @staticmethod
    def validate_positive_integer(value):
        if isinstance(value, int) and value > 0:
            return value
        else:
            raise ValidationError("Value must be a positive integer.")

    @staticmethod
    def validate_date(date_str):
        try:
            return datetime.strptime(date_str.strip(), "%m-%d-%Y")
        except ValueError:
            raise ValidationError("Invalid date format. Expected MM-DD-YYYY.")
        
# Database
def read_database(file_path):

    data = []

    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # Read data
                order_id = Validator.validate_text(row["Order_ID"])
                transport_type = Validator.validate_text(row["Transport_Type"])
                order_date = Validator.validate_date(row["Order_Date"])
                deliver_date = Validator.validate_date(row["Deliver_Date"])
                item_quantity = Validator.validate_text(row["Item_Quantity"])
                cuisines = Validator.validate_text(row["Cuisines"])
                rider_name = Validator.validate_text(row["Rider_Name"])                
                data.append(row)
            except ValidationError as ve:
                print(f"Validation error: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                
    return data


# GUI
class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
        self.geometry("800x600")
        self.current_user = None
        self.delivery_data = {}
        self.file_path = str(Path(__file__).resolve().parent / "delivery_data.csv")
        print(self.file_path)
        self.create_login_screen()
        

    def create_login_screen(self):
        """
        Create the login screen for role-based access control.
        """
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(fill="both", expand=True)
        
        ttk.Label(self.login_frame, text="Delivery Tracker", font=("Arial", 20)).pack(pady=20)
        self.username_combobox = ttk.Combobox(self.login_frame, values=["nang","aishah","yuen"], state="readonly")
        self.username_combobox.pack(pady=5)

        ttk.Label(self.login_frame, text="Select Role:").pack(pady=5)
        self.role_combobox = ttk.Combobox(self.login_frame, values=["customer_service_operator","cs_manager"], state="readonly")
        self.role_combobox.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).pack(pady=20)
       

    def handle_login(self):
        """
        Handle login validation.
        """
        username = self.username_combobox.get().strip()
        role = self.role_combobox.get().strip()

        if not username or not role:
            messagebox.showerror("Error", "Please enter a username and select a role.")
            return

        self.current_user = role
        self.login_frame.destroy()
        self.create_main_dashboard()

    def create_main_dashboard(self):
        """
        Create the main dashboard after successful login.
        """
        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.delivery_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.delivery_tab, text="Delivery Data")
        self.tab_control.pack(expand=1, fill="both")
        self.setup_production_tab()

    def setup_production_tab(self):
        """
        Setup the production data tab.
        """
        # Title
        ttk.Label(self.delivery_tab, text="Delivery Data", font=("Arial", 16)).pack(pady=10)

        # All Button
        ttk.Button(self.delivery_tab, text="Load Data / Reset Filter", command=self.load_production_data).pack(pady=5)
        ttk.Button(self.delivery_tab, text="Clear View", command=self.remove_view).pack(padx=1,pady=5)
        ttk.Label(self.delivery_tab, text="Select Parameter:").pack(pady=5)
        self.parameter_combobox = ttk.Combobox(self.delivery_tab, values=["Order_ID","Transport_Type","Item_Quantity","Cuisines","Rider_Name","Status"], state="readonly")
        self.parameter_combobox.pack(padx=0,pady=5)
        ttk.Label(self.delivery_tab, text="Filter by:").pack(pady=5)
        self.rider_entry = ttk.Entry(self.delivery_tab)
        self.rider_entry.pack(padx=5,pady=5)
        ttk.Button(self.delivery_tab, text="Filter", command=self.filter_by_parameter).pack(padx=3,pady=5)

        # View
        self.production_tree = ttk.Treeview(
            self.delivery_tab, 
            columns=(
                "Order_ID",
                "Transport_Type",
                "Order_Date","Deliver_Date",
                "Item_Quantity",
                "Cuisines",
                "Rider_Name",
                "Status"
                ),
            show="headings"
        )
        self.production_tree.heading("Order_ID", text="Order_ID")
        self.production_tree.heading("Transport_Type", text="Transport_Type")
        self.production_tree.heading("Order_Date", text="Order_Date")
        self.production_tree.heading("Deliver_Date", text="Deliver_Date")
        self.production_tree.heading("Item_Quantity", text="Item_Quantity")
        self.production_tree.heading("Cuisines", text="Cuisines")
        self.production_tree.heading("Rider_Name", text="Rider_Name")
        self.production_tree.heading("Status", text="Status")
        self.production_tree.pack(fill="both", expand=True, pady=10)

    def load_production_data(self):
        """
        Load production data from a CSV file.
        """
        if not self.file_path:
            return

        try:
            self.delivery_data = read_database(self.file_path)
            self.populate_production_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def populate_production_data(self, delivery_data:list=None):
        """
        Args:
            delivery_data (list[dict]): the list of data the load from .csv file

        Populate the production data treeview.
        """
        if delivery_data is None:
            delivery_data = self.delivery_data

        self.production_tree.delete(*self.production_tree.get_children())
        for data in delivery_data:
            data_in_list = list(data.values())
            self.production_tree.insert("", "end", values=data_in_list)

    def generate_report(self):
        """
        Generate a summary report.
        """
        self.report_text.delete(1.0, tk.END)
        if not self.delivery_data:
            self.report_text.insert(tk.END, "No data available to generate a report.")
            return

        report_lines = []
        for data in self.delivery_data:
            report_lines.append(f"Equipment Type: {data}")
            report_lines.append("")

        self.report_text.insert(tk.END, "\n".join(report_lines))
        
    def remove_view(self):
        self.production_tree.delete(*self.production_tree.get_children())
        
    def filter_by_parameter(self):
        # preprocess
        self.remove_view()
        self.delivery_data:list = read_database(self.file_path)
        
        # actual filter logic
        filtered_data = []
        for data in self.delivery_data:
            if self.rider_entry.get().strip() == data[self.parameter_combobox.get().strip()]:
                filtered_data.append(data)

        # postprocess
        self.populate_production_data(filtered_data)

if __name__ == "__main__":
    app = ProductionMonitoringApp()
    app.mainloop()
