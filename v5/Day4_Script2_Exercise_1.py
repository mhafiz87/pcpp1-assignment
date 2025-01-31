import sqlite3
import csv

def insert_production_data(csv_file, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT INTO Production (Machine_ID, Equipment_Type, Run_Start, Run_End, Units_Produced, Product_Category, Product_Type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Machine_ID"], row["Equipment_Type"], row["Run_Start"], row["Run_End"],
                int(row["Units_Produced"]), row["Product_Category"], row["Product_Type"]
            ))

    conn.commit()
    conn.close()
    print("Data inserted successfully.")

# Example Usage
if __name__ == "__main__":
    insert_production_data("Training_Datasets/Day1/production_line_data.csv", "Training_Datasets/Day4/production_data.db")
