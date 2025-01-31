import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import logging
import configparser

# Read configuration
config = configparser.ConfigParser()
config.read("Config.ini")
DB_FILE = config.get("Settings", "db_file", fallback="manufacturer.db")
LOG_FILE = config.get("Settings", "log_file", fallback="app.log")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class ManufacturerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Electronics Manufacturer Management")
        self.geometry("1000x700")

        # Initialize database
        self.init_db()

        # Create UI elements
        self.create_widgets()

    def init_db(self):
        """
        Create the SQLite database and tables if they don't already exist.
        """
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()

        # Create tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Category TEXT NOT NULL,
                Price REAL NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Supplier (
                SupplierID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Contact TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Inventory (
                InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
                ProductID INTEGER NOT NULL,
                Quantity INTEGER NOT NULL,
                FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Machine (
                MachineID INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Function TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS MachineActions (
                ActionID INTEGER PRIMARY KEY AUTOINCREMENT,
                MachineID INTEGER NOT NULL,
                ProductID INTEGER NOT NULL,
                ActionDate TEXT NOT NULL,
                Quantity INTEGER NOT NULL,
                FOREIGN KEY (MachineID) REFERENCES Machine (MachineID),
                FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
            )
        ''')

        self.conn.commit()

    def create_widgets(self):
        """
        Create the main GUI layout.
        """
        # Tabs for different tables
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.create_product_tab()
        self.create_supplier_tab()
        self.create_inventory_tab()
        self.create_machine_tab()

    def create_product_tab(self):
        """
        Create the Product management tab.
        """
        product_tab = ttk.Frame(self.notebook)
        self.notebook.add(product_tab, text="Products")

        self.product_tree = ttk.Treeview(product_tab, columns=("ProductID", "Name", "Category", "Price"), show="headings")
        for col in self.product_tree["columns"]:
            self.product_tree.heading(col, text=col)
            self.product_tree.column(col, anchor="center")
        self.product_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview(self.product_tree, "Product")

        # Buttons
        button_frame = ttk.Frame(product_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Product", command=self.add_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Product", command=self.update_product).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Product", command=self.delete_product).pack(side="left", padx=5)

    def create_supplier_tab(self):
        """
        Create the Supplier management tab.
        """
        supplier_tab = ttk.Frame(self.notebook)
        self.notebook.add(supplier_tab, text="Suppliers")

        self.supplier_tree = ttk.Treeview(supplier_tab, columns=("SupplierID", "Name", "Contact"), show="headings")
        for col in self.supplier_tree["columns"]:
            self.supplier_tree.heading(col, text=col)
            self.supplier_tree.column(col, anchor="center")
        self.supplier_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview(self.supplier_tree, "Supplier")

        # Buttons
        button_frame = ttk.Frame(supplier_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Supplier", command=self.add_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Supplier", command=self.update_supplier).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Supplier", command=self.delete_supplier).pack(side="left", padx=5)

    def create_inventory_tab(self):
        """
        Create the Inventory management tab.
        """
        inventory_tab = ttk.Frame(self.notebook)
        self.notebook.add(inventory_tab, text="Inventory")

        self.inventory_tree = ttk.Treeview(inventory_tab, columns=("InventoryID", "ProductID", "Quantity"), show="headings")
        for col in self.inventory_tree["columns"]:
            self.inventory_tree.heading(col, text=col)
            self.inventory_tree.column(col, anchor="center")
        self.inventory_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview(self.inventory_tree, "Inventory")

        # Buttons
        button_frame = ttk.Frame(inventory_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Inventory", command=self.add_inventory).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Inventory", command=self.update_inventory).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Inventory", command=self.delete_inventory).pack(side="left", padx=5)

    def create_machine_tab(self):
        """
        Create the Machine management tab.
        """
        machine_tab = ttk.Frame(self.notebook)
        self.notebook.add(machine_tab, text="Machines")

        self.machine_tree = ttk.Treeview(machine_tab, columns=("MachineID", "Name", "Function"), show="headings")
        for col in self.machine_tree["columns"]:
            self.machine_tree.heading(col, text=col)
            self.machine_tree.column(col, anchor="center")
        self.machine_tree.pack(fill="both", expand=True, padx=10, pady=10)
        self.update_treeview(self.machine_tree, "Machine")

        # Buttons
        button_frame = ttk.Frame(machine_tab)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Machine", command=self.add_machine).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Machine", command=self.update_machine).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Machine", command=self.delete_machine).pack(side="left", padx=5)

    def update_treeview(self, tree, table):
        """
        Update a Treeview with data from the specified table.
        """
        tree.delete(*tree.get_children())
        self.cursor.execute(f"SELECT * FROM {table}")
        rows = self.cursor.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

    def add_product(self):
        self.edit_window("Add Product", "Product", ["Name", "Category", "Price"])

    def update_product(self):
        self.edit_window("Update Product", "Product", ["Name", "Category", "Price"], update=True)

    def delete_product(self):
        self.delete_row("Product")

    def add_supplier(self):
        self.edit_window("Add Supplier", "Supplier", ["Name", "Contact"])

    def update_supplier(self):
        self.edit_window("Update Supplier", "Supplier", ["Name", "Contact"], update=True)

    def delete_supplier(self):
        self.delete_row("Supplier")

    def add_inventory(self):
        self.edit_window("Add Inventory", "Inventory", ["ProductID", "Quantity"])

    def update_inventory(self):
        self.edit_window("Update Inventory", "Inventory", ["ProductID", "Quantity"], update=True)

    def delete_inventory(self):
        self.delete_row("Inventory")

    def add_machine(self):
        self.edit_window("Add Machine", "Machine", ["Name", "Function"])

    def update_machine(self):
        self.edit_window("Update Machine", "Machine", ["Name", "Function"], update=True)

    def delete_machine(self):
        self.delete_row("Machine")

    def edit_window(self, title, table, fields, update=False):
        """
        Open a window for adding or updating rows in the database.
        """
        window = tk.Toplevel(self)
        window.title(title)

        entries = {}
        for field in fields:
            ttk.Label(window, text=field).pack(pady=5)
            entry = ttk.Entry(window)
            entry.pack(pady=5)
            entries[field] = entry

        def save():
            data = {field: entries[field].get() for field in fields}
            if update:
                # Update logic here
                pass
            else:
                placeholders = ", ".join(["?" for _ in fields])
                self.cursor.execute(f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})", tuple(data.values()))
                self.conn.commit()
                self.update_treeview(self.notebook.nametowidget(self.notebook.select()), table)
                logging.info(f"Added new record to {table}: {data}")
            window.destroy()

        ttk.Button(window, text="Save", command=save).pack(pady=10)

    def delete_row(self, table):
        """
        Delete the selected row from the database.
        """
        tree = self.notebook.nametowidget(self.notebook.select())
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return

        item_values = tree.item(selected_item, "values")
        row_id = item_values[0]
        self.cursor.execute(f"DELETE FROM {table} WHERE {table}ID = ?", (row_id,))
        self.conn.commit()
        self.update_treeview(tree, table)
        logging.info(f"Deleted record from {table} with ID {row_id}")

if __name__ == "__main__":
    app = ManufacturerApp()
    app.mainloop()
