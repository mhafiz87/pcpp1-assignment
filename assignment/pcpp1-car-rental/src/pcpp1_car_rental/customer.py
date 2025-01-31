import csv
import json
from dataclasses import dataclass
from pathlib import Path

from .singleton import Singleton

# CUSTOMER_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "customer.csv"))
CUSTOMER_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "customer.json"))


@dataclass
class Customer:
    full_name: str
    contact: str
    address: str
    email: str
    car: str
    start_date: str
    end_date: str


class CustomerData(metaclass=Singleton):
    def __init__(self):
        pass

    def load_customer_data_csv(self) -> list[dict]:
        CUSTOMER_DATA_PATH = str(
            Path(__file__).parents[2].joinpath("data", "customer.csv")
        )
        data = []
        header = []
        with open(CUSTOMER_DATA_PATH, "r") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                else:
                    data.append(dict(map(lambda x, y: (x, y), header, row)))
        return data

    def load_customer_data_json(self) -> list[dict]:
        CUSTOMER_DATA_PATH = str(
            Path(__file__).parents[2].joinpath("data", "customer.json")
        )
        data = []
        with open(CUSTOMER_DATA_PATH, "r") as file:
            read = json.load(file)
            data = read["data"]
        return data

    def load_customer_data(self) -> list[dict]:
        return self.load_customer_data_json()

    def update_customer_data(self, data) -> None:
        current_data = self.load_customer_data()
        for info in current_data:
            if info["contact"] == data["contact"]:
                info["start_date"] = data["start_date"]
                info["end_date"] = data["end_date"]
                info["car"] = data["car"]
                break
        else:
            current_data.append(data)
        with open(CUSTOMER_DATA_PATH, "w") as file:
            json.dump({"data": current_data}, file, indent=4)


if __name__ == "__main__":
    customer_data = CustomerData()
    for item in customer_data.load_customer_data_csv():
        print(item)
    print("\n")
    for item in customer_data.load_customer_data_json():
        print(item)
    print("\n")
    for item in customer_data.load_customer_data():
        print(item)
