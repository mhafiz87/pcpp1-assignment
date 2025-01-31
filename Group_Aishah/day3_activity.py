import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import csv
from datetime import datetime
import socket
import json
import threading
from urllib.parse import urlparse, parse_qs

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
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True  # Ensure thread exits when the main program does
        self.server_thread.start()
        self.create_login_screen()
        with open('pcpp_training/username_pw.json', 'r') as file:
            self.login_data = json.load(file)
        
    def start_server(self, host='0.0.0.0', port=8080): # if cannot 0.0.0.0, 43.74.32.85
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow the socket to reuse the address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        
        # Start listening for connections
        server_socket.listen(5)
        print(f"Server is running on http://{host}:{port}")
        
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            
            # Receive the request data
            request_data = client_socket.recv(1024).decode('utf-8')
            print(f"Received request:\n{request_data}")

            try:
            # Extract the first line of the HTTP request
                request_line = request_data.splitlines()[0]
                method, full_path, _ = request_line.split()  # Extract the method and full path

                # Parse the URL and query parameters
                parsed_url = urlparse(full_path)
                path = parsed_url.path  # The main path (e.g., /order)
                query_params = parse_qs(parsed_url.query)  # Query parameters as a dictionary

                # Route handling
                if path == "/order":
                    # Check for the "param" query parameter
                    if "param" in query_params:
                        order_id = query_params["param"][0]  # Get the first value of the "param"
                        # response_body = f"Order ID received: {order_id}"
                        for order_dict in self.delivery_data:
                            if order_dict['Order_ID']==order_id:
                                response_body=order_dict
                                break
                        
                        status_code = "200 OK"
                    else:
                        response_body = "400 Bad Request: Missing 'param'"

                        status_code = "400 Bad Request"
                else:
                    response_body = "404 Not Found"

                    status_code = "404 Not Found"

                response = (
                    # "HTTP/1.1 200 OK\r\n"
                    f"HTTP/1.1 {status_code}\r\n"
                    "Content-Type: application/json\r\n"
                    # "Content-Type: text/plain\r\n"
                    # f"Content-Length: {len(str(data))}\r\n"
                    f"Content-Length: {len(str(response_body))}\r\n"
                    "\r\n"
                    # f"{data}"
                    f"{response_body}"
                )
            except Exception as e:
            # Handle malformed requests
                response_body = "400 Bad Request"
                response = (
                    "HTTP/1.1 400 Bad Request\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "\r\n"
                    f"{response_body}"
                )
       
            # # Get the latest data after request received
            # data = self.delivery_data.copy()
            
            # Prepare a simple HTTP response
            # response = (
            #     "HTTP/1.1 200 OK\r\n"
            #     "Content-Type: application/json\r\n"
            #     # "Content-Type: text/plain\r\n"
            #     # f"Content-Length: {len(str(data))}\r\n"
            #     f"Content-Length: {len(str(response_body))}\r\n"
            #     "\r\n"
            #     # f"{data}"
            #     f"{response_body}"
            # )
            

            
            # Send the response to the client
            client_socket.sendall(response.encode('utf-8'))
            # client_socket.sendall(response)
            
            # Close the connection
            # client_socket.close()
        

    def create_login_screen(self):
        """
        Create the login screen for role-based access control.
        """
        self.login_frame = ttk.Frame(self)
        self.login_frame.pack(fill="both", expand=True)
        
        ttk.Label(self.login_frame, text="Order Tracker", font=("Arial", 20)).pack(pady=20)
        ttk.Label(self.login_frame, text="Username").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.pack(pady=5)

        ttk.Label(self.login_frame, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_frame)
        self.password_entry.pack(pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.handle_login).pack(pady=20)
       

    def handle_login(self):
        """
        Handle login validation.
        """
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter a username.")
            return

        # validate
        if username in self.login_data:
            if password == self.login_data.get(username):
                self.current_user = username
                self.login_frame.destroy()
                self.create_main_dashboard()
            else:
                messagebox.showerror("Error", "Please enter correct password.")
        else:
            messagebox.showerror("Error", "Please enter a valid user name.")

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
        if delivery_data is not None:
            self.delivery_data = delivery_data

        self.production_tree.delete(*self.production_tree.get_children())
        for data in self.delivery_data:
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
    def logout():
        messagebox.showinfo(title='', message='Logged out.')
        app.destroy()
    app.protocol('WM_DELETE_WINDOW', logout)
    app.mainloop()
