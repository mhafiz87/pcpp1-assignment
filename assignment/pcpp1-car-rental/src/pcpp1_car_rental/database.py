import sqlite3
from typing import Literal

from .car import CarData
from .singleton import Singleton

DB_FILE = "car_rental.db"
car_data = CarData()


class Database(metaclass=Singleton):
    def __init__(self):
        self.connection = sqlite3.connect(DB_FILE)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id TEXT PRIMARY KEY,
                brand TEXT NOT NULL,
                model TEXT NOT NULL,
                engine_type TEXT NOT NULL,
                seat_capacity INTEGER NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS customer (
                Contact TEXT PRIMARY KEY,
                full_name TEXT NOT NULL,
                address TEXT NOT NULL,
                email TEXT NOT NULL
            )
            """
        )
        # self.cursor.execute(
        #     """
        #     CREATE TABLE IF NOT EXISTS rental_booking (
        #         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         start_date TEXT NOT NULL,
        #         end_date TEXT NOT NULL,
        #         rent_status TEXT NOT NULL,
        #         FOREIGN KEY (contact) REFERENCES customer (contact),
        #         FOREIGN KEY (id) REFERENCES cars (id)
        #     )
        #     """
        # )
        self.connection.commit()

    def populate_table(self, table: Literal["cars", "customer", "rental_booking"]):
        placeholder = []
        if table == "cars":
            data = car_data.load_car_data()
            for item in data:
                item.pop("status")
                item.pop("start_date")
                item.pop("end_date")
                placeholder.append(tuple(item.values()))
        for item in placeholder:
            print(item)
        try:
            self.cursor.executemany(f"INSERT INTO cars (id, brand, model, engine_type, seat_capacity) VALUES (?, ?, ?, ?, ?)", placeholder)
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Cars with the same ID already exists.")

if __name__ == "__main__":
    db = Database(DB_FILE)
    db.create_tables()
    db.populate_table("cars")