import csv
import json
from pathlib import Path

# CAR_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "car.csv"))
CAR_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "car.json"))


class CarData:
    def __init__(self):
        pass

    def load_car_data_csv(self) -> list[dict]:
        CAR_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "car.csv"))
        data = []
        header = []
        with open(CAR_DATA_PATH, "r") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    header = row
                else:
                    data.append(dict(map(lambda x, y: (x, y), header, row)))
        return data

    def load_car_data_json(self) -> list[dict]:
        CAR_DATA_PATH = str(Path(__file__).parents[2].joinpath("data", "car.json"))
        data = []
        with open(CAR_DATA_PATH, "r") as file:
            read = json.load(file)
            data = read["data"]
        return data

    def load_car_data(self) -> list[dict]:
        return self.load_car_data_json()


if __name__ == "__main__":
    car_data = CarData()
    for item in car_data.load_car_data_csv():
        print(item)
    print("\n")
    for item in car_data.load_car_data_json():
        print(item)
    print("\n")
    for item in car_data.load_car_data():
        print(item)
