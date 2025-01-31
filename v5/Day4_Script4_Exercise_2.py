import sqlite3
import logging

# Configure logging
logging.basicConfig(filename="Training_Datasets/Day4/production_logs.log", level=logging.INFO)

def log_production_anomalies(db_file, threshold):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT Machine_ID, SUM(Units_Produced) AS Total_Units
    FROM Production
    GROUP BY Machine_ID
    """)
    results = cursor.fetchall()
    conn.close()

    for row in results:
        if row[1] < threshold:
            logging.warning(f"Anomaly detected: Machine {row[0]} produced {row[1]} units (below threshold of {threshold}).")
        else:
            logging.info(f"Machine {row[0]} production is normal: {row[1]} units.")

# Example Usage
if __name__ == "__main__":
    log_production_anomalies("Training_Datasets/Day4/production_data.db", 500)
    print("Anomalies logged in production_logs.log.")
