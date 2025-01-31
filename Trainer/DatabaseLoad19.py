import sqlite3
from datetime import datetime, timedelta
import random

DB_FILE = "manufacturer.db"

# Preload script to populate tables with consistent data
def preload_data():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create MachineActions table if not exists
    cursor.execute('''
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

    # Clear existing data
    cursor.execute("DELETE FROM Product")
    cursor.execute("DELETE FROM Supplier")
    cursor.execute("DELETE FROM Inventory")
    cursor.execute("DELETE FROM Machine")
    cursor.execute("DELETE FROM MachineActions")

    # Product Data
    products = [
        ("Speaker", "Audio Devices", 120.50),
        ("Headphones", "Audio Devices", 89.99),
        ("Amplifier", "Audio Devices", 299.99),
        ("Camera", "Video Devices", 450.00),
        ("Microphone", "Audio Devices", 49.99)
    ]

    cursor.executemany("INSERT INTO Product (Name, Category, Price) VALUES (?, ?, ?)", products)

    # Supplier Data
    suppliers = [
        ("Electronics Co.", "contact@electronicsco.com"),
        ("Parts R Us", "support@partsrus.com"),
        ("Gadget Supplies", "info@gadgetsupplies.com")
    ]

    cursor.executemany("INSERT INTO Supplier (Name, Contact) VALUES (?, ?)", suppliers)

    # Machine Data
    machines = [
        ("Speaker Assembly Machine", "Assembly"),
        ("Headphone Assembly Machine", "Assembly"),
        ("Amplifier Testing Machine", "Testing"),
        ("Camera Calibration Machine", "Calibration"),
        ("Microphone Packaging Machine", "Packaging")
    ]

    cursor.executemany("INSERT INTO Machine (Name, Function) VALUES (?, ?)", machines)

    # Generate consistent inventory and actions over 3 years
    product_ids = [row[0] for row in cursor.execute("SELECT ProductID FROM Product").fetchall()]
    for product_id in product_ids:
        current_date = datetime(2022, 1, 1)
        for _ in range(36):  # Monthly updates
            quantity = random.randint(50, 500)
            cursor.execute("INSERT INTO Inventory (ProductID, Quantity) VALUES (?, ?)", (product_id, quantity))

            # Simulate actions
            if random.choice([True, False]):
                machine_id = random.choice([row[0] for row in cursor.execute("SELECT MachineID FROM Machine").fetchall()])
                cursor.execute(
                    "INSERT INTO MachineActions (MachineID, ProductID, ActionDate, Quantity) VALUES (?, ?, ?, ?)",
                    (machine_id, product_id, current_date.strftime('%Y-%m-%d'), quantity // 2)
                )

            current_date += timedelta(days=30)  # Move to next month

    conn.commit()
    conn.close()

if __name__ == "__main__":
    preload_data()
    print("Database preloaded with consistent data for 2022-2024.")
