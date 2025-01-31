import sqlite3

def query_total_production(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Machine_ID, SUM(Units_Produced) AS Total_Units
    FROM Production
    GROUP BY Machine_ID
    ORDER BY Total_Units DESC
    """)
    results = cursor.fetchall()
    conn.close()

    print("Total Production by Machine:")
    for row in results:
        print(f"Machine {row[0]}: {row[1]} units")

# Example Usage
if __name__ == "__main__":
    query_total_production("Training_Datasets/Day4/production_data.db")
