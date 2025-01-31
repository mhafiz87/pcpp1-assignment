import sqlite3

def initialize_database():
    conn = sqlite3.connect("Training_Datasets/Day4/production_data.db")
    cursor = conn.cursor()

    # Create Production Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Production (
        Machine_ID TEXT,
        Equipment_Type TEXT,
        Run_Start TEXT,
        Run_End TEXT,
        Units_Produced INTEGER,
        Product_Category TEXT,
        Product_Type TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("Database initialized and table created.")

# Example Usage
if __name__ == "__main__":
    initialize_database()
