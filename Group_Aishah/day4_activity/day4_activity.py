import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox, filedialog, Toplevel
import csv
from datetime import datetime
import socket
import json
import threading
from urllib.parse import urlparse, parse_qs
import sqlite3
import logging
import configparser

CONFIG_FILENAME="config.ini"

DB_SQL = str(Path(__file__).resolve().parent / "delivery_data.db")
DB_CSV = str(Path(__file__).resolve().parent / "delivery_data.csv")
USER_PASS = str(Path(__file__).resolve().parent / "username_pw.json")

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,                    # Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format
    datefmt='%Y-%m-%d %H:%M:%S',           # Define the date format
    filename='pcpp.log',                    # Log to a file
    filemode='a'                           
)

logger = logging.getLogger()

# Read config file to load variables
config = configparser.ConfigParser()
config.read(CONFIG_FILENAME)



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
def read_database(file_path:str):

    orders_data = []
    riders_data = []

    file_extension = Path(file_path).suffix

    if file_extension == ".db":
        connection = sqlite3.connect(file_path)
        cursor = connection.cursor()
        # orders
        # order_id,rider_id,transport_type,order_date,deliver_date,item_quantity,cuisines,status
        # riders
        # rider_id, rider_id
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS riders (
                rider_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rider_name TEXT NOT NULL,
                phone_number TEXT NOT NULL,
                age TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                rider_id INTEGER NOT NULL,
                transport_type TEXT NOT NULL,
                order_date TEXT NOT NULL,
                deliver_date TEXT NOT NULL,
                item_quantity INTEGER NOT NULL,
                cuisines TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (rider_id) REFERENCES riders (rider_id)
            )
        ''')
        cursor.execute('SELECT * FROM orders')
        rows = cursor.fetchall()
        # Convert rows to a list of dictionaries
        for row in rows:
            order_id,rider_id,transport_type,order_date,deliver_date,item_quantity,cuisines,status = row
            orders_data.append({
                "order_id": order_id,
                "rider_id": rider_id,
                "transport_type": transport_type,
                "order_date": order_date,
                "deliver_date": deliver_date,
                "item_quantity": item_quantity,
                "cuisines": cuisines,
                "status": status
            })
        cursor.execute('SELECT * FROM riders')
        rows = cursor.fetchall()
        # Convert rows to a list of dictionaries
        for row in rows:
            rider_id,rider_name,phone_number,age,email = row
            riders_data.append({
                "rider_id": rider_id,
                "rider_name": rider_name,
                "phone_number": phone_number,
                "age": age,
                "email": email
            })

    elif file_extension == ".csv":
        # TO BE DEPRECATE
        with open(file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Read data
                    order_id = Validator.validate_text(row["order_id"])
                    rider_id = Validator.validate_text(row["rider_id"])                
                    transport_type = Validator.validate_text(row["transport_type"])
                    order_date = Validator.validate_date(row["order_date"])
                    deliver_date = Validator.validate_date(row["deliver_date"])
                    item_quantity = Validator.validate_text(row["item_quantity"])
                    cuisines = Validator.validate_text(row["cuisines"])
                    status = Validator.validate_text(row["status"])
                    orders_data.append(row)
                except ValidationError as ve:
                    logger.exception(f"Validation error: {ve}")
                except Exception as e:
                    logger.exception(f"Unexpected error: {e}")
                    
    return orders_data, riders_data

def write_database():
    ...

# command to start
"""
connection = sqlite3.connect("delivery_data.db")
cursor = connection.cursor()
"""

# command to add riders data
"""
riders_data = [
    ("Ali", ),
    ("Abu", ),
    ("Ahmad", ),
    ("Aishah", ),
    ("Aiman", ),
    ("Anwar", )
]
cursor.executemany("INSERT INTO riders (rider_id) VALUES (?)", riders_data)
connection.commit()
cursor.execute('SELECT * FROM riders')
rows = cursor.fetchall()
"""
# command to add orders data
"""
cursor.execute('DROP TABLE orders')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        rider_id INTEGER NOT NULL,
        transport_type TEXT NOT NULL,
        order_date TEXT NOT NULL,
        deliver_date TEXT NOT NULL,
        item_quantity INTEGER NOT NULL,
        cuisines TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (rider_id) REFERENCES riders (rider_id)
    )
''')
orders_data = list(csv.DictReader(open("delivery_data.csv")))
orders_data = [(randint(1,6),d['transport_type'],d['order_date'],d['deliver_date'],d['item_quantity'],d['cuisines'],d['status']) for d in orders_data]
cursor.executemany("INSERT INTO orders (rider_id, transport_type,order_date,deliver_date,item_quantity,cuisines,status) VALUES (?,?,?,?,?,?,?)", orders_data)
connection.commit()
cursor.execute('SELECT * FROM orders')
rows = cursor.fetchall()
"""

# GUI
class ProductionMonitoringApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Production Monitoring System")
        self.geometry("800x600")
        self.current_user = None
        self.orders_data = {}
        self.db_path = DB_SQL
        logger.info(f"reading db {self.db_path}")
        self.server_thread = threading.Thread(target=self.start_server)
        self.server_thread.daemon = True  # Ensure thread exits when the main program does
        self.server_thread.start()
        self.create_login_screen()
        with open(USER_PASS, 'r') as file:
            self.login_data = json.load(file)

    def start_server(
            self,
            #  host='0.0.0.0',
            host=config.get(section="server", option="host"),
            #  port=8080,
            port=int(config.get(section="server", option="port")),
        ):  # if cannot 0.0.0.0, 43.74.32.85
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Allow the socket to reuse the address
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the address and port
        server_socket.bind((host, port))
        
        # Start listening for connections
        server_socket.listen(5)
        logger.info(f"[*] Server is running on http://{host}:{port}")
        
        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            logger.debug(f"[x] Connection established with {client_address}")
            
            # Receive the request data
            request_data = client_socket.recv(1024).decode('utf-8')
            logger.info(f"[x] Received request:\n{request_data}")

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
                        for order_dict in self.orders_data:
                            if order_dict['order_id']==order_id:
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
            # data = self.orders_data.copy()
            
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
            logger.info("[x] Response returned.")
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
        self.rider_tab=ttk.Frame(self.tab_control)
        # self.tab_control.add(self.delivery_tab, text="Delivery Data")
        self.tab_control.add(self.delivery_tab,text="View orders")
        self.tab_control.add(self.rider_tab,text="View riders")
        self.tab_control.pack(expand=1, fill="both")
        self.tab_control.pack(expand=1,fill="both")
        self.setup_production_tab()
        self.setup_rider_tab()
    
    def setup_rider_tab(self):
        # Title
        ttk.Label(self.rider_tab, text="View riders", font=("Arial", 16)).pack(pady=10)
        # View
        self.riders_tree = ttk.Treeview(
            self.rider_tab, 
            columns=(
                "rider_id",
                "rider_name",
                "phone_number",
                "age",
                "email"
                ),
            show="headings"
        )
        self.riders_tree.heading("rider_id", text="rider_id")
        self.riders_tree.heading("rider_name", text="rider_name")
        self.riders_tree.heading("phone_number", text="phone_number")
        self.riders_tree.heading("age", text="age")
        self.riders_tree.heading("email", text="email")
        self.riders_tree.pack(fill="both", expand=True, pady=10)        

    def setup_production_tab(self):
        """
        Setup the production data tab.
        """
        # Title
        # ttk.Label(self.delivery_tab, text="Delivery Data", font=("Arial", 16)).pack(pady=10)
        ttk.Label(self.delivery_tab, text="View orders", font=("Arial", 16)).pack(pady=10)

        # All Button
        ttk.Button(self.delivery_tab, text="Load Data / Reset Filter", command=self.load_production_data).pack(pady=5)
        ttk.Button(self.delivery_tab, text="Clear View", command=self.remove_view).pack(padx=1,pady=5)
        ttk.Label(self.delivery_tab, text="Select Parameter:").pack(pady=5)
        self.parameter_combobox = ttk.Combobox(self.delivery_tab, values=["order_id","rider_id","transport_type","item_quantity","cuisines","status"], state="readonly")
        self.parameter_combobox.pack(padx=0,pady=5)
        ttk.Label(self.delivery_tab, text="Filter by:").pack(pady=5)
        self.rider_entry = ttk.Entry(self.delivery_tab)
        self.rider_entry.pack(padx=5,pady=5)
        ttk.Button(self.delivery_tab, text="Filter", command=self.filter_by_parameter).pack(padx=3,pady=5)
        ttk.Button(self.delivery_tab, text="Export to csv", command=self.export_table_to_csv).pack(padx=20,pady=5)
        ttk.Button(self.delivery_tab, text="Update Status", command=self.update_status).pack(padx=10,pady=5)
        
        

        # View
        self.production_tree = ttk.Treeview(
            self.delivery_tab, 
            columns=(
                "order_id",
                "rider_id",
                "transport_type",
                "order_date","deliver_date",
                "item_quantity",
                "cuisines",
                "status"
                ),
            show="headings"
        )
        self.production_tree.heading("order_id", text="order_id")
        self.production_tree.heading("rider_id", text="rider_id")
        self.production_tree.heading("transport_type", text="transport_type")
        self.production_tree.heading("order_date", text="order_date")
        self.production_tree.heading("deliver_date", text="deliver_date")
        self.production_tree.heading("item_quantity", text="item_quantity")
        self.production_tree.heading("cuisines", text="cuisines")
        self.production_tree.heading("status", text="status")
        self.production_tree.pack(fill="both", expand=True, pady=10)

    def load_production_data(self):
        """
        Load production data from a CSV file.
        """
        logger.info("loading data")
        if not self.db_path:
            return

        try:
            self.orders_data, self.riders_data = read_database(self.db_path)
            logger.info(f"loaded {len(self.orders_data)=}")
            logger.info(f"loaded {len(self.riders_data)=}")
            self.populate_production_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def populate_production_data(self, orders_data:list=None, riders_data:list=None):
        """
        Args:
            orders_data (list[dict]): the list of data the load from .csv file

        Populate the production data treeview.
        """
        if orders_data is not None:
            self.orders_data = orders_data
        if riders_data is not None:
            self.riders_data = riders_data

        self.production_tree.delete(*self.production_tree.get_children())
        # TODO: riders tree?
        for data in self.orders_data:
            data_in_list = list(data.values())
            self.production_tree.insert("", "end", values=data_in_list)

        self.riders_tree.delete(*self.riders_tree.get_children())
        for data in self.riders_data:
            data_in_list = list(data.values())
            self.riders_tree.insert("", "end", values=data_in_list)

    def generate_report(self):
        """
        Generate a summary report.
        """
        self.report_text.delete(1.0, tk.END)
        if not self.orders_data:
            self.report_text.insert(tk.END, "No data available to generate a report.")
            return

        report_lines = []
        for data in self.orders_data:
            report_lines.append(f"Equipment Type: {data}")
            report_lines.append("")

        self.report_text.insert(tk.END, "\n".join(report_lines))
        
    def remove_view(self):
        self.production_tree.delete(*self.production_tree.get_children())
        
    def filter_by_parameter(self):
        # preprocess
        self.remove_view()
        self.orders_data:list = read_database(self.db_path)
        
        # actual filter logic
        filtered_data = []
        for data in self.orders_data:
            if self.rider_entry.get().strip() == data[self.parameter_combobox.get().strip()]:
                filtered_data.append(data)

        # postprocess
        self.populate_production_data(filtered_data)
    
    def export_table_to_csv(self):
        
        """
        Export an SQLite table to a CSV file.
        """

        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Query to fetch all data from the table
            cursor.execute("SELECT * FROM orders")
            rows = cursor.fetchall()

            # Fetch column names
            column_names = [description[0] for description in cursor.description]

            # Write data to CSV
            with open("exported_orders.csv", mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(column_names)  # Write header row
                writer.writerows(rows)        # Write data rows
            messagebox.showinfo(title='', message='Exported!')
            logger.info("Table orders has been exported to csv (exported_orders.csv)")
        except sqlite3.Error as e:
                logger.exception(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()

    def update_status(self):
        popup = Toplevel(self)
        popup.title("Update Status")
        popup.geometry("300x150")
        
        # Create labels and entry widgets for Order ID and Status
        tk.Label(popup, text="Order ID:").pack(pady=5)
        orderid_entry = tk.Entry(popup)
        orderid_entry.pack(pady=5)
        
        tk.Label(popup, text="Status:").pack(pady=5)
        status_entry = tk.Entry(popup)
        status_entry.pack(pady=5)

        def update_with_entry():
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            order_id:int = orderid_entry.get().strip()
            new_status:str = status_entry.get().strip()
            cursor.execute(f"UPDATE orders SET status = '{new_status}' WHERE order_id = {order_id};")
            conn.commit()
            messagebox.showinfo(title='', message='Updated!')
            popup.destroy()

        ttk.Button(popup, text='update', command=update_with_entry).pack()



if __name__ == "__main__":
    app = ProductionMonitoringApp()
    def logout():
        messagebox.showinfo(title='', message='Logged out.')
        app.destroy()
    app.protocol('WM_DELETE_WINDOW', logout)
    app.mainloop()
