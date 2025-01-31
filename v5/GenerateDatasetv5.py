import os
import csv
import json
import sqlite3
import xml.etree.ElementTree as ET
from faker import Faker
from datetime import datetime, timedelta, date
import random

# Initialize Faker
fake = Faker()

# Base Directories
base_dir = "Training_Datasets"
days = ["Day1", "Day2", "Day3", "Day4"]
os.makedirs(base_dir, exist_ok=True)
for day in days:
    os.makedirs(os.path.join(base_dir, day), exist_ok=True)

# Fixed Parameters
RUN_DURATIONS = [7, 14, 21]  # Run durations in days
EQUIPMENT_TYPES = {
    "Speaker Assembly Machine": "Speakers",
    "Microphone Assembly Machine": "Microphones",
    "Headphone Assembly Machine": "Headphones",
    "Amplifier Assembly Machine": "Amplifiers",
    "Camera Assembly Machine": "Cameras"
}
PRODUCT_CATEGORIES = {
    "Audio Devices": ["Speakers", "Microphones", "Headphones", "Amplifiers"],
    "Video Devices": ["Cameras", "Projectors", "Monitors", "Streaming Devices"],
    "Accessories": ["Cables", "Remote Controls", "Mounts", "Batteries"]
}
MATERIAL_TYPES = ["Plastic", "Metal", "Circuit Board", "Wiring", "Packaging"]

# Units Produced Multiplier
UNITS_PER_DAY = {
    "Speaker Assembly Machine": 30,
    "Microphone Assembly Machine": 25,
    "Headphone Assembly Machine": 20,
    "Amplifier Assembly Machine": 15,
    "Camera Assembly Machine": 10
}

# 1. Generate Production Line Data (CSV)
def generate_production_line_data():
    file_path = os.path.join(base_dir, "Day1", "production_line_data.csv")
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Machine_ID", "Equipment_Type", "Run_Start", "Run_End", "Units_Produced", "Product_Category", "Product_Type"])
        
        for year in range(2020, 2025):
            start_date = date(year, 1, 1)  # Use datetime.date object
            end_date = date(year, 12, 31)  # Use datetime.date object
            for _ in range(200):
                machine_id = f"MC-{random.randint(1000, 9999)}"
                equipment_type, product_type = random.choice(list(EQUIPMENT_TYPES.items()))
                product_category = next((cat for cat, types in PRODUCT_CATEGORIES.items() if product_type in types), "Unknown")
                run_start = fake.date_between(start_date=start_date, end_date=end_date)
                duration = random.choice(RUN_DURATIONS)
                run_end = run_start + timedelta(days=duration)
                units_produced = duration * UNITS_PER_DAY[equipment_type]
                writer.writerow([machine_id, equipment_type, run_start.strftime("%Y-%m-%d"), run_end.strftime("%Y-%m-%d"), units_produced, product_category, product_type])

# 2. Generate Supplier Schedule Data (XML)
def generate_supplier_schedule():
    file_path = os.path.join(base_dir, "Day2", "supplier_schedule.xml")
    root = ET.Element("SupplierSchedules")
    
    for year in range(2020, 2025):
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        for _ in range(100):
            schedule = ET.SubElement(root, "Schedule")
            ET.SubElement(schedule, "Supplier_ID").text = f"SPL-{random.randint(100, 999)}"
            ET.SubElement(schedule, "Material_Type").text = random.choice(MATERIAL_TYPES)
            delivery_date = fake.date_between(start_date=start_date, end_date=end_date)
            ET.SubElement(schedule, "Delivery_Date").text = delivery_date.strftime("%Y-%m-%d")
    
    tree = ET.ElementTree(root)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)

# 3. Generate Inventory Levels (JSON)
def generate_inventory_levels():
    file_path = os.path.join(base_dir, "Day3", "inventory_levels.json")
    inventory = []
    
    for product_category, product_types in PRODUCT_CATEGORIES.items():
        for product_type in product_types:
            inventory.append({
                "Category": product_category,
                "Product_Type": product_type,
                "Stock_Level": random.randint(100, 1000),
                "Reorder_Threshold": random.randint(50, 300)
            })
    
    with open(file_path, mode="w") as file:
        json.dump(inventory, file, indent=4)

# 4. Generate Maintenance Logs (SQLite Database)
def generate_maintenance_logs():
    file_path = os.path.join(base_dir, "Day4", "maintenance_logs.db")
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS MaintenanceLogs (
        Machine_ID TEXT,
        Maintenance_Date TEXT,
        Issue_Description TEXT
    )
    """)

    machines = [f"MC-{random.randint(1000, 9999)}" for _ in range(10)]
    for _ in range(200):
        maintenance_date = fake.date_between(start_date=date(2020, 1, 1), end_date=date(2024, 12, 31))
        issue_description = random.choice(["Routine Check", "Component Replacement", "Alignment Adjustment", "Calibration"])
        machine_id = random.choice(machines)
        cursor.execute("INSERT INTO MaintenanceLogs VALUES (?, ?, ?)", (machine_id, maintenance_date.strftime("%Y-%m-%d"), issue_description))

    conn.commit()
    conn.close()

# Main Script Execution
if __name__ == "__main__":
    print("Generating refined datasets with proportional units produced...")
    generate_production_line_data()
    generate_supplier_schedule()
    generate_inventory_levels()
    generate_maintenance_logs()
    print(f"Datasets have been successfully generated in the '{base_dir}' directory.")
